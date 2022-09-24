from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
import os

def get_problem_name(problem_url):
    return problem_url.rstrip('/').split('/')[-1]

def fetch_data(p_url, dst, zipPath, rm_zip=False):
    if not os.path.exists(zipPath):
        fetch_sample_zip(p_url, zipPath)
    unpack_samples(zipPath, dst)
    if rm_zip:
        os.remove(zipPath)

def retriveUrl(url):
    req = Request(
        str(url),
        headers={"user-agent": "firefox"},
    )
    with urlopen(req) as r:
        return r.read()

def get(url, CACHE_DIR):
    fname = convert_url_to_file(url, CACHE_DIR)
    if os.path.exists(fname):
        return open(fname).read()
    else:
        r = requests.get(str(url))
        open(fname,'w').write(r.text)
        return r.text

def convert_url_to_file(url, CACHE_DIR):
    url = url.replace('https://','').replace('http://', '').replace('/','_') + '.html'
    return CACHE_DIR / url

def getBaseUrl(URL):
    return URL.split('kattis.com')[0] + 'kattis.com'

def get_samples_url(problem_url, CACHE_DIR):
    problemPage = get(problem_url, CACHE_DIR)
    soup = BeautifulSoup(problemPage, 'html.parser')
    dl = soup.find(class_='attribute_list-downloads')
    if dl:
        a = dl.find('a')
        if a:
            return getBaseUrl(problem_url) + a.get('href')
    return None

def fetch_sample_zip(problem_url, file_name, CACHE_DIR):
    url = get_samples_url(problem_url, CACHE_DIR)
    if url:
        resp = retriveUrl(url)
        
        with open(file_name, 'wb') as f:
            f.write(resp)
    else:
        print(f'WARN: couldnt find samples for: {problem_url}')
        exit(1)


def unpack_samples(zipName, destDir):
    with open(zipName, 'rb') as f:
        data = f.read()
        with ZipFile(BytesIO(data)) as z:
            z.extractall(destDir)