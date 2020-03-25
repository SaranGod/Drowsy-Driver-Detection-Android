from imutils import face_utils
import dlib
import cv2
import math
p = "Path to .dat file"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)
count=0
inear1l=[]
inear2l=[]
inmorl=[]
inmor=0
mor=0
innlr=0
innlrl=[]
nlr=0
drowsycount=0
inear1=0
inear2=0
inear=0
inmar=0
ear1=0
ear2=0
flag=[]
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    # Getting out image by webcam 
    _, image = cap.read()
    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Get faces into webcam's image
    rects = detector(gray, 0)
    # For each detected face, find the landmark.
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
        # Draw on our image, all the finded cordinate points (x,y) 
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        if(count<300):
            inear1l.append((math.hypot(shape[41][0] - shape[37][0], shape[41][1] - shape[37][1])+math.hypot(shape[40][0] - shape[38][0], shape[40][1] - shape[38][1]))/(2*math.hypot(shape[39][0] - shape[36][0], shape[39][1] - shape[36][1])))
            inear2l.append((math.hypot(shape[47][0] - shape[43][0], shape[47][1] - shape[43][1])+math.hypot(shape[46][0] - shape[44][0], shape[46][1] - shape[44][1]))/(2*math.hypot(shape[45][0] - shape[42][0], shape[45][1] - shape[42][1])))
            inmorl.append((math.hypot(shape[50][0] - shape[58][0], shape[50][1] - shape[58][1])+math.hypot(shape[51][0] - shape[57][0], shape[51][1] - shape[57][1])+math.hypot(shape[52][0] - shape[56][0], shape[52][1] - shape[56][1]))/(3*math.hypot(shape[48][0] - shape[54][0], shape[48][1] - shape[54][1])))
            innlrl.append(math.hypot(shape[27][0] - shape[30][0], shape[27][1] - shape[30][1]))
            cv2.putText(image, str(count), (0,200), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
            if count==299:
                inear1l.sort()
                inear2l.sort()
                inmorl.sort()
                inear1=sum(inear1l[150:])/150
                inear2=sum(inear2l[150:])/150
                inmor=sum(inmorl[:150])/150
                innlr=sum(innlrl)/300
                inear=(inear1+inear2)/2
                print('Initial Setup Complete!')
                print(inear)
                print(inmor)
                print(innlr)
            count+=1
        else:
            ear1=(math.hypot(shape[41][0] - shape[37][0], shape[41][1] - shape[37][1])+math.hypot(shape[40][0] - shape[38][0], shape[40][1] - shape[38][1]))/(2*math.hypot(shape[39][0] - shape[36][0], shape[39][1] - shape[36][1]))
            ear2=(math.hypot(shape[47][0] - shape[43][0], shape[47][1] - shape[43][1])+math.hypot(shape[46][0] - shape[44][0], shape[46][1] - shape[44][1]))/(2*math.hypot(shape[45][0] - shape[42][0], shape[45][1] - shape[42][1]))
            mor=(math.hypot(shape[50][0] - shape[58][0], shape[50][1] - shape[58][1])+math.hypot(shape[51][0] - shape[57][0], shape[51][1] - shape[57][1])+math.hypot(shape[52][0] - shape[56][0], shape[52][1] - shape[56][1]))/(3*math.hypot(shape[48][0] - shape[54][0], shape[48][1] - shape[54][1]))
            ear=(ear1+ear2)/2
            nlr=math.hypot(shape[27][0] - shape[30][0], shape[27][1] - shape[30][1])/innlr
            if(inear-ear>0.03):
                drowsycount+=1
            if(mor-inmor>0.3):
                drowsycount+=1
            if(nlr<0.3 or nlr>1.1):
                drowsycount+=1
            cv2.putText(image, str(nlr), (0,50), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
            if(drowsycount>6):
                cv2.putText(image, str(drowsycount), (0,200), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
            if(drowsycount>200):
                cv2.putText(image, 'WAKE UP!!!!', (0,500), font, 3, (0, 255, 0), 2, cv2.LINE_AA)

    
    # Show the image
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if (k == 99 or k == 67):
        drowsycount=0
    if k == 27:
        print(inear)
        break
cv2.destroyAllWindows()
cap.release()