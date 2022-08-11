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
		# elif key == "workplace":
		# 	result += '"workplace":['
		# 	for i in range(len(item)):
		# 		if i == len(item)-1:
		# 			result += '"{}"'.format(item[i])
		# 		else:
		# 			result += '"{}",'.format(item[i])
		# 	result += '],'
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
path = "/home/vlu1/CrawledData/jobsgo.vn"
os.chdir(path)
for x in os.listdir():
	file_name = path + "/" + x
	try:	
		soup = BeautifulSoup(open(file_name, encoding='utf-8'), features = "lxml")
		page = soup.find("div", class_="panel-body").text
		if "Yêu cầu công việc" in page:
			vacancy = page.split("Thời hạn")[0].split("Hết hạn")[0].strip(" ")
			# time_deadline = page[page.index("Thời hạn") : page.index("Mức lương")].split("Thời hạn")[1].strip(" ")
			salary = page[page.index("Mức lương") : page.index("Ứng tuyển ngay")].split("Mức lương")[1].strip(" ")
			workplace = page[page.index("Địa điểm làm việc") : page.index("Ngành nghề")].split("Địa điểm làm việc")[1].strip(" ").split("➢ ")[1]
			requirements = page[page.index("Yêu cầu công việc ") : page.index("Quyền lợi được hưởng")].split("Yêu cầu công việc ")[1].split("\n")[1:]

			tu_dien = {
				# "company_code": 16,
				"company_name": "Công Ty Cổ Phần Hóa Mỹ Phẩm Mỹ Hảo",
				"time_post": None,
				"time_deadline": None,
				"vacancy": vacancy +"-"+ workplace,
				"quantity": None,
				"salary" : salary,
				"requirements": requirements
			}
			DictToJsonFile(tu_dien,des)
	except:
		continue
	
