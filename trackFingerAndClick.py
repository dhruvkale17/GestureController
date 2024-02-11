import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mphands = mp.solutions.hands

cap = cv2.VideoCapture(0)
hands = mphands.Hands()

while True:
    data, image = cap.read()
    
    #Flipping it
    image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)

    #Storing results
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Resize the image
    new_width = int(1920/2)
    new_height = int(1080/2)
    resized_img = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    if results.multi_hand_landmarks:
        #print(results.multi_hand_landmarks[0])
        for hand_landmarks in results.multi_hand_landmarks:
            #print(hand_landmarks)
            #mp_drawing.draw_landmarks(
            #    image,
            #    hand_landmarks[0,1,2])
            index_x = int(hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].x * new_width)
            index_y = int(hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].y * new_height)
            thumb_x = int(hand_landmarks.landmark[mphands.HandLandmark.THUMB_TIP].x * new_width)
            thumb_y = int(hand_landmarks.landmark[mphands.HandLandmark.THUMB_TIP].y * new_height)
            cv2.circle(resized_img, (index_x,index_y), 5, (0, 0, 255), -1)
            cv2.circle(resized_img, (thumb_x,thumb_y), 5, (0, 0, 255), -1)
            
            #print(f'Finger tip coordinates: (',
            #f'{int(hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].x * new_width)}, '
            #f'{int(hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].y * new_height)})'
            #)
            pyautogui.moveTo(index_x*2, index_y*2, duration = 0.1)

            if index_x-2 < thumb_x < index_x+3 and index_y-2 < thumb_y < index_y+3:
                print(f"CLICK: {index_x}, {index_y}.....{thumb_x}, {thumb_y}")
                pyautogui.click()
    cv2.imshow('HandTracker', resized_img)
    cv2.waitKey(1)

