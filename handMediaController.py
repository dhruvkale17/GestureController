from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import pyautogui

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    wrist_x = 0
    wrist_y = 0
    pauseTimer = 0

    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image,1)
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #print(f'old: ',{wrist_x}, {wrist_y})
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
                
                #print(f'new: ',{wrist_x} ,{wrist_y})
        
        if results.multi_handedness:
            for idx, hand_handedness in enumerate(results.multi_handedness):
                handedness_dict = MessageToDict(hand_handedness)
                if handedness_dict["classification"][0]['label'] == "Right":
                    currentVolume = volume.GetMasterVolumeLevel()
                    if wrist_x < int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * 100):
                        if currentVolume <= -1:
                            volume.SetMasterVolumeLevel(currentVolume+1, None)
                            print(f"increasing volume",{wrist_x},{int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * 100)})

                    if wrist_x > int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * 100):
                        if currentVolume >= -62:
                            volume.SetMasterVolumeLevel(currentVolume-1, None)
                            print(f"decreasing volume",{wrist_x}, {int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * 100)})
                    
                    wrist_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * 100)
                    
                    #if wrist_y < int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * 100)
                
                if handedness_dict["classification"][0]['label'] == "Left":
                    pauseTimer += 1
                    if pauseTimer == 60:
                        pyautogui.typewrite(['space'])
                        pauseTimer = 0


        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()

   