#!/usr/bin/env python3
from __future__ import annotations
import ast, hashlib, json, os, re, shutil, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPORT_DIR=Path('reports/current/stegverse-001-remote-core-lite')
RECEIPT_DIR=Path('receipts/current/stegverse-001-remote-core-lite')
REPORT_JSON=REPORT_DIR/'working_contract_report.json'
REPORT_MD=REPORT_DIR/'working_contract_report.md'
PLAN_JSON=REPORT_DIR/'remediation_plan.json'
RECEIPTS=RECEIPT_DIR/'receipts.jsonl'
DEFAULT_REPO='Data-Continuation/core-lite'
DEFAULT_BRANCH='main'
DEFAULT_WORK_DIR=Path(tempfile.gettempdir())/'stegverse-001-remote-core-lite'
CORE_PACKAGE='core_lite'

def canonical_json(v:dict[str,Any])->str:
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True)

def hash_dict(v:dict[str,Any])->str:
    return hashlib.sha256(canonical_json(v).encode()).hexdigest()

def sha256_file(p:Path)->str|None:
    if not p.exists() or not p.is_file(): return None
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

class ReceiptChain:
    def __init__(self,p:Path):
        self.path=p; self.path.parent.mkdir(parents=True,exist_ok=True); self.previous_hash=self._last_hash()
    def _last_hash(self):
        if not self.path.exists(): return None
        last=None
        for line in self.path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                try: last=json.loads(line).get('receipt_hash')
                except json.JSONDecodeError: pass
        return last
    def record(self,event_type,decision,basis,metadata=None):
        r={'schema':'stegverse_001_remote_operator_receipt.v3','generated_at':datetime.now(timezone.utc).isoformat(),'actor':'StegVerse-001','event_type':event_type,'decision':decision,'basis':basis,'previous_receipt_hash':self.previous_hash,'metadata':metadata or {}}
        r['receipt_hash']=hash_dict(r)
        with self.path.open('a',encoding='utf-8') as f: f.write(canonical_json(r)+'\n')
        self.previous_hash=r['receipt_hash']; return r

def read_text(p:Path)->str:
    if not p.exists() or not p.is_file(): return ''
    try: return p.read_text(encoding='utf-8')
    except UnicodeDecodeError: return ''

def module_name_from_path(p:Path,root:Path)->str|None:
    try: rel=p.relative_to(root)
    except ValueError: return None
    if not rel.parts or rel.parts[0]!=CORE_PACKAGE or p.suffix!='.py': return None
    parts=rel.with_suffix('').parts[:-1] if p.name=='__init__.py' else rel.with_suffix('').parts
    return '.'.join(parts) if parts else None

def parse_python(p:Path,root:Path)->dict[str,Any]:
    rel=p.relative_to(root).as_posix() if p.exists() and root in p.parents else p.as_posix()
    txt=read_text(p)
    c={'path':rel,'module':module_name_from_path(p,root),'exists':p.exists() and p.is_file(),'sha256':sha256_file(p),'functions':[],'classes':[],'exports':[],'import_from':[],'imports':[],'parse_error':None}
    if not txt: return c
    try: tree=ast.parse(txt)
    except SyntaxError as e: c['parse_error']=f'{type(e).__name__}: {e}'; return c
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)): c['functions'].append(n.name)
        elif isinstance(n,ast.ClassDef): c['classes'].append(n.name)
        elif isinstance(n,ast.ImportFrom): c['import_from'].append({'module':n.module or '','level':n.level,'names':[a.name for a in n.names]})
        elif isinstance(n,ast.Import): c['imports'].extend(a.name for a in n.names)
    c['functions']=sorted(set(c['functions'])); c['classes']=sorted(set(c['classes'])); c['exports']=sorted(set(c['functions'])|set(c['classes'])); c['imports']=sorted(set(c['imports']))
    return c

def resolve_import_module(importing_module:str,item:dict[str,Any])->str|None:
    raw=item.get('module',''); level=int(item.get('level',0) or 0)
    if level==0:
        if raw==CORE_PACKAGE or raw.startswith(CORE_PACKAGE+'.'): return raw
        if importing_module.startswith(CORE_PACKAGE+'.') and raw: return f'{CORE_PACKAGE}.{raw}'
        return None
    parts=importing_module.split('.')[:-1]
    if level>1: parts=parts[:-(level-1)]
    if raw: parts.append(raw)
    return '.'.join(parts) if parts else None

def collect_core_contracts(root:Path):
    core=root/CORE_PACKAGE; out={}
    if not core.exists(): return out
    for p in sorted(core.glob('*.py')):
        c=parse_python(p,root); m=c.get('module')
        if m: out[m]=c
    return out

def inspect_internal_import_contracts(contracts):
    observed=[]; missing=[]
    for importing_module,c in sorted(contracts.items()):
        for item in c.get('import_from',[]):
            target=resolve_import_module(importing_module,item)
            if not target or not target.startswith(CORE_PACKAGE+'.'): continue
            if target not in contracts and item.get('level', 0) == 0 and not str(item.get('module', '')).startswith(CORE_PACKAGE + '.'):
                continue
            names=item.get('names',[]); tc=contracts.get(target)
            observed.append({'importing_module':importing_module,'importing_path':c.get('path'),'from_module':item.get('module',''),'level':item.get('level',0),'resolved_module':target,'names':names,'target_exists':tc is not None})
            if tc is None:
                missing.append({'type':'missing_internal_module','importing_module':importing_module,'required_module':target,'names':names}); continue
            exports=set(tc.get('exports',[]))
            for name in names:
                if name!='*' and name not in exports:
                    missing.append({'type':'missing_internal_export','importing_module':importing_module,'required_module':target,'required_export':name,'target_path':tc.get('path')})
    return observed,missing

def inspect_workflows(root:Path):
    wd=root/'.github'/'workflows'; out=[]
    if not wd.exists(): return out
    for p in sorted(wd.glob('*')):
        if not p.is_file(): continue
        t=read_text(p)
        out.append({'path':p.relative_to(root).as_posix(),'sha256':sha256_file(p),'mentions_incoming':'incoming' in t,'mentions_intake':'intake' in t.lower(),'mentions_cge':'cge' in t.lower(),'mentions_cli':'cli' in t.lower(),'mentions_reports_current':'reports/current' in t,'python_commands':re.findall(r'python[^\n]+',t),'workflow_dispatch':'workflow_dispatch' in t})
    return out

def inspect_task_manifests(root:Path):
    td=root/'tools'/'tasks'; out=[]
    if not td.exists(): return out
    for p in sorted(td.glob('*.json')):
        e={'path':p.relative_to(root).as_posix(),'sha256':sha256_file(p),'task_ids':[],'commands':[],'parse_error':None}
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
            for task in data.get('tasks',[]):
                if isinstance(task,dict):
                    if task.get('task_id'): e['task_ids'].append(task['task_id'])
                    if task.get('command'): e['commands'].append(task['command'])
        except Exception as ex: e['parse_error']=f'{type(ex).__name__}: {ex}'
        out.append(e)
    return out

def clone_or_use_local(receipts):
    local=os.environ.get('CORE_LITE_LOCAL_PATH','').strip(); repo=os.environ.get('CORE_LITE_REPO',DEFAULT_REPO).strip() or DEFAULT_REPO; branch=os.environ.get('CORE_LITE_BRANCH',DEFAULT_BRANCH).strip() or DEFAULT_BRANCH; token=os.environ.get('CORE_LITE_TOKEN') or os.environ.get('GITHUB_TOKEN') or ''
    if local:
        lp=Path(local); meta={'mode':'local','repo':repo,'branch':branch,'root':lp.as_posix(),'success':lp.exists()}
        receipts.record('target_repo_selected','LOCAL_PATH_SELECTED' if meta['success'] else 'FAIL_CLOSED','StegVerse-001 selected local target path for inspection.',meta)
        return (lp if lp.exists() else None), meta
    work=Path(os.environ.get('CORE_LITE_WORK_DIR',str(DEFAULT_WORK_DIR))); shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True,exist_ok=True)
    clone=work/'core-lite'; url=f'https://x-access-token:{token}@github.com/{repo}.git' if token else f'https://github.com/{repo}.git'
    safe=repo
    proc=subprocess.run(['git','clone','--depth','1','--branch',branch,url,str(clone)],text=True,capture_output=True)
    meta={'mode':'clone','repo':safe,'branch':branch,'root':clone.as_posix(),'runtime_work_dir':work.as_posix(),'success':proc.returncode==0,'returncode':proc.returncode,'stdout_tail':proc.stdout[-2000:],'stderr_tail':proc.stderr[-2000:],'runtime_committed_path':False}
    receipts.record('target_repo_cloned','CLONED' if proc.returncode==0 else 'FAIL_CLOSED','StegVerse-001 cloned target repo into runtime temp space for inspection.',meta)
    return (clone if proc.returncode==0 else None), meta

def group_missing_by_target(missing):
    grouped={}
    for item in missing:
        if item['type']=='missing_internal_export':
            key=(item['required_module'],item.get('target_path') or '')
            g=grouped.setdefault(key,{'type':'internal_contractual_inclusion','target_module':item['required_module'],'target_path':item.get('target_path'),'required_exports':[],'required_by':[]})
            g['required_exports'].append(item['required_export']); g['required_by'].append(item['importing_module'])
        else:
            key=(item.get('required_module','unknown'),'')
            g=grouped.setdefault(key,{'type':'missing_internal_module','target_module':item.get('required_module'),'target_path':None,'required_exports':[],'required_by':[]})
            g['required_by'].append(item['importing_module'])
    out=[]
    for g in grouped.values():
        g['required_exports']=sorted(set(g['required_exports'])); g['required_by']=sorted(set(g['required_by'])); out.append(g)
    return sorted(out,key=lambda x:(x.get('target_path') or '',x.get('target_module') or ''))

def determine_contract(root:Path):
    contracts=collect_core_contracts(root); observed,missing=inspect_internal_import_contracts(contracts); grouped=group_missing_by_target(missing)
    surfaces={'incoming':{'path':'incoming/','exists':(root/'incoming').exists(),'file_count':len([p for p in (root/'incoming').rglob('*') if p.is_file()]) if (root/'incoming').exists() else 0},'reports_current':{'path':'reports/current/','exists':(root/'reports'/'current').exists()},'receipts_current':{'path':'receipts/current/','exists':(root/'receipts'/'current').exists()},'workflows':inspect_workflows(root),'task_manifests':inspect_task_manifests(root)}
    req={'incoming_bundle_detected':surfaces['incoming']['exists'],'workflow_execution_surface':bool(surfaces['workflows'])}
    for m in ['core_lite.cli','core_lite.cge','core_lite.ingest','core_lite.sandbox','core_lite.receipts']: req[f'{m}_surface']=m in contracts
    blockers=[]
    for item in grouped: blockers.append({'type':item['type'],'basis':'Internal core_lite import/export contract mismatch detected.','items':[item]})
    for k,v in req.items():
        if not v: blockers.append({'type':'missing_transition_surface','basis':f'Required surface absent for active transition: {k}','items':[k]})
    if grouped:
        first=grouped[0]
        next_change={'classification':first['type'],'target':first.get('target_path') or first.get('target_module'),'target_module':first.get('target_module'),'required_exports':first.get('required_exports',[]),'required_by':first.get('required_by',[]),'preserve_existing_exports':True,'basis':'Observed internal import contract requires these exports before Intake can run.'}
    elif blockers: next_change={'classification':'minimal_surface_completion','target':'first_missing_transition_surface','basis':'Complete only the missing surface required by the active transition.'}
    else: next_change={'classification':'run_existing_intake','target':'existing Core-Lite Intake workflow','basis':'No internal import/export blockers observed for the active transition.'}
    report={'schema':'stegverse_001_remote_core_lite_working_contract_report.v3','generated_at':datetime.now(timezone.utc).isoformat(),'success':True,'actor':'StegVerse-001','mode':'initialization','target_repo_root':root.resolve().as_posix(),'active_transition':'Core-Lite Recorded Ingestion + CGE + Sandbox Result Return','core_package':CORE_PACKAGE,'python_contracts':contracts,'observed_internal_imports':observed,'missing_internal_contracts':missing,'grouped_missing_internal_contracts':grouped,'surfaces':surfaces,'transition_requirements':req,'blockers':blockers,'decision':'PLAN_RETURNED','boundary':['formalism-tests is the proof and command backdrop.','core-lite is the remote target.','This task does not patch, push, submit incoming bundles, or change workflows.','Runtime clone is outside the repo working tree by default.','STOP after report, plan, and receipt.']}
    plan={'schema':'stegverse_001_remote_core_lite_remediation_plan.v3','generated_at':report['generated_at'],'actor':'StegVerse-001','transition':report['active_transition'],'decision':'RETURN_PLAN_ONLY','install_authority':False,'production_authority':False,'workflow_change_authority':False,'push_authority':False,'incoming_submission_authority':False,'blockers':blockers,'next_admissible_change':next_change,'stop_condition':'Return plan and receipt. Do not mutate target repo.'}
    return report,plan

def write_markdown(report,plan):
    lines=['# StegVerse-001 Remote Core-Lite Working Contract Report','','## Status','','```text',f"actor: {report['actor']}",f"mode: {report['mode']}",f"schema: {report['schema']}",f"active_transition: {report['active_transition']}",f"decision: {report['decision']}",f"blocker_count: {len(report['blockers'])}",'```','','## Missing Internal Contracts','']
    if report['grouped_missing_internal_contracts']:
        for item in report['grouped_missing_internal_contracts']:
            lines += [f"### {item.get('target_module')}",'','```text',f"type: {item.get('type')}",f"target_path: {item.get('target_path')}",f"required_exports: {', '.join(item.get('required_exports', [])) or '(none)'}",f"required_by: {', '.join(item.get('required_by', []))}",'```','']
    else: lines += ['No missing internal import/export contracts observed.','']
    lines += ['## Next Admissible Change','','```json',json.dumps(plan['next_admissible_change'],indent=2,sort_keys=True),'```','','## Boundary','','```text','No target mutation.','No push.','No workflow widening.','No incoming bundle submission.','No production.','Return plan and receipt.','STOP.','```']
    REPORT_MD.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    REPORT_DIR.mkdir(parents=True,exist_ok=True); RECEIPT_DIR.mkdir(parents=True,exist_ok=True)
    receipts=ReceiptChain(RECEIPTS); receipts.record('remote_operator_started','RECEIVED','StegVerse-001 remote operator v3 started from formalism-tests backdrop.',{'target_repo':os.environ.get('CORE_LITE_REPO',DEFAULT_REPO),'branch':os.environ.get('CORE_LITE_BRANCH',DEFAULT_BRANCH)})
    target,meta=clone_or_use_local(receipts)
    if target is None:
        failure={'schema':'stegverse_001_remote_core_lite_working_contract_report.v3','generated_at':datetime.now(timezone.utc).isoformat(),'success':False,'decision':'FAIL_CLOSED','basis':'Could not access target repo.','target_access':meta}
        REPORT_JSON.write_text(json.dumps(failure,indent=2,sort_keys=True)+'\n',encoding='utf-8'); PLAN_JSON.write_text(json.dumps({'schema':'stegverse_001_remote_core_lite_remediation_plan.v3','decision':'FAIL_CLOSED','basis':'Could not access target repo.'},indent=2,sort_keys=True)+'\n',encoding='utf-8'); receipts.record('remote_operator_failed','FAIL_CLOSED','Could not access target repo.',meta); print(json.dumps(failure,indent=2,sort_keys=True)); return 1
    report,plan=determine_contract(target); report['target_access']=meta
    REPORT_JSON.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8'); PLAN_JSON.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n',encoding='utf-8'); write_markdown(report,plan)
    receipts.record('remote_contract_determined','PLAN_RETURNED','StegVerse-001 determined remote core-lite internal contracts and returned a plan.',{'report':REPORT_JSON.as_posix(),'plan':PLAN_JSON.as_posix(),'blocker_count':len(report['blockers']),'next_admissible_change':plan['next_admissible_change']})
    print(json.dumps(report,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
