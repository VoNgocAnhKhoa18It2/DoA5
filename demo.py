from PIL import Image,ImageTk
import pdfplumber
import pytesseract
import cv2
import re


special_characters = r"[~\!@#\$%\^&\*\(\)_\+{}\":;'.,\[\]]"
img = cv2.imread('abc.png')

arrPDF = []
with pdfplumber.open(r'C:\Users\Administrator\Desktop\GiaoTrinh\Bảo Mật\BTL_Bảo mật & an toàn hệ thống thông tin.pdf') as pdf:
	first_page = pdf.pages[0]
	arr = first_page.extract_text().split("\n")
	for i in arr:
		if len(i) > 1:

			if "•" in i:
				i = i.replace("•", "")

			if "-" in i:
				i = i.replace("-", "")

			while (True):
				i = i.strip()
				if re.findall(special_characters, i[:1].strip()):
					i = re.sub(special_characters, "", i.strip(), 1)
				else:
					break

			arrPDF.append(i.strip())

rows = []
config = r'--psm 3'
data = (pytesseract.image_to_string(img,config=config,lang='vie'))
t = data.split('\n')
for i in t:
	if len(i) > 2:
		while (True):
			i = i.strip()
			if re.findall(special_characters, i[:1].strip()):
				i = re.sub(special_characters, "", i.strip(),1)
			else:
				break
		rows.append(i.strip())
def soKhop(StringPDF,string):
	if string in StringPDF:
		return True
	else:
		if re.findall(special_characters, string[-2:].strip()):
			string = re.sub(special_characters, "", string.strip(), 1)
			if string in StringPDF:
				return True

	return False

def checkChatacter(i):
	while (True):
		i = i.strip()
		if re.findall(special_characters, i[:1].strip()):
			i = re.sub(special_characters, "", i.strip(), 1)
		else:
			break
	return i

boxes = (pytesseract.image_to_data(img,config=config,lang='vie'))
potision = -1
for x, b in enumerate(boxes.splitlines()):
	if x != 0:
		b = b.split()
		if len(b) == 12:
			if int(b[5]) == 1:
				potision = potision + 1
			check = soKhop(arrPDF[potision],checkChatacter(b[11]).strip())
			if check == False:
				x, y, width, height = int(b[6]),int(b[7]),int(b[8]),int(b[9])
				cv2.rectangle(img, (x, y), (x + width, y + height),(50, 50, 255), 1)
				print(b[11],len(b[11]), "\n",arrPDF[potision].strip())

cv2.imshow("a",img)
cv2.waitKeyEx(0)
