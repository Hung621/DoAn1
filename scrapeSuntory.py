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
path = "/home/vlu1/CrawledData/nhanlucnganhluat.vn"
os.chdir(path)
for x in os.listdir():
	file_name = path + "/" + x
	soup = BeautifulSoup(open(file_name, encoding='utf-8'), features = "lxml")
	for pg1 in soup.find_all("div", class_="td-view text-center"):
		page1 = pg1.text
		if "Đã hết hạn" in page1:
			salary = page1.split("\n Đã hết hạn")[0].split("Hồ Chí Minh")[1].strip("\n")
			# time_deadline = page1.split("Nộp đơn")[0].strip("\n").split("Hồ Chí Minh")[1].split("\n")[4]
	for pg2 in soup.find_all("div", id="thongtinchitiet"):
		page2 = pg2.text
		if "Nơi làm việc" in page2:
			workplace = page2.split("Nơi làm việc")[1].split("Cấp bậc")[0].strip("\n")
			time_post = page2.split("Ngày đăng tuyển")[1].split("Nơi làm việc")[0].strip("\n")
			vacancy = page2.split("Cấp bậc")[1].split("Kỹ năng")[0].split("Ngành nghề")[0].strip("\n")
			indSt = page2.index("Yêu cầu công việc")
			indEnd = page2.index("Phúc lợi công việc")
			requirements = page2[indSt : indEnd].split("Yêu cầu công việc")[1].strip("\n").split("\n")

			tu_dien = {
				# "company_code": 15,
				"company_name": "Suntory PepsiCo Vietnam Beverage",
				"time_post": time_post,
				"time_deadline": None,
				"vacancy": vacancy + "-" + workplace,
				"quantity": None,
				"salary" : salary,
				"requirements": requirements
			}
			DictToJsonFile(tu_dien,des)
