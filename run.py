import urllib, urllib.request
import html_to_json
import json
import requests
import os
import util

dry_run=True
dry_run=False

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

def get_list(url):
#    url = 'http://export.arxiv.org/api/query?search_query=all:quantum&start=0&max_results=5'
    data = urllib.request.urlopen(url)
    s=data.read()#.decode('utf-8')
    output_json = html_to_json.convert(s)

#    print(output_json['feed'][0])
    entries  = output_json['feed'][0]['entry']
    for entry in entries:
        process(entry)

def process(entry):
    x=entry
    print('----------------',x['id'][0]['_value'],'-------------')
    print('title:',x['title'][0]['_value'].replace('\n',''))
#    print('id:',x['id'][0]['_value'])
#    print('link:',x['link'])
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
#        response = requests.get(pdfURL)
#        open(file_pdf, "wb").write(response.content)
#    x=x['link'][2]['_attributes']
    for k in x:
        break
        print(k,':')
#        break
        print(x[k])


def main():
    for i in range(100):
        start=i*10+0
        url = f'http://export.arxiv.org/api/query?search_query=all:quantum&start={start}'
        get_list(url)

main()
