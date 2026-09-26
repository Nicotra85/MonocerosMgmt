"""Create and restore a temporary site backup; compare every file, then audit restored copy."""
import hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def files(root):return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in {'.git','__pycache__'} for x in p.relative_to(root).parts))
def manifest(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files(root)}
before=manifest(ROOT)
with tempfile.TemporaryDirectory(prefix='monoceros-restore-') as tmp:
 temp=Path(tmp); archive=temp/'backup.zip'; restored=temp/'restored'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files(ROOT):z.write(p,p.relative_to(ROOT))
 with zipfile.ZipFile(archive) as z:z.extractall(restored)
 assert manifest(restored)==before,'Restored bytes differ'
 subprocess.run([sys.executable,str(restored/'scripts/security_check.py'),str(restored)],check=True)
 print(json.dumps({'restore':'PASS','files_verified':len(before),'method':'SHA-256 every file; static security check rerun','scope':'Local static files only; no database, cloud recovery or scheduled backup tested'},indent=2))
