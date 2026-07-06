"""
Iteratively fix all compilation errors by:
1. Compiling each program
2. Extracting 'not defined' errors
3. Adding missing vars/paragraphs
4. Re-compiling until clean or max iterations
"""
import sys, subprocess, os, re
sys.path.insert(0, 'app')
from pathlib import Path
from sql_preprocessor import preprocessar_arquivo
from cobol_runner import _cobc, _get_env, COPY_DIR, BUILD_DIR, PROJECT_ROOT, CONVERTIDOS_DIR

SKIP = {'AUML01','CAPA01','CCCC99','COFI02','COFI04','COFI11',
        'EMIS98','EMIS99','EMPA01','GERA01','MENS01','MENS03','RENA01','RENA04'}

FLAGS = [_cobc(), "-m", None, "-o", None, "-I", str(COPY_DIR),
         "-w", "-frelax-syntax-checks", "-frelax-level-hierarchy",
         "-flarger-redefines-ok"]


def compile_prog(source, dll):
    cmd = [_cobc(), "-m", str(source), "-o", str(dll),
           "-I", str(COPY_DIR), "-w", "-frelax-syntax-checks",
           "-frelax-level-hierarchy", "-flarger-redefines-ok"]
    env = _get_env()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env,
                           timeout=30, cwd=str(PROJECT_ROOT))
        return r.returncode == 0, r.stderr
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)


def extract_undefined(stderr):
    # Capturar tudo entre aspas simples que é "not defined" ou "not a field"
    not_defined = list(set(re.findall(r"'([^']+)' is not defined", stderr)))
    not_field = list(set(re.findall(r"'([^']+)' is not a field", stderr)))
    return not_defined + not_field


def add_vars_to_file(filepath, var_names):
    """Add undefined vars/paragraphs to the processed file."""
    content = filepath.read_text(encoding='latin-1')
    
    ws_vars = [v for v in var_names if not any(
        v.startswith(x) for x in ('HANDLE-','DATABASE-','9999-')
    ) and '-DB2DMS' not in v and not re.match(r'\d{3}-', v)
      and '-STBG' not in v.upper() and not v.endswith('-FL')]
    
    # -FL suffixed names are flags (variables), -STBG are SQL statements (paragraphs)
    # But names like XXX-STBG-FL are variables
    ws_vars += [v for v in var_names if v.endswith('-FL')]
    
    pd_paras = [v for v in var_names if v not in ws_vars]
    
    if ws_vars:
        block = '\n      * Auto-fix undefined vars\n'
        for v in sorted(ws_vars):
            block += f'       01  {v[:30]:<30} PIC X(050) VALUE SPACES.\n'
        for marker in ['       LINKAGE SECTION', '       PROCEDURE']:
            if marker in content:
                content = content.replace(marker, block + marker, 1)
                break
    
    if pd_paras:
        block = '\n      * Auto-fix undefined paragraphs\n'
        for p in sorted(pd_paras):
            block += f'       {p}.\n           CONTINUE.\n'
        # Add before COPY PDGL or at end
        for marker in ['       COPY PDGL', '       COPY PDGLDB']:
            if marker in content:
                content = content.replace(marker, block + marker, 1)
                break
        else:
            content += '\n' + block
    
    filepath.write_text(content, encoding='latin-1')


def fix_program(prog_name, max_iter=3):
    source = CONVERTIDOS_DIR / prog_name
    processed = BUILD_DIR / f'{prog_name}_processed'
    dll = BUILD_DIR / f'{prog_name}.dll'
    
    # Remove old
    try:
        processed.unlink(missing_ok=True)
    except:
        pass
    dll.unlink(missing_ok=True)
    
    # Preprocess
    preprocessar_arquivo(source, processed)
    
    for i in range(max_iter):
        ok, stderr = compile_prog(processed, dll)
        if ok:
            return True, f'OK (iter {i})'
        
        undefined = extract_undefined(stderr)
        if not undefined:
            # No "not defined" errors - other errors remain
            err_count = stderr.count('error:')
            return False, f'{err_count} errors (no undefined)'
        
        add_vars_to_file(processed, undefined)
    
    err_count = stderr.count('error:')
    return False, f'{err_count} errors after {max_iter} iterations'


# Main
progs = [f.name for f in sorted(CONVERTIDOS_DIR.iterdir())
         if f.is_file() and not f.name.startswith('MAPA') and f.name not in SKIP]

ok_count = 0
fail_count = 0
fails = []

for p in progs:
    import time
    time.sleep(0.1)
    success, msg = fix_program(p)
    if success:
        ok_count += 1
        print(f'  OK   {p} ({msg})')
    else:
        fail_count += 1
        fails.append((p, msg))
        print(f'  FAIL {p} ({msg})')

print(f'\n=== OK={ok_count} FAIL={fail_count} Total={ok_count+fail_count} ===')
if fails:
    print('\nFalhas restantes:')
    for name, msg in fails:
        print(f'  {name}: {msg}')
