import json
import wget
import requests
import os

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
result = requests.get(url+'.json')
r = json.loads(result.content)
board = url[25:27]
thread = url[-7:]
#for boards like diy,r9k
if '/' in board:
    board = board.replace('/','')
print "Downloading images from "+url
for i in r['posts']:
    download(i['tim'],i['ext'],board,thread)
