# 🖐 Hand Gesture Controls (Mouse & Volume)

Control your **mouse cursor, clicks, and system volume** using **hand gestures** captured from your webcam.  
Built with **Python, OpenCV, and MediaPipe Tasks**. Optimized for **macOS**.

---

## 📖 Project Description
This project enables touchless control of your **mouse (cursor movement and clicks)** and **system volume** using real-time **hand gestures**.  
It leverages computer vision to detect hand landmarks and translate them into actual operating system actions.

---

## 🧩 Requirements
- **Python 3.10+** (recommended: **3.11**)  
- **Webcam** (built-in or external)  
- **macOS recommended** (volume control via AppleScript)  
- **Git**

---

## 🔽 Clone
```bash
git clone https://github.com/mohamedganady/hand-gesture-controls.git
cd hand-gesture-controls
```

---

## 🧪 Create & Activate Virtual Environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Run
```bash
python main.py
```
- Press **ESC** to exit.  
- On the first run, the MediaPipe hand model will be downloaded automatically if it is not already present.

---

## 🖐 Gesture Guide
| Gesture | Action |
|--------|--------|
| Move index finger | Move mouse cursor |
| Pinch (index + middle) | Click |
| Open hand ✋ | Enable volume control |
| Closed hand ✊ | Disable volume control |
| Thumb ↔ Index distance | Increase / Decrease volume |

---

## 📁 Project Structure
```
hand-gesture-controls/
├─ main.py               # Full system: mouse + click + volume + on-screen UI
├─ mouse_cursor.py      # Cursor movement logic
├─ clickUsingPinch.py   # Pinch-click gesture testing
├─ count.py             # Finger counting experiments
├─ test.py              # MediaPipe / environment checks
├─ requirements.txt     # Project dependencies
└─ README.md            # Documentation
```

---

## 🧠 How It Works
1) **Capture** video frames using OpenCV  
2) **Detect** hand landmarks using MediaPipe Tasks  
3) **Map** landmarks to:
   - Cursor position (index fingertip)
   - Click action (pinch gesture)
   - Volume level (thumb–index distance)  
4) **Smooth and apply** actions while rendering a live UI overlay

---

## 🛠 Troubleshooting

**Camera not working / black screen**
- Close other apps using the camera (Zoom, Teams, browsers)
- Try another camera index in code:
```python
cap = cv2.VideoCapture(1)
```
- Restart the terminal

**Volume does not change on macOS**
```bash
osascript -e 'set volume output volume 50'
```
If this does not change the volume, check macOS automation permissions.

**Cursor is shaking or too sensitive**
- Increase smoothing values in `main.py`
- Improve lighting conditions
- Keep your hand centered and steady

---

## 🧪 Use-Cases
- Touchless control for presentations  
- Accessibility tools  
- HCI / Computer Vision demonstrations  
- Robotics & AI education  
- Smart workspaces  

---

## 🗺 Roadmap
- Windows support using `pycaw`  
- Left / Right click gestures  
- Calibration & sensitivity UI  
- Multi-hand support  
- Custom gesture mapping  

---

## 🙏 Acknowledgements
- Google **MediaPipe**  
- **OpenCV** community  
- Python open-source ecosystem  

---

## 👨‍💻 Author
**Mohamed Ganady**  
Robotics & AI Instructor | Embedded Systems Developer  
GitHub: https://github.com/mohamedganady  

---

## 📝 License
MIT License — free to use and modify with attribution.
