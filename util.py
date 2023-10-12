import requests
from tqdm import tqdm
import os

def download(url: str, fname: str, chunk_size=1024): #1024 for 1kB
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    tmp_file='tmp.pdf'
    with open(tmp_file, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

    os.system(f'mv {tmp_file} {fname}')
            
def test():
    url = 'http://arxiv.org/pdf/q-alg/9508008v1'
    fname='q-alg.9508008v1.pdf'
    download(url,fname)
if __name__=="__main__":
    test()
