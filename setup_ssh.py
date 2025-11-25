from pathlib import Path
import subprocess, sys

def run(cmd): subprocess.run(cmd, shell=True, check=True)

def gen_key(p):
    if p.exists(): return
    run(f'ssh-keygen -t ed25519 -f {p} -N ""')

def add_agent(p):
    run('eval "$(ssh-agent -s)"')
    run(f'ssh-add {p}')

def show_pub(p): print(p.with_suffix('.pub').read_text())

def main():
    p = Path.home()/'.ssh/id_ed25519'
    gen_key(p)
    add_agent(p)
    show_pub(p)

if __name__=='__main__': main()
