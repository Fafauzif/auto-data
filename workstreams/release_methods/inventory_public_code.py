"""Static public-code inventory. Reads AST/text only; does not import acquisition scripts."""
import ast,json,collections,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
modules=collections.defaultdict(set);dependencies=[];errors=[];scripts=[]
for p in sorted(ROOT.rglob('*.py')):
 if 'private_cache' in p.parts or '__pycache__' in p.parts:continue
 scripts.append(p);text=p.read_text()
 try:tree=ast.parse(text)
 except SyntaxError as e:errors.append({'file':str(p.relative_to(ROOT)),'line':e.lineno,'syntax_error':e.msg});continue
 for n in ast.walk(tree):
  if isinstance(n,ast.Import):
   for x in n.names:modules[x.name.split('.')[0]].add(str(p.relative_to(ROOT)))
  elif isinstance(n,ast.ImportFrom) and n.module:modules[n.module.split('.')[0]].add(str(p.relative_to(ROOT)))
 if p==Path(__file__).resolve():continue
 for i,line in enumerate(text.splitlines(),1):
  if '/workspace/scratch/' in line or '/opt/codex/' in line or 'ROOT.parent/' in line or 'ROOT.parent /' in line:dependencies.append({'file':str(p.relative_to(ROOT)),'line':i,'kind':'absolute_runtime_or_external_workspace_dependency'})
result={'snapshot_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_count':len(scripts),'imports':{k:sorted(v) for k,v in modules.items()},'hardcoded_or_parent_dependencies':dependencies,'syntax_errors':errors,'imported_or_executed_research_scripts':False,'secret_values_printed':False,'inspection_scope':'static syntax/import/path scan; not end-to-end functional validation'}
(OUT/'SCRIPT_INVENTORY_QA.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['imports','hardcoded_or_parent_dependencies']},indent=2));print('path_dependency_locations',len(dependencies))
