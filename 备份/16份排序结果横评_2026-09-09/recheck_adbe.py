from pathlib import Path
import re,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
out=Path(__file__).resolve().parent
p=Path('D:/drive/Investment/分析报告/公司情景投资决策/结果/ADBE_经营情景市场状态投资决策_2026-09-09.md')
code=re.findall(r'```(?:javascript|js)\n(.*?)```',p.read_text(encoding='utf-8'),re.S)
assert len(code)==1
assert not re.search(r'\b(?:require|import|process|fetch|exec|writeFile|readFile|child_process)\b',code[0])
(out/'ADBE原文模型_核验副本.js').write_text(code[0],encoding='utf-8')
(out/'ADBE原文来源.json').write_text(json.dumps({'source':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(code[0].encode()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
print('Extracted one self-contained arithmetic model, no I/O calls.')
