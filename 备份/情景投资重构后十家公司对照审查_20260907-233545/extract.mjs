import fs from 'node:fs';
import path from 'node:path';
const root=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
const base=decodeURIComponent(root);
const manifest=JSON.parse(fs.readFileSync(path.join(base,'manifest.json'),'utf8'));
const all=[];
for(const m of manifest)for(const version of ['new','old']){
 const file=m[version+'Snapshot'];const text=fs.readFileSync(file,'utf8');const lines=text.split(/\r?\n/);const tables=[];
 for(let i=0;i<lines.length;i++)if(/^\s*\|/.test(lines[i])){const start=i;while(i+1<lines.length&&/^\s*\|/.test(lines[i+1]))i++;const rows=lines.slice(start,i+1);tables.push({line:start+1,end:i+1,header:rows[0],rows});}
 const matrices=tables.filter(t=>['悲观','基准','乐观','突破'].every(w=>t.rows.some(r=>r.split('|')[1]?.includes(w)))&&t.rows.filter(r=>/建议|等待|中性/.test(r)).length>=4&&t.rows.length<=8);
 const headings=lines.map((s,i)=>({line:i+1,text:s})).filter(x=>/^#{1,3} /.test(x.text));
 all.push({subject:m.subject,version,file,chars:text.length,lines:lines.length,headings,tables:tables.map(t=>({line:t.line,end:t.end,header:t.header})),matrices});
}
fs.writeFileSync(path.join(base,'structure.json'),JSON.stringify(all,null,2));
let out='# 两轮条件矩阵原文\n\n';for(const a of all){out+=`## ${a.subject} ${a.version}\n\n`;for(const t of a.matrices)out+=`来源行 ${t.line}\n\n${t.rows.join('\n')}\n\n`;}
fs.writeFileSync(path.join(base,'两轮条件矩阵原文.md'),out);
console.log(JSON.stringify(all.map(a=>({subject:a.subject,version:a.version,matrices:a.matrices.map(t=>t.line),chars:a.chars,lines:a.lines})),null,2));
