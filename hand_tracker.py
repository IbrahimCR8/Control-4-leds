import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time
import numpy as np

# --- CONFIGURATION ---
ARDUINO_PORT = 'COM3'  # Update with your active port
BAUD_RATE = 9600

# Try to connect to Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE)
    time.sleep(2)
    print("Serial connection established.")
except Exception as e:
    print(f"Running without Serial Connection: {e}")
    arduino = None

# Initialize Webcam and Detector
cap = cv2.VideoCapture(1) # Set to 0 or 1 depending on your webcam index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Disable default drawing so we can render our custom UI overlay
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variables for UI metrics
pTime = 0
sent_counter = 0

# UI Colors (BGR format in OpenCV)
BG_COLOR = (25, 22, 25)       # Dark grey/black background
PINK = (255, 50, 200)         # Neon Pink for hand skeleton
GREEN = (0, 255, 0)           # Neon Green for active elements
CYAN = (255, 255, 0)          # Cyan for Sent counter
YELLOW = (0, 255, 255)        # Yellow for Gesture Name
DARK_GREY = (70, 70, 70)      # Inactive state
WHITE = (255, 255, 255)

# Hand landmark connections for drawing the skeleton
connections = [
    (0,1), (1,2), (2,3), (3,4),       # Thumb
    (0,5), (5,6), (6,7), (7,8),       # Index
    (5,9), (9,10), (10,11), (11,12),  # Middle
    (9,13), (13,14), (14,15), (15,16),# Ring
    (13,17), (17,18), (18,19), (19,20),# Pinky
    (0,17)                            # Palm base
]

# Gesture Dictionary
gesture_names = {
    "00000": "FIST",
    "01000": "ONE",
    "01100": "TWO",
    "01110": "THREE",
    "01111": "FOUR",
    "11111": "OPEN HAND"
}
finger_labels = ["THU", "IND", "MID", "RIN", "PIN"]

while True:
    success, img = cap.read()
    if not success:
        break
    
    # Create the main blank canvas (Height: 650, Width: 640)
    canvas = np.zeros((650, 640, 3), dtype=np.uint8)
    canvas[:] = BG_COLOR
    
    # Detect hands directly on the un-flipped frame so MediaPipe accurately calculates thumb direction
    hands, img = detector.findHands(img, draw=False, flipType=False)
    
    gesture_text = "CUSTOM"
    hand_type_text = ""
    fingers = [0, 0, 0, 0, 0]
    
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        
        # Correctly identify hand side
        hand_type_text = hand["type"].upper() + " HAND"
        fingers = detector.fingersUp(hand)
        
        # Build the 5-digit string for serial transmission
        finger_string = f"{fingers[0]}{fingers[1]}{fingers[2]}{fingers[3]}{fingers[4]}"
        gesture_text = gesture_names.get(finger_string, "CUSTOM")
        
        # Send data to Arduino
        if arduino:
            arduino.write((finger_string + '\n').encode())
            sent_counter += 1
            
        # --- CUSTOM HAND DRAWING (Neon Pink Skeleton) ---
        # Draw skeleton lines
        for connection in connections:
            start_idx, end_idx = connection
            if start_idx < len(lmList) and end_idx < len(lmList):
                x1, y1 = lmList[start_idx][0], lmList[start_idx][1]
                x2, y2 = lmList[end_idx][0], lmList[end_idx][1]
                cv2.line(img, (x1, y1), (x2, y2), PINK, 3)
                
        # Draw landmark dots
        for lm in lmList:
            cx, cy = lm[0], lm[1]
            cv2.circle(img, (cx, cy), 6, PINK, cv2.FILLED)
            cv2.circle(img, (cx, cy), 2, WHITE, cv2.FILLED)

    # Place video feed onto canvas
    canvas[50:530, 0:640] = cv2.resize(img, (640, 480))
    
    # --- TOP UI BAR ---
    # FPS Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    
    cv2.putText(canvas, f". FPS  {int(fps)}", (20, 35), cv2.FONT_HERSHEY_DUPLEX, 0.7, GREEN, 2)
    cv2.putText(canvas, hand_type_text, (240, 35), cv2.FONT_HERSHEY_DUPLEX, 0.7, WHITE, 2)
    cv2.putText(canvas, f". SENT  {sent_counter}", (470, 35), cv2.FONT_HERSHEY_DUPLEX, 0.7, CYAN, 2)
    
    # --- BOTTOM UI BAR ---
    # Gesture Name
    text_size = cv2.getTextSize(gesture_text, cv2.FONT_HERSHEY_DUPLEX, 1.2, 2)[0]
    text_x = (640 - text_size[0]) // 2
    cv2.putText(canvas, gesture_text, (text_x, 575), cv2.FONT_HERSHEY_DUPLEX, 1.2, YELLOW, 2)
    
    # Interactive Finger State Boxes
    box_w, box_h = 95, 35
    start_x, spacing = 50, 15
    y_pos = 600
    
    for i, state in enumerate(fingers):
        x = start_x + i * (box_w + spacing)
        color = GREEN if state == 1 else DARK_GREY
        
        # Box Outline
        cv2.rectangle(canvas, (x, y_pos), (x + box_w, y_pos + box_h), color, 2, cv2.LINE_AA)
        # Indicator Dot
        cv2.circle(canvas, (x + 18, y_pos + 18), 5, color, cv2.FILLED)
        # Finger Name
        cv2.putText(canvas, finger_labels[i], (x + 35, y_pos + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Creator Attribution
    cv2.putText(canvas, "Made by Ibrahim", (495, 640), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)

    # Display window
    cv2.imshow("Hand Tracker UI", canvas)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Resource Cleanup
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()