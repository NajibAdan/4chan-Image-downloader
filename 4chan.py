import json
import wget
import requests
import os
import re
import threading
import time
class myThread (threading.Thread):
   def __init__(self, threadID, name,url):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.url = url
   def run(self):
      print "Starting " + self.name + '\n'
      threadLock.acquire()
      checking(self.url)
      print "Exiting " + self.name + '\n'
      threadLock.release()
#checks if the filepath exists, if not it creates the file path
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
def checking(url):
    treads = "boards.4chan.org/[a-zA-Z0-9]*?/thread/\d*"
    matchObj = re.search(treads,url,re.M|re.I)
    if matchObj:
        url = 'http://'+matchObj.group()
        result = requests.get(url+'.json')
        r = json.loads(result.content)
        splitt = url.split('/')
        board = splitt[3]
        thread_number = splitt[5]
        for i in r['posts']:
            if 'tim' in i:
                download(i['tim'],i['ext'],board,thread_number)
                print '\n'
    else:
        print 'no match'

def download(tim,ext,board,thread):
    link = 'https://i.4cdn.org/'+board+'/' + str(tim) +ext
    filepath = board+'\\'+thread+'\\'
    ensure_dir(filepath)
    #checks if the file exists to avoid overwriting and wasting bandwidth
    if (not os.path.isfile(filepath+str(tim)+ext)):
        wget.download(link, filepath+str(tim)+ext)

threadLock = threading.Lock()
urllist = []
threadID = 1
threadlist = []
while 1:
    response = raw_input('Enter 4chan thread url or Enter q to exit inputting: ')
    if response == 'q':
        break
    else:
        urllist.append(response)

for url in urllist:
    thread = myThread(threadID,'thread-'+str(threadID),url)
    threadlist.append(thread)
    thread.start()
    threadID += 1

for t in threadlist:
    t.join
    
print '\nExiting main thread'
