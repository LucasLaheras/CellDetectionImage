import SwarmPackagePy
from CellDetectionImage import CellDetectionImage
import cv2

for i in range(1,11):
    path = str(i) +'.jpg'

    im0 = cv2.imread(path)

    CellDetectionImage(im0)

    """""
    cv2.namedWindow(path, cv2.WINDOW_NORMAL) 
    cv2.imshow(path, im0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



SwarmPackagePy.fa()
"""
