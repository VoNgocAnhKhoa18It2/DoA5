import cv2
import pytesseract
from PIL import Image


img = cv2.imread("Screenshot 2021-04-03 205412.png")
boxes = pytesseract.image_to_data(img)
text = []
row = ""
for x,b in enumerate(boxes.splitlines()):
    if x!=0:
        b = b.split()
        if len(b) == 12:
            # if int(b[5]) == 1:
            #     text.append(row)
            #     row = ""
            print(b)
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.rectangle(img, (x, y), (x+w, y + h), (50, 50, 255), 1)
            row = row + b[11]+" "

rows = []
data = (pytesseract.image_to_string(Image.open('Screenshot 2021-04-03 205412.png')))
t = data.split('\n')
for i in t:
	rows.append(i)
s = ''
print(s.join(rows))
cv2.imshow("Result", img)

cv2.waitKey()
cv2.destroyAllWindows()



