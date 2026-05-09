from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

def canonical(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def h(v: Any) -> str:
    return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON input must be an object.")
    return data

def write_json(path: str | Path, value: Any) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")

def ingest(path: str) -> dict:
    case = read_json(path)
    required = ["formalism_id", "case_id", "payload", "metadata", "expected_decision"]
    missing = [k for k in required if k not in case]
    if missing:
        return {"decision":"FAIL_CLOSED","reasons":[f"Missing keys: {', '.join(missing)}"],"case":case}
    return {
        "decision":"ALLOW",
        "case_hash":h(case),
        "formalism_id":case["formalism_id"],
        "case_id":case["case_id"],
        "payload":case["payload"],
        "metadata":case["metadata"],
        "expected_decision":case["expected_decision"],
        "sandbox_model":case.get("sandbox_model","github-ubuntu.v1"),
        "reasons":["Case ingested."]
    }

def eval_formalism(i: dict) -> dict:
    fid = i["formalism_id"]
    p = i["payload"]
    if fid == "data-continuation.v1":
        if not p.get("continuation_valid", True):
            decision, reasons = "DENY", ["Continuation validity failed."]
        elif p.get("action") == "disable_governance":
            decision, reasons = "DENY", ["Hard denied action."]
        elif "action" not in p:
            decision, reasons = "FAIL_CLOSED", ["Missing action."]
        else:
            decision, reasons = "ALLOW", ["Data-Continuation constraints passed."]
        return {"formalism_id":fid,"decision":decision,"confidence":1.0,"constraints_checked":["input_shape","continuation_validity","hard_denial"],"reasons":reasons}
    if fid == "gcat-bcat.v1":
        g,c,a,t = float(p.get("g",0)), float(p.get("c",0)), float(p.get("a",0)), float(p.get("t",0))
        K,alpha,beta,gamma = float(p.get("K",1)), float(p.get("alpha",1)), float(p.get("beta",1)), float(p.get("gamma",1))
        capacity = K*(g**alpha)*(c**beta)*(t**gamma)
        invariant = a - capacity
        decision = "ALLOW" if invariant <= 0 else "DENY"
        return {"formalism_id":fid,"decision":decision,"confidence":1.0,"constraints_checked":["I(x)=a-K*g^alpha*c^beta*t^gamma<=0"],"values":{"capacity":capacity,"invariant":invariant},"reasons":["GCAT/BCAT invariant satisfied." if decision=="ALLOW" else "GCAT/BCAT invariant violated."]}
    return {"formalism_id":fid,"decision":"FAIL_CLOSED","confidence":0.0,"reasons":["Unknown formalism adapter."]}

def tvc(i: dict) -> dict:
    m = i.get("metadata",{})
    if any(k in m for k in ("secret","api_key","password","private_key")):
        return {"decision":"DENY","reasons":["Raw secret found."]}
    missing = [k for k in ("authority_ref","policy_ref") if not m.get(k)]
    if missing:
        return {"decision":"FAIL_CLOSED","reasons":[f"Missing TVC refs: {', '.join(missing)}"]}
    return {"decision":"ALLOW","reasons":["TVC refs validated."],"refs":{"authority_ref":m["authority_ref"],"policy_ref":m["policy_ref"]}}

def cge(i: dict, f: dict, tv: dict) -> dict:
    if tv.get("decision") != "ALLOW":
        return {"decision":"FAIL_CLOSED","reasons":["TVC failed."]+tv.get("reasons",[])}
    if f.get("decision") in ("DENY","FAIL_CLOSED"):
        return {"decision":f["decision"],"reasons":["Formalism blocked continuation."]+f.get("reasons",[])}
    risk = float(i.get("payload",{}).get("risk",0.0))
    action = i.get("payload",{}).get("action","continue")
    if action == "state_mutation" or risk >= 0.45:
        return {"decision":"SANDBOX","risk":risk,"reasons":["Sandbox required."]}
    return {"decision":"ALLOW","risk":risk,"reasons":["CGE passed."]}

def sandbox(i: dict, cg: dict) -> dict:
    model = i.get("sandbox_model","github-ubuntu.v1")
    d = cg.get("decision")
    if d in ("ALLOW","DENY","FAIL_CLOSED"):
        final, reasons = d, ["Sandbox preserved terminal decision."]
    elif d == "SANDBOX" and i.get("metadata",{}).get("sandbox_approved") is True:
        final, reasons = "ALLOW", ["Sandbox approved after explicit approval."]
    else:
        final, reasons = "DENY", ["Sandbox denied without approval."]
    return {"sandbox_model":model,"decision":final,"ubuntu_execution":model=="github-ubuntu.v1","stegverse_governance":model in ("stegverse-dryrun.v1","llm-adapter-gate.v1"),"reasons":reasons}

def make_receipt(event_type: str, subject_hash: str, decision: str, details: dict, prev: str|None, timestamp: str|None=None) -> dict:
    r = {"receipt_version":"formalism-test-harness.v001","timestamp_utc":timestamp or now(),"event_type":event_type,"subject_hash":subject_hash,"decision":decision,"details":details,"previous_receipt_hash":prev}
    r["receipt_hash"] = h(r)
    return r

def write_receipts(out: Path, i: dict, f: dict, tv: dict, cg: dict, sb: dict) -> list[dict]:
    receipts=[]; prev=None
    for et, res in [("ingestion",i),("formalism",f),("tvc",tv),("cge",cg),("sandbox",sb)]:
        r = make_receipt(et, i["case_hash"], res.get("decision","ALLOW"), res, prev)
        receipts.append(r); prev = r["receipt_hash"]
    with (out/"original_receipts.jsonl").open("w", encoding="utf-8") as fp:
        for r in receipts: fp.write(json.dumps(r, sort_keys=True, ensure_ascii=False)+"\n")
    return receipts

def verify_chain(path: str|Path) -> dict:
    p=Path(path)
    if not p.exists(): return {"decision":"FAIL_CLOSED","valid":False,"reasons":["Receipt file missing."]}
    prev=None; count=0
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        r=json.loads(line)
        if r.get("previous_receipt_hash") != prev:
            return {"decision":"FAIL_CLOSED","valid":False,"count":count,"reasons":["Previous hash mismatch."]}
        stored=r.get("receipt_hash"); body=dict(r); body.pop("receipt_hash",None)
        if h(body)!=stored:
            return {"decision":"FAIL_CLOSED","valid":False,"count":count,"reasons":["Receipt hash mismatch."]}
        prev=stored; count+=1
    return {"decision":"ALLOW","valid":True,"count":count,"reasons":["Receipt chain verified."]}

def playback(path: str|Path, out_dir: str|Path|None=None) -> dict:
    timeline=[]
    for idx,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if line.strip():
            r=json.loads(line)
            timeline.append({"step":idx,"event_type":r["event_type"],"decision":r["decision"],"receipt_hash":r["receipt_hash"]})
    rep={"decision":"ALLOW","timeline":timeline,"reasons":["Playback generated."]}
    if out_dir: write_json(Path(out_dir)/"playback_report.json", rep)
    return rep

def reconstruct(source_dir: str|Path, out_dir: str|Path) -> dict:
    src=Path(source_dir); out=Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    orig=[json.loads(l) for l in (src/"original_receipts.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    prev=None; rec=[]
    for r in orig:
        nr=make_receipt(r["event_type"], r["subject_hash"], r["decision"], r["details"], prev, timestamp="RECONSTRUCTED")
        rec.append(nr); prev=nr["receipt_hash"]
    with (out/"reconstructed_receipts.jsonl").open("w", encoding="utf-8") as fp:
        for r in rec: fp.write(json.dumps(r, sort_keys=True, ensure_ascii=False)+"\n")
    rep={"decision":"ALLOW","reconstructed_count":len(rec),"known_limitation":"timestamps intentionally differ; compare events, not receipt hashes.","reasons":["Receipts reconstructed from original event details."]}
    write_json(out/"reconstruction_report.json", rep)
    return rep

def compare(original: str|Path, reconstructed: str|Path, out_dir: str|Path) -> dict:
    a=[json.loads(l) for l in Path(original).read_text(encoding="utf-8").splitlines() if l.strip()]
    b=[json.loads(l) for l in Path(reconstructed).read_text(encoding="utf-8").splitlines() if l.strip()]
    aligned=sum(1 for x,y in zip(a,b) if x["event_type"]==y["event_type"] and x["decision"]==y["decision"] and x["subject_hash"]==y["subject_hash"])
    total=max(len(a),len(b),1)
    rep={"decision":"ALLOW" if aligned==total else "SANDBOX","original_count":len(a),"reconstructed_count":len(b),"aligned_events":aligned,"alignment":aligned/total,"reasons":["Receipt event comparison completed."]}
    write_json(Path(out_dir)/"receipt_comparison.json", rep)
    return rep

def artifact_manifest(out: Path) -> dict:
    files=["ingestion_report.json","formalism_result.json","tvc_result.json","cge_result.json","sandbox_result.json","original_receipts.jsonl"]
    entries=[]
    for f in files:
        p=out/f
        if p.exists(): entries.append({"path":f,"hash":hashlib.sha256(p.read_bytes()).hexdigest()})
    rep={"decision":"ALLOW","artifacts":entries}
    write_json(out/"artifact_manifest.json", rep)
    return rep

def confidence(source: str|Path, out_dir: str|Path) -> dict:
    src=Path(source)
    verified = verify_chain(src/"original_receipts.jsonl").get("valid", False)
    comp = read_json(src/"receipt_comparison.json") if (src/"receipt_comparison.json").exists() else {"alignment":0}
    align=float(comp.get("alignment",0))
    dims={"receipt_chain_integrity":1.0 if verified else 0.0,"artifact_hash_alignment":1.0 if (src/"artifact_manifest.json").exists() else 0.5,"formalism_decision_alignment":align,"tvc_alignment":align,"cge_alignment":align,"sandbox_decision_alignment":align,"playback_alignment":1.0 if (src/"playback_report.json").exists() else 0.0,"reconstruction_alignment":align,"missing_data_penalty":0.0 if align>=1 else 0.1,"unexpected_mutation_penalty":0.0,"unexplained_gap_penalty":0.0 if align>=1 else 0.05}
    positives=[dims[k] for k in ["receipt_chain_integrity","artifact_hash_alignment","formalism_decision_alignment","tvc_alignment","cge_alignment","sandbox_decision_alignment","playback_alignment","reconstruction_alignment"]]
    score=max(0.0,min(1.0,sum(positives)/len(positives)-dims["missing_data_penalty"]-dims["unexpected_mutation_penalty"]-dims["unexplained_gap_penalty"]))
    rep={"decision":"ALLOW" if score>=0.85 else "SANDBOX","confidence":score,"dimensions":dims,"recommendation":"ALLOW_WITH_MONITORING" if score>=0.85 else "CONTINUE_TESTING"}
    write_json(Path(out_dir)/"confidence_report.json", rep)
    return rep

def sandbox_report(source: str|Path, out_dir: str|Path) -> dict:
    src=Path(source)
    conf=read_json(src/"confidence_report.json") if (src/"confidence_report.json").exists() else {"confidence":0}
    sb=read_json(src/"sandbox_result.json") if (src/"sandbox_result.json").exists() else {"sandbox_model":"unknown"}
    model=sb.get("sandbox_model","unknown")
    rep={"decision":"ALLOW" if conf.get("confidence",0)>=0.85 else "CONTINUE_TESTING","task_class":"formalism-test","sandbox_models":{model:{"confidence":conf.get("confidence",0),"runs":1}},"preferred_sandbox":model,"recommendation":"CONTINUE_TESTING" if conf.get("confidence",0)<0.95 else "ALLOW"}
    write_json(Path(out_dir)/"sandbox_model_report.json", rep)
    return rep

def run_case(path: str, out_dir: str|Path) -> dict:
    out=Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    i=ingest(path)
    f=eval_formalism(i) if i["decision"]=="ALLOW" else {"decision":"FAIL_CLOSED","reasons":["ingestion failed"]}
    tv= t = tvc(i) if i["decision"]=="ALLOW" else {"decision":"FAIL_CLOSED","reasons":["ingestion failed"]}
    cg=cge(i,f,tv) if i["decision"]=="ALLOW" else {"decision":"FAIL_CLOSED","reasons":["ingestion failed"]}
    sb=sandbox(i,cg) if i["decision"]=="ALLOW" else {"decision":"FAIL_CLOSED","sandbox_model":"unknown","reasons":["ingestion failed"]}
    for name,val in [("ingestion_report.json",i),("formalism_result.json",f),("tvc_result.json",tv),("cge_result.json",cg),("sandbox_result.json",sb)]:
        write_json(out/name,val)
    write_receipts(out,i,f,tv,cg,sb)
    artifact_manifest(out)
    playback(out/"original_receipts.jsonl", out)
    reconstruct(out, out/"reconstruction")
    compare(out/"original_receipts.jsonl", out/"reconstruction"/"reconstructed_receipts.jsonl", out)
    conf=confidence(out,out)
    sr=sandbox_report(out,out)
    return {"decision":sb["decision"],"case_id":i.get("case_id"),"formalism_id":i.get("formalism_id"),"receipt_verify":verify_chain(out/"original_receipts.jsonl"),"confidence":conf,"sandbox_model_report":sr}

def main():
    ap=argparse.ArgumentParser(prog="formalism-harness")
    sub=ap.add_subparsers(dest="cmd", required=True)
    r=sub.add_parser("run"); r.add_argument("case"); r.add_argument("--out",default="out")
    p=sub.add_parser("playback"); p.add_argument("receipts"); p.add_argument("--out",default=None)
    rec=sub.add_parser("reconstruct"); rec.add_argument("source"); rec.add_argument("--out",default="out/reconstruction")
    co=sub.add_parser("compare"); co.add_argument("original"); co.add_argument("reconstructed"); co.add_argument("--out",default="out")
    cf=sub.add_parser("confidence"); cf.add_argument("source"); cf.add_argument("--out",default="out")
    sr=sub.add_parser("sandbox-report"); sr.add_argument("source"); sr.add_argument("--out",default="out")
    v=sub.add_parser("verify"); v.add_argument("receipts")
    st=sub.add_parser("selftest"); st.add_argument("--out",default="out")
    args=ap.parse_args()
    if args.cmd=="run": res=run_case(args.case,args.out)
    elif args.cmd=="playback": res=playback(args.receipts,args.out)
    elif args.cmd=="reconstruct": res=reconstruct(args.source,args.out)
    elif args.cmd=="compare": res=compare(args.original,args.reconstructed,args.out)
    elif args.cmd=="confidence": res=confidence(args.source,args.out)
    elif args.cmd=="sandbox-report": res=sandbox_report(args.source,args.out)
    elif args.cmd=="verify": res=verify_chain(args.receipts)
    elif args.cmd=="selftest":
        res=run_case("examples/data_continuation_allow.json", args.out)
        write_json(Path(args.out)/"selftest_report.json", res)
    print(json.dumps(res, indent=2, sort_keys=True, ensure_ascii=False))

if __name__=="__main__":
    main()
