#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
HEX40=re.compile(r"^[0-9a-f]{40}$")
REQUIRED={"tt_transition_element_schema","transition_role_model","continuation_decision_function","standing_proof_candidates","entity_architecture_slot","stage25_entity_charter_runner","stage30_instantiation_runner","external_derivation_schema","portable_reduction_schema"}
def fail(m): raise SystemExit("FAIL: "+m)
def check(p):
 d=json.loads(Path(p).read_text())
 if d.get("schema")!="stegverse.sv011-canonical-source-pins/v0.1": fail("schema")
 if d.get("entity_id")!="SV-011": fail("entity")
 if d.get("authority_effect")!="NONE": fail("authority")
 pins=d.get("pins") or []
 ids=[x.get("id") for x in pins]
 if set(ids)!=REQUIRED or len(ids)!=len(REQUIRED): fail("required pin set drift")
 for x in pins:
  for k in ("repository","path","role"):
   if not x.get(k): fail("missing "+k)
  if not HEX40.fullmatch(str(x.get("commit",""))) or not HEX40.fullmatch(str(x.get("blob",""))): fail("commit/blob identity")
 r=d.get("rules") or {}
 if r.get("resolve_by_commit_and_blob") is not True or r.get("main_branch_is_not_identity") is not True or r.get("downstream_copy_is_not_authority") is not True: fail("pin rules")
 print("PASS: SV-011 canonical source pinset satisfies v0.1 contract")
if __name__=="__main__":
 if len(sys.argv)!=2: raise SystemExit("usage: check_sv011_canonical_source_pins.py <pins.json>")
 check(sys.argv[1])
