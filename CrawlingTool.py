import requests, lxml, os, re, subprocess
from bs4 import BeautifulSoup
    
def HaveNextPage(soup):
    nextPage = None
    if soup.find("a", title="Trang sau") != None:
        nextPage =soup.find("a", title="Trang sau")
    else :
        nextPage = soup.find("a", title="Go to next page")
    if nextPage == None:
        return False
    return nextPage["href"]

def GetLink(url, lstLinks, urls):
    HomePage = url[ : url.index("/", len("https://"))]

    # Reuqest to the page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    # Check if page has next one
    if HaveNextPage(soup) != False:
        urls.append(HomePage+"/"+HaveNextPage(soup))
    # Get all the link in the a tag
    for a in soup.find_all("a"):
        try:
            link = a["href"]
            if "http" not in link:
                if link.startswith("/"):
                    link = HomePage + link
                else:
                    link = HomePage + "/" + link
            if (link not in lstLinks) and (HomePage in link):
                lstLinks.append(link)
        except KeyError:
            continue

def DownLoadLink(lstLinks):
    ind = 0
    for link in lstLinks:
        try:
            if not link.endswith("/"):
                file_name = link[link.rindex("/") + 1: ]
                Folder = link[link.index("://")+3: link.index("/", link.index("://")+3)]
                SourceFolder = "C:/Users/dell/Downloads/CrawledData/"
                os.chdir(SourceFolder)
                if Folder not in os.listdir():
                    os.mkdir(Folder)
                SourceFolder += Folder
                if "." not in file_name:
                    file_name += ".txt"
                file_name = file_name.replace("-", "")
                if not file_name.isalpha():
                    file_name = "file_name_" + str(ind) + ".txt"
                    ind += 1
                
                try:
                    print(link, SourceFolder+"/"+file_name)
                    subprocess.check_output('curl "%s">>%s'%(link, SourceFolder+"/"+file_name), shell=True)
                except:
                    file_name = "/file_name"+str(ind)+".txt"
                    print(link, SourceFolder+file_name)
                    subprocess.check_output('curl "%s">>%s'%(link, SourceFolder+file_name), shell=True)
            else:
                continue
        except ValueError:
            continue

urls = [
    "https://docs.scrapy.org/en/latest/topics/items.html"
]
lstLinks = []
count = 0
while count <len(urls):
    GetLink(urls[count], lstLinks, urls)
    count += 1
DownLoadLink(lstLinks)
