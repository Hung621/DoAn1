from bs4 import BeautifulSoup
import requests ,lxml,os
# writing infomation on dict
def DictToJsonFile(dct, file):
    result ='{'
    for key, item in dct.items():
        if key == "requirements":
            result +='"requirements":['
            for i in range(len(item)):
                if i == len(item)-1:
                    result += '"{}"'.format(item[i])
                else:
                    result +='"{}",'.format(item[i])
            result += ']'
        elif key == "quantity":
            if type(item) == int :
                result += '"{}":{},'.format(key,item)
            else:
                result +='"{}":"{}",'.format(key,item)
        else:
            result +='"{}":"{}",'.format(key,item)
    else:
        result +='}\n'
    file.write(result)
count=0
company="Satori"
salary=None
time=None
vacancy=None
requirements=None
workplace=None
time_post=None
path = "/home/vlu1/CrawledData/satoricompany.vn"
os.chdir(path)
file=open("/home/vlu1/CrawledData/recruitments.json","a",encoding="utf-8")
for fi in os.listdir():#browse the list in file 
    file_name =open( path + "/" + fi,encoding="utf-8")
    
    soup= BeautifulSoup(file_name,features ="lxml")
    con=soup.find("article",id="entry-recruitment")
    
    vacancy=soup.find("h2",class_="font-bold single-recruitment-title")
    if vacancy!=None: #scraper data and assigned to the dict    
        vacancy=soup.find("h2",class_="font-bold single-recruitment-title").text.strip() 
        require=con.text[con.text.index("Các yêu cầu cần có"):].strip()
        require=require.split("\n")
        require.remove(require[0])
        require.remove(require[0])
        requirements=require
             
                                  
        for l in soup.find_all('p'):
            if 'Nơi làm việc' in l.text:
                workpl=l.text
                workpl=workpl[workpl.index(":")+1 :]
                workplace=workpl.strip().replace("N","n")
            if 'lương' in l.text:
                sa=l.text
                sa=sa[sa.index(":")+1 :]
                salary=sa.strip()
        th=soup.find_all('th',class_="number")
        quantity=int(th[count].text)
        dt=soup.find_all('th',class_="date")
        time=dt[count].text
        info = {
            "Company_name": "SATORI",
            "time_post": time_post,
            "time_deadline": time,
            "vacancy" : vacancy +"-" + workplace,
            "quantity" : quantity,
            "salary":salary,        
            "requirements" : requirements
        }
        count+=1
        print(info)
        DictToJsonFile(info, file)
        
file.close()
