from CellDetectionImage import CellDetectionImage
import cv2
import numpy as np
from GUI import GUI

def mostra(img, name='Name'):
    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    for i in range(10):
        path = 'Images/' + str(i+1) + '.jpg'

        im0 = cv2.imread(path)

        im1 = CellDetectionImage(im0)

        cv2.imwrite('final'+str(i)+'.png', im1)
    #GUI()
"""""
    im0 = cv2.imread('Images/3.jpg')
    #im0 = cv2.imread('im_gray.png', 3)
    #im0 = cv2.imread('im_gray.png', 0)

    imResp = CellDetectionImage(im0)

    cv2.imwrite("final3.png", imResp)

"""""





