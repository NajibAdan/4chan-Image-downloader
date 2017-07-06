import json
import wget
import requests
import os
import re
#checks if the filepath exists, if not it creates the file path
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def download(tim,ext,board,thread):
    link = 'https://i.4cdn.org/'+board+'/' + str(tim) +ext
    filepath = board+'\\'+thread+'\\'
    ensure_dir(filepath)
    #checks if the file exists to avoid overwriting and wasting bandwidth
    if (not os.path.isfile(filepath+str(tim)+ext)):
        wget.download(link, filepath+str(tim)+ext)

url = raw_input('Enter 4chan thread url: ')
thread = "boards.4chan.org/[a-zA-Z0-9]*?/thread/\d*"

matchObj = re.search(thread,url,re.M|re.I)
if matchObj:
    url = 'http://'+matchObj.group()
else:
    print 'no match'
result = requests.get(url+'.json')
r = json.loads(result.content)
splitt = url.split('/')
board = splitt[3]
thread_number = splitt[5]

#getting the board name from the link
for i in r['posts']:
    if 'tim' in i:
        download(i['tim'],i['ext'],board,thread_number)
