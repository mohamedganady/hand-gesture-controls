<!-- =========================
     Hand Gesture Controls README
     Interactive + All-in-one
========================= -->

# 🖐 Hand Gesture Controls (Mouse & Volume)  
Control your **mouse cursor, clicks, and system volume** using **hand gestures** from your webcam.  
Built with **Python + OpenCV + MediaPipe Tasks** and optimized for **macOS**.

> ✅ Touchless HCI (Human–Computer Interaction) demo: gestures → real mouse + volume actions.

---

## 🔗 Quick Navigation (Interactive)
- [✨ Demo & Features](#-demo--features)
- [🧩 Requirements](#-requirements)
- [⚡ Installation](#-installation)
- [▶️ Run](#️-run)
- [🖐 Gesture Guide](#-gesture-guide)
- [📁 Project Files](#-project-files)
- [🛠 Troubleshooting](#-troubleshooting)
- [🧠 How It Works](#-how-it-works)
- [🗺 Roadmap](#-roadmap)
- [👨‍💻 Author](#-author)
- [📝 License](#-license)

---

## ✨ Demo & Features
✅ What you can do:
- 🖱 **Move mouse** with your **index finger**
- 👆 **Click** using a **pinch** gesture
- 🔊 **Adjust volume** using **thumb ↔ index distance**
- 📊 Show **volume bar** on screen
- ✋ **Open hand** → enable volume control
- ✊ **Closed hand** → disable volume control
- 🧭 **Smooth cursor movement** for stability

<details>
<summary><b>💡 Tip: Best environment for accuracy (click to expand)</b></summary>

- Use good lighting
- Keep hand inside the camera frame
- Avoid very fast movements at the start
- Use a plain background if possible
</details>

---

## 🧩 Requirements
- Python **3.10+** (recommended: **3.11**)
- Webcam (built-in or external)
- macOS recommended (volume control uses AppleScript)

---

## ⚡ Installation

### 1) Clone the repository
```bash
git clone https://github.com/mohamedganady/hand-gesture-controls.git
cd hand-gesture-controls

### 2) Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate


###  3) Install dependencies
pip install -r requirements.txt


### ▶️ Run
python main.py
