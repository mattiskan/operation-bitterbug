#! /usr/bin/python3
import bs4
import urllib.request
import pickle
import os.path


VISITED = 0
FAILED = 1

def parse_posts(link):
    url = "%s%s" % ("http://www.familjeliv.se", link)
    print(url)
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
        print("fail")
        return FAILED

    return [ anchor.getText()
             for anchor in soup.find_all('div', 'message-body') ]


def write_post(post_data, url):
    filename = "posts/%s" % url.split("/")[-1]

    with open(filename, 'w') as output:
        output.write('[')
        output.write(",".join(post_data).replace("\n", " "))
        output.write(']')

    visited.add(url)
    print("added", url)

forum_prefix="http://www.familjeliv.se/forum"
def parse_forum_page(fid, sidnummer):
    url = "%s/%d/latest/%d" % (forum_prefix, fid, sidnummer)
    webpage = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(webpage.read().decode('utf8'))

    links = soup.find(id="forum-threadlist")

    return [ link.find('a').get('href')
             for link in links.find_all('td', 'thread') ]

def parse_forum(fid):
    pagenum = 1
    links = parse_forum_page(fid, 1)

    while (links != []):

        [ parse_posts(link) for link in links ]
        [ parse_posts(link) for link in links ]
        
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
        parse_forum(1)
    finally:
        print("wrote")
        write_visited()

    write_visited()
