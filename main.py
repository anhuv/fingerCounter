import cv2
import time
import os
import hand_tracking_module as htm


cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


path="finger"
myList=os.listdir(path)
overlayList=[]

for impath in myList:
    image=cv2.imread(f'{path}/{impath}')
    overlayList.append(image)
pTime=0

detector=htm.handDetector(detectionCon=0.75) # lây kết quả độ chính xác từ 75% trở lên
tipIds=[4,8,12,16,20] #id các đầu ngón cái, trỏ, giữa, áp út và út
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False) #kết quả thu được bởi tracking, thu toạn độ x, y của các điểm trên bàn tay
    #print(lmList)
    if len(lmList) !=0:
        fingers=[]

        # Ngón cái check xem tay phai hay trai, và xem trạng thái có được giơ lên không
        if lmList[tipIds[0]][1] > lmList[tipIds[4]][1]:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)
        

        for id in range(1,5):  #y axis ngon tay con lai
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers=fingers.count(1)
        #print(fingers)


        h,w,c=overlayList[totalFingers].shape
        #img[0:h,0:w]=overlayList[totalFingers]
        img[480-h:480,640-w:640]=overlayList[totalFingers] #đưa ảnh ra màn hình thuộc foder finger ra màn hình

        cv2.rectangle(img,(20,225),(170,425),(255,255,0),cv2.FILLED) #vẽ hình chữ nhật
        cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25) #viết kết quả là số đếm

    cTime=time.time() #lấy thời gian hiện tại
    fps=1/(cTime-pTime) # số khung hình
    pTime=cTime  #lưu thời gian quá khứ

    cv2.putText(img,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
    cv2.imshow("Image",img)
    cv2.waitKey(1)