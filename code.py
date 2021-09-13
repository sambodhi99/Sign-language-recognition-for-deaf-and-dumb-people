#importing ovencv
import cv2
#importing mediapipe of google
import mediapipe as mp

mp_hands= mp.solutions.hands
hands= mp_hands.Hands()
mp_draw= mp.solutions.drawing_utils

#storing fingertips in an array
finger_tips=[8,12,16,20]
thumb_tip=4

#capturing video frames from webcam
cap=cv2.VideoCapture(0)

while True:
    #declaring variables
    ret, img=cap.read()
    h,w,c=img.shape
    #flip image from video
    img = cv2.flip(img, 1)
    results= hands.process(img)
    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list=[]
            for id, lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)
            finger_fold_status=[]
            #to circle tips of fingers with blue
            for tip in finger_tips:
                x,y= int(lm_list[tip].x*w),int(lm_list[tip].y*h)
                #print(id,":",x,y)
                cv2.circle(img, (x,y),15,(255,0,0), cv2.FILLED )

                #to check if finger is folded or not
                if lm_list[tip].x < lm_list[tip - 3].x:
                    cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)
            print(finger_fold_status)
            #print if finger is folded or not
            #for printing hellow
            if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x:
                if all(finger_fold_status):


                    print("Hellow")
                    cv2.putText(img, "HELLOW", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            #for printing call me
            if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x:
                if any(finger_fold_status):

                    print("CALL ME")
                    cv2.putText(img, "CALL ME", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    print("Hellow")
                    cv2.putText(img, "HELLOW", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


            #for printing yes
            if lm_list[thumb_tip].y< lm_list[thumb_tip-1].y < lm_list[thumb_tip-2].y:
                if all(finger_fold_status):
                    print("YES")
                    cv2.putText(img, "YES", (20,30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

            #for printing no
            if lm_list[thumb_tip].y> lm_list[thumb_tip-1].y > lm_list[thumb_tip-2].y:
                if all(finger_fold_status):
                    print("NO")
                    cv2.putText(img, "NO", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            mp_draw.draw_landmarks(img,hand_landmark, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", img)
    cv2.waitKey(1)
