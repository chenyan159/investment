import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const sdkUrl = new URL('../node_modules/@openai/codex-sdk/dist/index.js', import.meta.url).href;
const supervisorUrl = new URL('../codex-turn.mjs', import.meta.url).href;
const queueUrl = new URL('../queue-store.mjs', import.meta.url).href;

test('installed SDK accepts successful completion after cancelling its stuck CLI', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'runner-sdk-exit-'));
  try {
    // Node acts as the executable; SDK's first CLI argument is the local script
    // named "exec". No credentials, API calls or real Codex processes are used.
    fs.writeFileSync(path.join(root, 'exec'), `
      process.stdin.resume();
      process.stdin.on('end', () => {
        console.log(JSON.stringify({type:'thread.started',thread_id:'local-fixture'}));
        console.log(JSON.stringify({type:'item.completed',item:{id:'1',type:'agent_message',text:'report complete'}}));
        console.log(JSON.stringify({type:'turn.completed',usage:{input_tokens:10,cached_input_tokens:0,output_tokens:2}}));
        setInterval(()=>{},1000);
      });
    `);
    const script = `
      import assert from 'node:assert/strict';
      import { Codex } from ${JSON.stringify(sdkUrl)};
      import { runCodexTurn } from ${JSON.stringify(supervisorUrl)};
      const thread = new Codex({codexPathOverride:process.execPath}).startThread({skipGitRepoCheck:true});
      const result = await runCodexTurn(thread, 'fixture', {timeoutMs:3000,exitGraceMs:40,cleanupMs:1000});
      assert.equal(result.threadId,'local-fixture');
      assert.equal(result.finalResponse,'report complete');
      assert.equal(result.usage.output_tokens,2);
      console.log('SDK fixture passed');
    `;
    const child = spawnSync(process.execPath, ['--input-type=module', '-e', script], { cwd: root, windowsHide: true, encoding: 'utf8', timeout: 6000 });
    assert.equal(child.status, 0, child.stderr || child.error?.message);
    assert.match(child.stdout, /SDK fixture passed/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('cleanup quarantine preserves output and survives interrupted-run recovery', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'runner-cleanup-queue-'));
  try {
    const script = `
      import assert from 'node:assert/strict';
      import fs from 'node:fs';
      import {ensureQueueFiles,writeActiveQueue,readActiveQueue,markQueueItemCleanupBlocked,hasCleanupBlock,recoverRunningQueueItems} from ${JSON.stringify(queueUrl)};
      ensureQueueFiles();
      const base={domain:'company',subject:'TEST',status:'running',attempts:1};
      writeActiveQueue([{...base,id:'protected'},{...base,id:'ordinary'}]);
      fs.writeFileSync('report.md','finished report');
      markQueueItemCleanupBlocked('protected','pid 123');
      assert.ok(readActiveQueue().some(hasCleanupBlock));
      const before=readActiveQueue().find(x=>x.id==='protected');
      assert.deepEqual(recoverRunningQueueItems({maxAttempts:7}),{recovered:1,failed:0});
      assert.deepEqual(readActiveQueue().find(x=>x.id==='protected'),before);
      assert.equal(readActiveQueue().find(x=>x.id==='ordinary').status,'retry_pending');
      assert.equal(fs.readFileSync('report.md','utf8'),'finished report');
    `;
    const child = spawnSync(process.execPath, ['--input-type=module', '-e', script], {
      cwd: root, windowsHide: true, encoding: 'utf8', timeout: 6000,
      env: { ...process.env, RESEARCH_RUNNER_QUEUE_DIR: root },
    });
    assert.equal(child.status, 0, child.stderr || child.error?.message);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
