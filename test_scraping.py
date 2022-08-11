from bs4 import BeautifulSoup
import lxml, json, os, re

def CheckTitle(title):
    if title == None: return False
    if ("tuyển" in title.text.lower()) and ("dụng" in title.text.lower()): return True
    if("recruitment" in title.text.lower()): return True
    else: return False

def CheckVacancy(string):
    pattern = "(Vị trí).*:(.+)"
    if re.match(pattern, string.text):
        result = string.text.strip()
        return result[result.index(":")+1 : ]

def CheckDate(date):
    patterns = ["(.*) ../../....", "(.*) ../../..", "(.*) ..../../.."]
    for pattern in patterns:
        if re.fullmatch(pattern, date):
            date = date[date.rindex(" ") : ]
            return date

def DictToJsonFile(dct, file):
    result = '{"time":"%s", "vacancy":"%s", "quantity":%d, "workplace":"%s", "requirements":['%(dct["time"], dct["vacancy"], dct["quantity"], dct["workplace"])
    if len(dct["requirements"]) >0:
        for i in range(len(dct["requirements"])):
            if i == len(dct["requirements"])-1:
                result += ' "%s"]}\n'%(dct["requirements"][i])
            else: 
                result += '"%s",'%(dct["requirements"][i])
    else:
        result +=']}\n'
    file.write(result)

# Open json file to write in
DesFile = open("D:/DHG.json", "a", encoding="utf-8")
# Get list of files
SourceFolder = "D:/DA_DMS/DHG"
os.chdir(SourceFolder)
ListFile = os.listdir()

for item in ListFile:
    SourceFile = SourceFolder + "/" + item
    file = open(SourceFile, encoding="utf-8")
    soup = BeautifulSoup(file, features="lxml")
    title = soup.find("title")
    print(file.name)
    if CheckTitle(title):
        # Get the published date
        TimePublished = soup.find("time", itemprop="datePublished")["datetime"]
        time = TimePublished[ : TimePublished.index("T")]+"-"
        time_end = ""

        lstVacancy = []
        lstQuantity = []
        lstWorkplace = []
        table = soup.find("table")
        for p in table.find_all("p"):
            if CheckVacancy(p) !=None:
                lstVacancy.append(CheckVacancy(p))
            if p.text.find("tại")>=0:
                lstWorkplace.append(p.text[p.text.index("tại") : ])
            try:
                lstQuantity.append(int(p.text))
            except ValueError:
                if re.match("Số lượng: [0-9][0-9]", p.text):
                    quan = p.text.strip()
                    lstQuantity.append(int(quan[quan.rindex(" ")+1 : ]))
                if re.match("[0-9][0-9] .*", p.text):
                    quan = p.text.strip()
                    lstQuantity.append(int(quan[ : quan.index(" ")]))
                else:
                    continue

        for p in soup.find_all("p"):
            if p.text.find("Thời gian nộp")>=0:
                time_end = p.text[p.text.rindex(" ")+1: ]
                time += time_end
        if time_end == "":
            for li in soup.find_all("li"):
                if li.text.find("Thời gian nộp")>=0:
                    time_end = li.text[li.text.rindex(" ")+1: ]
                    time += time_end

        file.seek(0)
        data = file.read()
        # Getting requirments
        counter = 0
        ind_st = 0
        ind_end = 0
        lstStartInd = []
        lstEndInd = []
        while counter < len(lstVacancy):
            if counter == 0:
                ind_st = data.index("Trình độ")
                ind_end = data.index("Mô tả công việc")
                lstStartInd.append(ind_st)
                lstEndInd.append(ind_end)
                counter +=1
            else:
                ind_st = data.index("Trình độ", ind_st + 1)
                ind_end = data.index("Mô tả công việc", ind_end + 1)
                lstStartInd.append(ind_st)
                lstEndInd.append(ind_end)
                counter += 1
        checker = True
        while checker:
            if len(lstQuantity) < len(lstVacancy):
                lstQuantity.append("N/A")
            elif len(lstWorkplace) < len(lstVacancy):
                lstWorkplace.append("N/A")
            else:
                checker = False
        for i in range(len(lstVacancy)):
            require = data[lstStartInd[i] : lstEndInd[i]]
            ind_st = 0
            ind_end = 0
            while True:
                try:
                    ind_st = require.index("<")
                    ind_end = require.index(">") + 1
                    subString = require[ind_st : ind_end]
                    require = require.replace(subString, "")
                    if ind_end == len(require)-1 :
                        break
                except ValueError :
                    break
            require = require.replace("\t", "")
            require = require.split("\n")
            while True:
                try:
                    require.remove("")
                except ValueError:
                    break
            require.remove(require[0])
            try:
                require.remove("&nbsp;")
            except:
                print("Alert")
            requirements = []
            for a in range(len(require)):
                requirements.append(require[a])
            info = {
                "time": time,
                "vacancy" : lstVacancy[i],
                "quantity" : lstQuantity[i],
                "requirements" : requirements,
                "workplace" : lstWorkplace[i]
            }
            DictToJsonFile(info, DesFile)
DesFile.close()