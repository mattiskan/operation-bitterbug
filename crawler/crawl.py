#! /usr/bin/python3
import bs4
import urllib.request
import pickle
import os.path
import re
import threading

def parse_posts(link):
    url = "%s%s" % ("http://www.familjeliv.se", link)

    post_data = parse_post(url)

    if post_data:
        write_post(post_data, url)    

def parse_post(url):
    if url in visited:
        return False
    
    try:
        webpage = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(webpage.read().decode('utf8'))
    except UnicodeDecodeError:
        visited.add(url)
        print("failed", url)
        return False

    return " ".join([ anchor.getText()
             for anchor in soup.find_all('div', 'message-body') ])


def write_post(post_data, url):
    filename = "posts/%s" % url.split("/")[-1]

    with open(filename, 'w') as output:
        output.write(tokenize(post_data))

    visited.add(url)
    print("added", url)

def tokenize(data):
    data = data.replace("\n", " ").lower()

    data = data.replace("-", " ")
    data = data.replace("(", "")
    data = data.replace(")", "")    
    
    data = re.split('[.-:;?!]+', data)

    sent = [ sent.split(" ") for sent in data ]

    ret = []
    for words in sent:
        next = [ word for word in words if check(word)]
        if next:
            ret += [ next ]

    return repr(ret)

def check(word):
    return word and word != '-'

forum_prefix="http://www.familjeliv.se/forum"
def parse_forum_page(fid, sidnummer):
    try:
        url = "%s/%d/latest/%d" % (forum_prefix, fid, sidnummer)
        webpage = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(webpage.read().decode('utf8'))

        links = soup.find(id="forum-threadlist")

        return [ link.find('a').get('href')
                 for link in links.find_all('td', 'thread') ]
    except:
        pass
    
    return [ 'anything' ]
        
def parse_forum(fid):
    pagenum = 1
    links = parse_forum_page(fid, 1)

    while (links != []):
        page = "pagenum %d %d" % (fid, pagenum)

        if page in visited:
            pagenum += 1
            continue


        while threading.active_count() > 120:
            print("sleeping")
            time.sleep(1)
            print("done sleeping")

        [ threading.Thread(target=parse_posts, args=(link,) ).start()
          for link in links ]

        visited.add(page)
        pagenum += 1
        links = parse_forum_page(fid, pagenum)


visited_file = "visited.data"

def write_visited():
    with open(visited_file, 'wb') as output:
        pickle.dump(visited, output)
        
def read_visited():
    if not os.path.isfile(visited_file):
        return set()
    
    with open(visited_file, 'rb') as data:
        return pickle.load(data)
        

if __name__ == "__main__":
    visited = read_visited()
    
    try:
        parse_forum(4)
    except KeyboardInterrupt:
        pass
    finally:
        print("wrote visited")
        write_visited()
