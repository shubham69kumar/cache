from django.shortcuts import render, HttpResponseRedirect
import socket
import time

ipAdd = ["107.108.11.123", "107.109.123.255"]
URL = ["www.samsung.com", "www.samsung.net"]


def cache(request):
    return render(request,'DNS_CACHE.html')


def getIndex(c):
    return 26 if c == '.' else (ord(c) - ord('a'))


def getCharFromIndex(i):
    return '.' if i == 10 else ('0' + i)


class trieNode:
    def __init__(self):
        self.isLeaf = None
        self.URL = None
        self.child = [None] * 27


def newTrieNode():
    newNode = trieNode()
    newNode.isLeaf = False
    newNode.URL = None
    for i in range(11):
        newNode.child[i] = None
    return newNode


def insert(root, ipAdd, URL):
    l = len(ipAdd)
    pCrawl = root
    for level in range(l):
        index = getIndex(ipAdd[level])
        if pCrawl.child[index] is None:
            pCrawl.child[index] = newTrieNode()

        pCrawl = pCrawl.child[index]

    pCrawl.isLeaf = True
    pCrawl.URL = ''
    pCrawl.URL = URL


# print(pCrawl.URL)


def searchDNSCache(root, ipAdd):
    pCrawl = root
    l = len(ipAdd)

    for level in range(l):
        index = getIndex(ipAdd[level])
        if pCrawl.child[index] is None:
            return None

        pCrawl = pCrawl.child[index]

    if (pCrawl and pCrawl.isLeaf):
        return pCrawl.URL

    return None

def find(url):
    n = len(URL)
    root = newTrieNode()
    data = []

    for i in range(n):
        insert(root, URL[i], ipAdd[i])

    start_time = time.time()
    res_url = searchDNSCache(root, url)
    end_time=start_time-time.time()
    if res_url != None:
        data.append("url stored in cache is")
        data.append(res_url)
        data.append(end_time)
        data.append(url)
        print("url stored in cache", res_url)
        print("time taken to get the ip from cache:")
        print(end_time)

    else:
        try:
            url_time=time.time()
            ip = socket.gethostbyname(url)
            end_url_time=url_time-time.time()
            data.append('url not in cache')
            data.append(ip)
            data.append(abs(end_url_time))
            print("url not in cache")
            print("ip address:" + ip)
            print("time taken to get the ip which was not in cache:")
            print(abs(end_url_time))
            ipAdd.append(ip)
            URL.append(url)
            insert(root, url, ip)
            data.append(url)
        except:
            data.append("Enter a valid url")
            data.append('1')
    return data

def search(request):
    urll= request.POST['search']
    out=find(urll)
    
    return render(request,'DNS_CACHE.html',{'output':out})
