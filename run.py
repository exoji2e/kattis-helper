#!/usr/bin/pypy3
import argparse
import subprocess
import glob
import time

def run(cmd, inp):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(inp.encode('ascii'))
    out, _ = p.communicate()
    return out.decode('ascii')

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
    for a, b in zip(out.split(), ans.split()):
        ok, diff = compare_token(a, b)
        if not ok:
            return False, 0
        maxDiff = max(maxDiff, diff)
    return maxDiff < 1e-5, maxDiff


        

def process(cmd, inp, ans, name):
    t0 = time.time()
    out = run(cmd, inp)
    dt = time.time() - t0
    ok, diff = compare(out, ans)
    out = out.strip()
    ans = ans.strip()
    if ok:
        if diff == 0:
            print('[OK] {} time: {:.2f}'.format(name, dt))
        else:
            print('[OK - maxdiff: {}] {} time: {:.2f}'.format(diff, name, dt))
    else:
        print('[FAIL] {} time: {:.2f}'.format(name, dt))
        print('[EXPECTED]:')
        print(ans)
        print('---------')
        print('[GOT]:')
        print(out)
        print('---------')


def compile(file):
    pass

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='source file to run')
    parser.add_argument('--python_name', default='pypy3')
    parser.add_argument('-d', '--sample_dir')
    parser.add_argument('-c', '--command')
    args = parser.parse_args()
    args.sample_dir = args.sample_dir.rstrip('/')
    assert args.file or args.command
    return args

def get_ans_file(in_file):
    return in_file[:-3] + '.ans'

def main():
    args = get_args()
    fName = args.file
    assert '.py' == fName[-3:]
    in_files = glob.glob(args.sample_dir + '/*.in')
    for in_file in in_files:
        inp = open(in_file).read()
        ans = open(get_ans_file(in_file)).read()
        process([args.python_name, args.file], inp, ans, in_file)
        
if __name__ == '__main__':
    main()
