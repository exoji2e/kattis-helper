import argparse, os
import sample_tool

def get_args():
    usages = """
python3 fetcher.py -u https://open.kattis.com/problems/froshweek
"""
    parser = argparse.ArgumentParser(usage=usages)
    parser.add_argument('-u', '--url', required=True, help='url for kattis problem to fetch')
    parser.add_argument('-o', '--outdir', default='', help='directory to put problem data in')
    args = parser.parse_args()
    args.outdir = args.outdir.rstrip('/')
    return args

def main(args):
    problem_name = sample_tool.get_problem_name(args.url)
    target = args.outdir
    if not target:
        target = problem_name
    os.makedirs(target, exist_ok=True)
    zip_path = f'{target}/{problem_name}.zip'
    data_dst = f'{target}/data'
    sample_tool.fetch_data(args.url, data_dst, zip_path, rm_zip=True)
    open(f'{target}/{problem_name}.py', 'w').write(f'# {problem_name}\n\n')




if __name__ == '__main__':
    args = get_args()
    main(args)