"""Check errors for a specific program."""
import sys, subprocess, os, re
sys.path.insert(0, 'app')
from sql_preprocessor import preprocessar_arquivo
from pathlib import Path
from cobol_runner import _cobc, _get_env, COPY_DIR, BUILD_DIR, PROJECT_ROOT, CONVERTIDOS_DIR

prog = sys.argv[1] if len(sys.argv) > 1 else 'FGAA032D'
src = CONVERTIDOS_DIR / prog
out = BUILD_DIR / f'{prog}_processed'
dll = BUILD_DIR / f'{prog}.dll'

dll.unlink(missing_ok=True)
out.unlink(missing_ok=True)

preprocessar_arquivo(src, out)
env = _get_env()
r = subprocess.run([_cobc(), '-m', str(out), '-o', str(dll), '-I', str(COPY_DIR)],
                   capture_output=True, text=True, env=env, timeout=30, cwd=str(PROJECT_ROOT))

errs = re.findall(r'error: (.+)', r.stderr)
unique_errs = set(e[:80] for e in errs)
print(f'{prog}: {len(errs)} errors ({len(unique_errs)} unique)')
for e in sorted(unique_errs)[:15]:
    print(f'  {e}')
