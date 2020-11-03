import requests
from bs4 import BeautifulSoup
import sample_tool
import argparse
import os, time, json
from datetime import datetime
import progressbar 
from pathlib import Path

CACHE_DIR = Path('cache')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', default='https://ncpc19.kattis.com', help='url for kattis competition to fetch')
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('-w', '--wait', default='')
    parser.add_argument('-o', '--outdir', default='.')
    args = parser.parse_args()
    args.wait = get_wait(args.wait)
    args.url = args.url.rstrip('/')
    args.outdir = Path(args.outdir)
    args.cachedir = Path('cache')
    return args

def get(url):
    fname = convert_url_to_file(url)
    if os.path.exists(fname):
        return open(fname).read()
    else:
        r = requests.get(str(url))
        open(fname,'w').write(r.text)
        return r.text
        
def extract_problems(URL):
    html = get(URL + '/problems')
    print('got html')
    soup = BeautifulSoup(html, 'html.parser')
    print('parsed soup')
    problems = {}
    for tr in soup.find_all('tr'):
        if tr.find_all(class_='problem_letter'):
            problems[tr.th.text] =  URL + tr.find('a').get('href')
    with open('problems.json', 'w') as f:
        f.write(json.dumps(problems))
    return problems


def get_wait(wait_str):
    if not wait_str: return None
    v = [int(x) for x in wait_str.split(':')]
    if len(v) == 2:
        v.append(0)
    d = datetime.now()
    return d.replace(d.year, d.month, d.day, v[0], v[1], v[2], 0)


def wait_until(date_time):
    now = datetime.now()
    tE = date_time.timestamp()
    t0 = now.timestamp()
    M = int(tE-t0) + 1
    if M <= 0: return
    widgets=[
        ' [', progressbar.CurrentTime(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]
    print(f'waiting from {now} until {date_time}')
    bar = progressbar.ProgressBar(max_value=int(tE-t0), widgets=widgets)
    while time.time() < tE:
        cT = time.time()
        bar.update(min(M, int(cT - t0)))
        time.sleep(1)
    bar.finish()

def convert_url_to_file(url):
    url = url.replace('https://','').replace('http://', '').replace('/','_') + '.html'
    return CACHE_DIR / url

def get_problem_statement(id):
    problems = json.loads(open('problems.json').read())
    url = problems[id]
    return get(url)

def process_statement(statement):
    soup = BeautifulSoup(statement, 'html.parser')
    pbody = soup.find(class_='problembody')
    return len(str(pbody).replace('\n','')) # len of problem body

def main(args):
    if args.force:
        os.rmdir(CACHE_DIR)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(args.outdir, exist_ok=True)
    if args.wait != None:
        wait_until(args.wait)
    URL = args.url
    r = extract_problems(URL)
    for id, url in r.items():
        zipName = CACHE_DIR / f'{id}.zip'
        if not os.path.exists(zipName):
            sample_tool.fetch_sample_zip(url, zipName)
        sample_tool.unpack_samples(zipName, args.outdir / f'{id}')
        statement = get(url)
        print(id, process_statement(statement), url)
        

if __name__ == '__main__':
    args = get_args()
    main(args)

