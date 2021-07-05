import cv2
import numpy, math
import scipy.fftpack as fftim
from PIL import Image
import scipy.misc

b = cv2.imread(r'C:\Users\Administrator\Desktop\GiaoTrinh\Khoa-VoNgocAnh-18IT075-lab 4\hoa.jpg')

b = cv2.resize(b,(400,400),fx=1,fy=1)
b = cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)

M = b.shape[0]
N = b.shape[1]

def Ideal_Lowpass(d_0):
    H = numpy.ones((M, N))
    center1 = M / 2
    center2 = N / 2

    for i in range(1, M):
        for j in range(1, N):
            r1 = (i - center1) ** 2 + (j - center2) ** 2
            r = math.sqrt(r1)
            if r > d_0:
                H[i, j] = 0.0
    k = Image.fromarray(H)
    print(k)
    con = b * k
    e = abs(fftim.ifft2(con))
    return e,H

def do(_=None):
    d0 = cv2.getTrackbarPos('d0', filter_win)
    flag = cv2.getTrackbarPos('flag', filter_win)
    n = cv2.getTrackbarPos('n', filter_win)
    lh = cv2.getTrackbarPos('lh', filter_win)
    img = None
    if(lh == 0):
        if (flag == 0):
            img,H = Ideal_Lowpass(d0)
        pass
    else:
        pass
    cv2.imshow("INPUT", b)
    cv2.imshow("OUTPUT",img)
    cv2.imshow("H", H)


filter_win = 'Filter Parameters'
cv2.namedWindow(filter_win)
rows, cols = b.shape[:2]
cv2.createTrackbar('d0', filter_win, 20, int(min(rows, cols) / 4),do)
cv2.createTrackbar('flag', filter_win, 0, 2,do)
cv2.createTrackbar('n', filter_win, 1, 5,do)
cv2.createTrackbar('lh', filter_win, 0, 1,do)
cv2.resizeWindow(filter_win, 512, 20)
do()
cv2.waitKey(0)
cv2.destroyAllWindows()
