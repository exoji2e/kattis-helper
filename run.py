#!/usr/bin/env python3
import argparse
import subprocess
import glob
import time

PYTHON_ENV = 'pypy3'

ext2cmd = {
    'py' : lambda fName: [PYTHON_ENV, fName],
    'java' : lambda fName: ['java', split_ext(fName)[0]],
    'cpp' : lambda fName: ['./' + split_ext(fName)[0]],
    'out' : lambda fName: ['./' + fName]
}

def run(cmd, inp):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(inp.encode('ascii'))
    out, _ = p.communicate()
    r = p.returncode
    return r, out.decode('ascii')

def compare_token(a, b):
    if a == b: return True, 0
    try:
        aF = float(a)
        bF = float(b)
        return True, abs(aF - bF)
    except:
        return False, False


def compare(out, ans):
    out = out.strip()
    ans = ans.strip()
    if out == ans:
        return True, 0
    maxDiff = 0
    A, B = out.split(), ans.split()
    if len(A) != len(B): return False, 0
    for a, b in zip(A, B):
        ok, diff = compare_token(a, b)
        if not ok:
            return False, 0
        maxDiff = max(maxDiff, diff)
    return maxDiff < 1e-5, maxDiff


def process(cmd, inp, ans, name):
    t0 = time.time()
    r, out = run(cmd, inp)
    out = out.strip()
    ans = ans.strip()
    dt = time.time() - t0
    if r != 0:
        print('[RTE] {:.2f}s {}'.format(dt, name))
        if out:
            print('stdout:')
            print(out)
        exit(r)

    ok, diff = compare(out, ans)
    if ok:
        if diff == 0:
            print('[AC] {:.2f}s {}'.format(dt, name))
        else:
            import math
            err = int(math.log(diff, 10))
            print('[AC] {:.2f}s {} - maxdiff: 1e{}'.format(dt, name, err))
    else:
        print('[WA] {:.2f}s {}'.format(dt, name))
        print('[EXPECTED]:')
        print(ans)
        print('---------')
        print('[GOT]:')
        print(out)
        print('---------')


def compile(file):
    pass

def get_args():
    usage = """
p3 run.py -d data/H H.py
p3 run.py -d data/H -c 'pypy3 H.py'"""
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('file', default=None, help='source file to run (or command if -c is specified.)')
    parser.add_argument('--python_name', required=False, default='pypy3')
    parser.add_argument('-d', '--sample_dir', required=True, help='directory with in/ans-files')
    parser.add_argument('-r', '--recursive', required=False, action='store_true', help='look for in/ans files in subdirectories as well')
    parser.add_argument('-c', '--command', required=False, action='store_true', help='interpret file argument as command')
    args = parser.parse_args()
    args.sample_dir = args.sample_dir.rstrip('/')
    PYTHON_ENV = args.python_name
    return args

def strip_in(in_file):
    assert in_file[-3:] == '.in', 'in file {} does not end with .in'.format(in_file)
    return in_file[:-3]

def split_ext(fName):
    ext = fName.split('.')[-1]
    pre = fName.replace('.' + ext, '')
    return pre, ext


def get_run_command(fName, command):
    if command: return fName.split()
    _, ext = split_ext(fName)
    if ext not in ext2cmd:
        print('extension {} not supported: {}'.format(ext, fName))
        exit(1)
    return ext2cmd[ext](fName)
    

def main():
    args = get_args()
    run_cmd = get_run_command(args.file, args.command)
    in_files = sorted(glob.glob(args.sample_dir + '/*.in'))
    if args.recursive:
        in_files = sorted(in_files + glob.glob(args.sample_dir + '/**/*.in'))
    for in_file in in_files:
        inp = open(in_file).read()
        ans = open(strip_in(in_file) + '.ans').read()
        process(run_cmd, inp, ans, in_file)
        
if __name__ == '__main__':
    main()
