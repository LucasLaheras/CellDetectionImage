import cv2

def CellDetectionImage(im0):

    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    im1 = [im1],[0],None,[256],[0,256]

    for i in im1:
        print(str(i) + ' ')

    return

"""
def psrGrayHistogram(im):

    [Lin, Col] = size(im)
    H = zeros(1,256)
    for y=1:Lin
        for x=1:Col
          H(im(y,x)+1) = H(im(y,x)+1) + 1
        end
    end
    % normalization
    H = H/(sum(H))
    return H

"""