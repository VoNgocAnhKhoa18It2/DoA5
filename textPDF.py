import pdfplumber
with pdfplumber.open(r'C:\Users\Administrator\Desktop\Dao-Huynh-Nghia-Cv.pdf') as pdf:
    first_page = pdf.pages[0]
    rows = []
    arr = first_page.extract_text().split("\n")
    for i in arr:
        if len(i) > 1:
            if "•" in i:
                i = i.replace("•","")
            rows.append(i.strip())
    print(rows)