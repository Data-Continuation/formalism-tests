import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PIN=ROOT/"data"/"sv011_canonical_source_pins.json"
CHECK=ROOT/"tools"/"check_sv011_canonical_source_pins.py"
def main():
 r=subprocess.run([sys.executable,str(CHECK),str(PIN)],capture_output=True,text=True)
 assert r.returncode==0, r.stdout+r.stderr
 assert "PASS:" in r.stdout
 print("SV011_CANONICAL_SOURCE_PINS_PASS")
 return 0
if __name__=="__main__": raise SystemExit(main())
