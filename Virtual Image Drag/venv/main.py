import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

class DragImg:
    def __init__(self, path, posOrigin, imgType):
        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8, maxHands= 10)

    path = r"D:\Thi giac may tinh\Virtual Image Drag\ImagesPNG"
    myList = os.listdir(path)
    print(myList)

    listImg = []
    for x, pathImg in enumerate(myList):
        imgType = 'png' if 'png' in pathImg else 'jpg'
        listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 300, 50], imgType))

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            for hand in hands:
                lmList = hand['lmList']
                cursor = lmList[8]
                length = detector.findDistance(lmList[8][0:2], lmList[12][0:2], color = "0,255,255")
                print(length)
                if length[0] < 30:
                    for imgObject in listImg:
                        imgObject.update(cursor)

        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()
