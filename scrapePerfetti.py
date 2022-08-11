import os, lxml
from bs4 import BeautifulSoup

def DictToJsonFile(dct, file):
	result = '{'
	for key, item in dct.items():
		if key == "requirements":
			result += '"requirements":['
			for i in range(len(item)):
				if i == len(item)-1:
					result += '"{}"'.format(item[i])
				else:
					result += '"{}",'.format(item[i])
			result += ']'
		elif key == "quantity":
			if type(item) == int:
				result += '"{}":{},'.format(key, item)
			else:
				result += '"{}":"{}",'.format(key, item)
		else:
			result += '"{}":"{}",'.format(key, item)
	result +='}\n'
	file.write(result)

des = open("/home/vlu1/CrawledData/recruitments.json", "a", encoding = "utf-8")
path = "/home/vlu1/CrawledData/www.jobstreet.vn"
os.chdir(path)
for x in os.listdir():
	file_name = path + "/" + x
	soup = BeautifulSoup(open(file_name, encoding='utf-8'), features = "lxml")
	for p in soup.find_all("div", id="job-description-container"):
		if "Địa điểm làm việc" in p.text:
			data = p.text
			workplace = data.split(":")[2].split("\n\n")[0]
			vacancy = data.split("Chức vụ:")[1].split(":")[0].split("\n")[0]
			salary = data.split("Mức lương: ")[1].split(")")[0]
			indSt = data.index("Yêu cầu")
			indEnd = data.index("Ngành nghề")
			require = data[indSt : indEnd].split("\n")
			for item in require:
				if "•" in item:
					require = item.split("•")[1:]
				elif "-" in item:
					require = item.split("-")[1:]
				elif ". " in item:
					require = item.split(". ")[1:]
			tu_dien = {
				# "company_code": 14,
				"company_name": "Perfetti Van Melle (Việt Nam) Limited",
				"time_post": None,
				"time_deadline": None,
				"vacancy": vacancy + workplace,
				"quantity": None,
				"salary" : salary,
				"requirements": require
			}
			DictToJsonFile(tu_dien,des)
