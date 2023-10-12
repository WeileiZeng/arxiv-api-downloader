import urllib, urllib.request
import html_to_json
import json
import requests
import os
import util

dry_run=True
dry_run=False



import argparse

parser = argparse.ArgumentParser(description='Hardworking arXiv downloader.')
parser.add_argument('--start', type=int, help='an integer',default=0)
args = parser.parse_args()
#print(args.start)
#exit()


#print(args.accumulate(args.integers))


html_string = """<head>
    <title>Test site</title>
    <meta charset="UTF-8"></head>"""
output_json = html_to_json.convert(html_string)


def get_pdf_link(links):
    for link in links:
        try:
            if link['_attributes']['title'] =='pdf':
                pdfURL=link['_attributes']['href']
                return pdfURL
        except:
            continue

def get_list(url, index=0):
#    url = 'http://export.arxiv.org/api/query?search_query=all:quantum&start=0&max_results=5'
    data = urllib.request.urlopen(url)
    s=data.read()#.decode('utf-8')
    output_json = html_to_json.convert(s)

#    print(output_json['feed'][0])
    try:
        entries  = output_json['feed'][0]['entry']
    except: #no entry from this search
        return
    for entry in entries:
        process(entry, index:=index+1)

def process(entry, index=0):
    x=entry
    print(index,'----------------',x['id'][0]['_value'],'-------------')
    print('title:',x['title'][0]['_value'].replace('\n',''))
    pdfURL = get_pdf_link(x['link'])
    print('downloading pdfURL:',pdfURL, end=' ')

    a=pdfURL.split('/')[-2:]
    if a[0]=='pdf':
        file_pdf = 'pdf/'+a[1]+'.pdf'
    else:
        file_pdf = 'pdf/'+a[0]+'.'+a[1]+'.pdf'
    print('saving to ',file_pdf)
    if os.path.isfile(file_pdf):
        print(file_pdf,'already exist')        
    elif not dry_run:
        util.download(pdfURL,file_pdf)
#    for k in x:
#        break
#        print(k,':')
#        print(x[k])


def main():
    for i in range(100):
#        start=i*10+200
        start=i*10 + args.start        
#        print('index:',start)
        url = f'http://export.arxiv.org/api/query?search_query=all:quantum&start={start}'
        get_list(url, index=start)

main()
