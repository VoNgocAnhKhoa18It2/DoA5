from tkinter import *
from tkinter import filedialog
import numpy as np
import cv2
import pytesseract
from PIL import Image, ImageTk
from tkPDFViewer import tkPDFViewer as pdf
import pdfplumber
import re
from tkinter import messagebox

pytesseract.pytesseract.tesseract_cmd = r"E:\\SOFTWARE\\Tesseract-OCR\\tesseract.exe"

path = ""
lg = "vie"
arrPDF = []

root = Tk()  # create root windows

root.title("GUI")  # title of the GUI window
# root.geometry("1400x600")
width = root.winfo_screenwidth()
height = root.winfo_screenheight() - 100
# setting tkinter window size
root.geometry("%dx%d" % (width, height))
root.config(bg="skyblue")  # specify background color

center = Frame(root, bg="skyblue", pady=10)
center.pack(fill=BOTH, expand=True, side=TOP)

panelPDF = Frame(center, bg="skyblue")
panelPDF.pack(side=LEFT, padx=10)

lblText = Label(center, fg='#000', bg="skyblue")
lblText.pack(side=RIGHT, padx=(0, 10))


def openFile():
    fln = filedialog.askopenfilename()
    return fln


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


def selectPDF():
    url = openFile()
    if (len(url) == 0):
        return

    clear_frame(panelPDF)
    pdf.ShowPdf().img_object_li.clear()
    v2 = pdf.ShowPdf().pdf_view(panelPDF, pdf_location=f'{url}', width=80)
    v2.pack()

    global arrPDF
    if arrPDF:
        arrPDF.clear()

    with pdfplumber.open(url) as pdfs:
        first_page = pdfs.pages[0]
        arr = first_page.extract_text().split("\n")
        for i in arr:
            if len(i) > 1:
                if "[•]" in i:
                    i = i.replace("•", "")
                arrPDF.append(i.strip())


def selectIMG():
    url = openFile()
    if (len(url) == 0):
        return

    global path
    path = url
    img = cv2.imread(url)
    img = cv2.resize(img, (int((center.winfo_width() + 10) / 2), height), fx=2, fy=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = ImageTk.PhotoImage(image=Image.fromarray(img))
    lblText.configure(image=image)
    lblText.image = image


def tienxuly(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgAdaptiveThre = cv2.adaptiveThreshold(gray, 255, 1, 1, 7, 2)
    imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
    imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 1)
    return imgAdaptiveThre


def adjust_gamma(image):
    invGamma = 1.0 / 0.5
    table = []
    for i in range(256):
        table.append(((i / 255.0) ** invGamma) * 255)
    table = np.array(table).astype("uint8")
    image = cv2.LUT(image, table)
    return image


def Average(lst):
    return sum(lst) / len(lst)


special_characters = r"[~\!@#\$%\^&\*\(\)_\+{}\":;'.,\[\]]"


def soKhop(StringPDF, string):
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

def Message(title,message):
   messagebox.showinfo(title, message)

def scanImg():
    global path,height
    img = cv2.imread(path)
    a = adjust_gamma(img)
    config = r'--psm 3'
    boxes = pytesseract.image_to_data(a, config=config, lang=lg)
    potision = -1
    count = 0
    check = True
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                if int(b[5]) == 1:
                    potision = potision + 1
                checkC = soKhop(arrPDF[potision], checkChatacter(b[11]).strip())
                if checkC == False:
                    check = False
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 1)
                    count = count +1

    img = cv2.resize(img, (int((center.winfo_width() + 10) / 2), height), fx=2, fy=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = ImageTk.PhotoImage(image=Image.fromarray(img))
    lblText.configure(image=image)
    lblText.image = image

    if check is True:
        Message("Thông Báo", "Trùng Khớp")
    else:
        Message("Thông Báo","Không Trung Khớp \n Số ký tự không trùng khớp: {}".format(count))
    # lblText.configure(text=row)


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Select File PDF", command=selectPDF)
filemenu.add_command(label="Select IMG", command=selectIMG)
filemenu.add_command(label="Scan IMG", command=scanImg)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.update()
root.mainloop()
