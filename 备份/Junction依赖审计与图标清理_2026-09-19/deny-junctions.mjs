import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {syncBuiltinESMExports} from 'node:module';
const audit = path.dirname(fileURLToPath(import.meta.url));
const inv = JSON.parse(fs.readFileSync(path.join(audit,'inventory-before.json'),'utf8').replace(/^\uFEFF/,''));
const aliases = inv.Links.map(x=>x.Path.toLowerCase());
const reads = new Set(); const denied=[]; const writes=[];
const originalWrite = fs.writeFileSync.bind(fs);
const staging = path.resolve('D:/investment/分析报告/公司排序/.站点数据-junction-audit-20260919');
const isolated = path.join(audit,'isolated-ranking-output');
fs.mkdirSync(isolated,{recursive:true});
function inspect(p,method){
  if(typeof p!=='string' && !(p instanceof URL) && !Buffer.isBuffer(p))return p;
  const full=path.resolve(p instanceof URL?fileURLToPath(p):p.toString());
  const lower=full.toLowerCase();
  if(aliases.some(x=>lower===x||lower.startsWith(x+path.sep))){denied.push({method,path:full});throw new Error('JUNCTION_DEPENDENCY_BLOCKED: '+full);}
  reads.add(full);return p;
}
for(const name of ['readFile','readdir','stat','lstat','access','realpath','open']){
  const orig=fsp[name].bind(fsp);fsp[name]=function(p,...rest){inspect(p,name);return orig(p,...rest);};
  const sync=name+'Sync';if(fs[sync]){const origSync=fs[sync].bind(fs);fs[sync]=function(p,...rest){inspect(p,sync);return origSync(p,...rest);};}
}
for(const name of ['mkdir','writeFile']){
  const orig=fsp[name].bind(fsp);fsp[name]=function(p,...rest){
    inspect(p,name);const full=path.resolve(p);
    if(full!==staging && !full.startsWith(staging+path.sep))throw new Error('AUDIT_WRITE_OUTSIDE_STAGING: '+full);
    const redirected=path.join(isolated,path.relative(staging,full));writes.push({requested:full,actual:redirected});return orig(redirected,...rest);
  };
}
syncBuiltinESMExports();
process.on('exit',code=>originalWrite(path.join(audit,`runtime-${process.env.JUNCTION_AUDIT_LABEL||'check'}.json`),JSON.stringify({exitCode:code,denied,reads:[...reads],writes},null,2)));
