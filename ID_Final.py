from PIL import Image
import pytesseract
import time
import cv2
import os
import re
import pandas as pd
df=pd.DataFrame()
pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Python37/Tesseract-OCR/tesseract.exe"
#r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
#"C:/Program Files/Python37/Tesseract-OCR/tesseract.exe"
attendance=[]
def img_capture():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Place your ID card.")
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,10)

    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        cv2.imshow("Place your ID card.", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            print("Attendance list:\n",attendance)
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            #time.sleep(0.5)
            print("{} written!".format(img_name))
            img_counter += 1
        
            a=pytesseract.image_to_string(Image.open(img_name), lang="eng")
            #time.sleep(1)
            print(a)
            print("\n")
      
            #time.sleep(0.5)
            b=re.findall('[0-9][0-9][A-Z].*[0-9]',a)
        
            print(b)
            if(len(b)==0):
                print("Try Again \n1*******************************\n*******************************")
             
            elif(len(b[0])==9):
                #if(b[0][0]!='1'):
                #print("Try Again \n2*******************************\n*******************************")    
                
            #else:
                if(b[0][0]=='4'):
                    b[0]='1'+b[0][1:]
                for i in range(2,5):
                    if(b[0][i]=='1'):
                        b[0]=b[0][0:i]+'I'+b[0][i+1:]
                    if(b[0][i]=='8'):
                        b[0]=b[0][0:i]+'B'+b[0][i+1:]
                    if(b[0][i]=='i'):
                        b[0]=b[0][0:i]+'I'+b[0][i+1:]
                
                reg=b[0]
            
                print("Final Reg. number: ",reg)        
                if(attendance.count(reg)==0):
                    attendance.append(reg)
             
            else:
                print("Try Again \n3*******************************\n*******************************")        
            print("*****************************************\n*****************************************")
            os.remove(img_name)
    cam.release()

    cv2.destroyAllWindows()
    sr_num=[i for i in range(1,len(attendance)+1)]
    df['Serial Number']=sr_num
    df['Registration Number']=attendance
    df.to_excel('attendance.xlsx',index=False)

while(True):
    img_capture()


