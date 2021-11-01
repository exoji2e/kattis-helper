from urllib.request import Request, urlopen
from zipfile import ZipFile
from io import BytesIO
import os

def get_samples_url(problem_url):
    return problem_url.rstrip('/') + '/file/statement/samples.zip'

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


def fetch_sample_zip(problem_url, file_name):
    url = get_samples_url(problem_url)
    resp = retriveUrl(url)
    
    with open(file_name, 'wb') as f:
        f.write(resp)


def unpack_samples(zipName, destDir):
    with open(zipName, 'rb') as f:
        data = f.read()
        with ZipFile(BytesIO(data)) as z:
            z.extractall(destDir)