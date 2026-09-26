"""Static-site regression guard. Python standard library only; not a penetration test."""
import base64,hashlib,json,re,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'; errors=[]
def check(ok,message):
 if not ok:errors.append(message)
config=json.loads((ROOT/'vercel.json').read_text())
headers={h['key'].lower():h['value'] for h in config['headers'][0]['headers']}
csp=headers.get('content-security-policy','')
check(config.get('outputDirectory')=='public','Output must be public only')
for policy in ["default-src 'none'","script-src 'self'","script-src-attr 'none'","object-src 'none'","base-uri 'none'","frame-ancestors 'none'","form-action 'none'","connect-src 'none'"]:
 check(policy in csp,'Missing policy: '+policy)
check('unsafe-inline' not in csp and 'unsafe-eval' not in csp,'Unsafe CSP exception')
check(headers.get('x-content-type-options')=='nosniff','Missing nosniff')
check(headers.get('x-frame-options')=='DENY','Missing frame protection')
check(headers.get('x-robots-tag')=='noindex, nofollow','Preview indexing protection missing')
allowed={'.html','.css','.js','.svg','.png','.webp','.mp4','.ico','.txt','.woff2','.woff','.ttf'}
secret=re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_|github_pat_)[A-Za-z0-9_]{25,}|\bAKIA[A-Z0-9]{16}\b|\bsk_live_[A-Za-z0-9]{16,}')
for p in PUBLIC.rglob('*'):
 check(not p.is_symlink(),'Symlink: '+str(p.relative_to(ROOT)))
 if p.is_file():
  check(not p.is_symlink(),'Symlink: '+str(p.relative_to(ROOT)))
  check(p.suffix in allowed and not any(x.startswith('.') for x in p.relative_to(PUBLIC).parts),'Unexpected public file: '+str(p.relative_to(ROOT)))
  if p.suffix in {'.html','.css','.js','.svg','.txt'}:check(not secret.search(p.read_text()),'Potential secret in '+str(p.relative_to(ROOT)))

def resource(value,page):
 parsed=urlsplit(value)
 if parsed.scheme or parsed.netloc:
  check(parsed.scheme=='https' and parsed.hostname=='fonts.googleapis.com','Unexpected external resource: '+page)
 elif parsed.path:
  candidate=(PUBLIC/unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else (PUBLIC/page).parent/unquote(parsed.path)
  candidate=candidate.resolve()
  check(candidate.is_relative_to(PUBLIC) and candidate.is_file(),'Missing/unsafe resource '+value+' in '+page)
class AuditHTML(HTMLParser):
 def __init__(self,page):super().__init__(convert_charrefs=True);self.page=page;self.script=None;self.data=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  check(not any(k.startswith('on') for k in a),'Inline event in '+self.page)
  check('style' not in a,'Inline style in '+self.page)
  check(tag not in {'iframe','object','embed','form','input','textarea'},'New active surface requires review: '+self.page)
  for key in ['href','src','action']:
   check(not re.match(r'\s*(javascript|data|vbscript):',a.get(key,''),re.I),'Unsafe URL in '+self.page)
  if tag=='style':check(False,'Inline CSS in '+self.page)
  if tag=='script':
   self.script=a;self.data=''
   if 'src' in a:resource(a['src'],self.page)
   else:check(a.get('type')=='application/ld+json','Inline executable script in '+self.page)
  if tag in {'img','source','video'}:
   for key in ['src','poster']:
    if a.get(key):resource(a[key],self.page)
  if tag=='link' and a.get('rel') in {'stylesheet','icon'}:resource(a.get('href',''),self.page)
 def handle_data(self,data):
  if self.script is not None:self.data+=data
 def handle_endtag(self,tag):
  if tag=='script' and self.script is not None:
   if self.script.get('type')=='application/ld+json':
    token="'sha256-"+base64.b64encode(hashlib.sha256(self.data.encode()).digest()).decode()+"'"
    check(token in csp,'JSON-LD CSP hash stale: '+self.page)
    try:json.loads(self.data)
    except ValueError:check(False,'Invalid JSON-LD: '+self.page)
   self.script=None
for p in PUBLIC.rglob('*.html'):AuditHTML(str(p.relative_to(PUBLIC))).feed(p.read_text())
for p in PUBLIC.rglob('*.css'):
 text=p.read_text()
 check(not re.search(r'@import\b',text,re.I),'CSS imports require review: '+str(p.relative_to(ROOT)))
 for url in re.findall(r'url\(\s*[\"\']?([^\"\')]+)[\"\']?\s*\)',text,re.I):resource(url.strip(),str(p.relative_to(PUBLIC)))
for p in PUBLIC.rglob('*.js'):
 check(not re.search(r'\beval\s*\(|new\s+Function\s*\(|\.innerHTML\s*=|document\.write\s*\(|\bfetch\s*\(|\bXMLHttpRequest\b|\blocalStorage\b',p.read_text()),'Review JavaScript surface: '+str(p.relative_to(ROOT)))
if errors:
 print('\n'.join('FAIL '+e for e in errors));sys.exit(1)
print('PASS: static surface, local scripts, CSP, assets and high-signal secret checks. Not an exhaustive security guarantee.')
