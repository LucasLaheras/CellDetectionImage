from CellDetectionImage import CellDetectionImage
import cv2

if __name__ == '__main__':

    path = 'Images/1.jpg'

    im0 = cv2.imread(path)

    CellDetectionImage(im0)
