# 🖐️ Hand Gesture LED Controller

A real-time computer vision and hardware integration project that tracks hand gestures via webcam to control physical LEDs on an Arduino. This project features a custom-built, dark-mode graphical interface overlaid on the webcam feed, complete with a neon-pink hand skeleton and interactive finger-state indicators.

---

## 1. Circuit Diagram 

Thumb LED: Connect Arduino Pin 2 $\rightarrow$ Resistor $\rightarrow$ LED Long Leg (+). Connect LED Short Leg (-) to GND.Index LED: Connect Arduino Pin 3 $\rightarrow$ Resistor $\rightarrow$ LED Long Leg (+). Connect LED Short Leg (-) to GND.Middle LED: Connect Arduino Pin 4 $\rightarrow$ Resistor $\rightarrow$ LED Long Leg (+). Connect LED Short Leg (-) to GND.Ring LED: Connect Arduino Pin 5 $\rightarrow$ Resistor $\rightarrow$ LED Long Leg (+). Connect LED Short Leg (-) to GND.Pinky LED: Connect Arduino Pin 6 $\rightarrow$ Resistor $\rightarrow$ LED Long Leg (+). Connect LED Short Leg (-) to GND.

## 1. Arduino Setup

1. Open the Arduino IDE.
2. Copy and paste your C++ code into a new sketch.
3. Connect your Arduino (UNO, Nano, Mega, or compatible) to your computer via USB.
4. Build your circuit by connecting 5 LEDs and 5 Resistors (220Ω – 330Ω) to Digital Pins 2, 3, 4, 5, and 6. Connect all LED cathodes to Ground.
5. Select the correct Board and Port from the Tools menu.
6. Click **Upload**.
7. **Important:** Close the Serial Monitor in the Arduino IDE so the Python script can access the port later.

---

## 2. Python Setup

1. Open your terminal or command prompt and install the required libraries:

   ```bash
   pip install opencv-python mediapipe cvzone pyserial numpy
   ```

2. Open `hand_tracker.py` in your preferred code editor (like VS Code).

3. Update the Arduino port in the code to match your active connection (e.g., `COM3` for Windows):

   ```python
   ARDUINO_PORT = 'COM3'
   BAUD_RATE = 9600
   ```

4. Run the script:

   ```bash
   python hand_tracker.py
   ```

---

## 3. Controls

- Hold your hand up to the webcam to see the custom interface track your gestures.
- Make gestures like **1**, **2**, **3**, **4**, **"FIST"**, or **"OPEN HAND"** to instantly mirror your physical finger states to the LEDs on your breadboard.
- Press `q` on your keyboard while the webcam window is active to quit the application safely and release the camera.

---

### Developer

Made by **Ibrahim** | Code Error
