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
                SourceFolder = "D:/DA_DMS/" + Folder
                os.chdir("D:/DA_DMS/")
                if Folder not in os.listdir():
                    os.mkdir(SourceFolder)
                
                if "." not in file_name:
                    file_name += ".txt"
                file_name = file_name.replace("-", "")
                if not file_name.isalpha():
                    file_name = "file_name" + str(ind) + ".txt"
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
    "https://sgfoods.com.vn/vi/news-categories/tuyen-dung",
    "https://www.traphaco.com.vn/vi/tuyen-dung.html",
    "https://uni-president.com.vn/?page_id=925",
    "http://vinapharm.com.vn/index.php/listnews/72/1/Tuyen-dung.html",
    "https://www.dhgpharma.com.vn/vi/tuyen-dung/tin-tuyen-dung"
]
lstLinks = []
count = 0
while count <len(urls):
    GetLink(urls[count], lstLinks, urls)
    count += 1
DownLoadLink(lstLinks)