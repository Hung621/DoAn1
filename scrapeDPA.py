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
path = "/home/vlu1/CrawledData/www.dap.vn"
os.chdir(path)
for x in os.listdir():
	file_name = path + "/" + x
	soup = BeautifulSoup(open(file_name, encoding='utf-8'), features = "lxml")
	for data in soup.find_all("div", class_="page-recruiment page-recruiment-detail-public"):
		page = data.text
		page1 = data.text.lower()
		vacancy = page.split("Hạn nộp hồ sơ:")[0].strip("\n").split("TUYỂN DỤNG ")[1].split(" TẠI HÀ NỘI")[0]
		time_deadline = page1[page1.index("hạn nộp hồ sơ:") : page1.index("mô tả công việc")].split("hạn nộp hồ sơ:")[1].strip(" ").split("\n")[0]
		if "Yêu cầu" in page:
			requirements = page[page.index("Yêu cầu") : page.index("Quyền lợi")].split("Yêu cầu")[1].split("\n")[3:-3]
		if "YÊU CẦU" in page:
			requirements = page[page.index("YÊU CẦU") : page.index("III.QUYỀN LỢI")].split("YÊU CẦU")[1].strip("\n").rstrip("\xa0 \n\n\xa0\xa0\xa0\xa0\xa0 ").split("\n")
		if "thu nhập" in page1:
			salary = page1[page1.index("thu nhập") : page1.index("triệu")].split("thu nhập")[1].strip(": ")
		
		tu_dien = {
			# "company_code": 19,
			"company_name": "Dược phẩm Đông Á",
			"time_post": None,
			"time_deadline": time_deadline,
			"vacancy": vacancy + ", " + "Hà Nội",
			"quantity": None,
			"salary" : salary,
			"requirements": requirements
		}
		DictToJsonFile(tu_dien,des)
