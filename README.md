
# droic

<div style="float: right; margin-left: 10px; vertical-align: middle;">
  <img src="./assets/droic_logo.svg" alt="Droic Logo" width="150" />
</div>

**Droic** is a cross-platform Python application that interfaces with Android devices via **ADB** (USB or Wi-Fi) to extract and visualize real-time system metrics like **CPU usage, memory**, and **tasks data**. Built with **Dash** and **Plotly**, it offers a UI and **local SQLite database** logging for historical insights.

---

## ✨ Features

- 🔍 Auto-detects ADB-connected devices via USB or Wi-Fi
- 📡 One-click ADB-over-WiFi connection from the dashboard
- 📊 Live metric visualization (currently supports CPU, memory, tasks)
- 💾 Local SQLite storage with device metadata and timestamps
- 🛎️ In-app notifications for device events and status
- 🧭 Custom monitoring controls:
  - Interval adjustment
  - Metric selection
  - Toggle saving to DB
- 📈 Live plot (latest 100 points) + persistent historical data
- ⚙️ Built using Python, Dash, Plotly, Pandas

---

## 📸 Screenshot

<div>
  <img src="./assets/droic_screenshot.webp" alt="Droic Logo" width="1000" />
</div>

---

## 🛠️ Getting Started

### ✅ Requirements

- Python 3.11+
- ADB (Android device Bridge) installed and added to your system's PATH
- Android device(s) with USB debugging enabled.
- Initially, device must be connected via USB.
- To enable ADB over Wi-Fi for the first time, manual setup may be needed.


### 📦 Installation

#### Python

```bash
python -m pip install -r requirements.txt
```

### 🚀 Running Droic

```bash
python droic.py
```

Once running, visit: [http://127.0.0.1:8050](http://127.0.0.1:8050)

#### Docker



---

## 🗃️ Data Storage

All collected data is stored in a local `droic.db` SQLite file. It includes:
- Timestamps
- CPU & memory metrics
- Number of active tasks
- Device model and serial number

---

## 💻 Compatibility

✅ Tested on **macOS**  
⚠️ Expected to work on **Windows** and **Linux** (ADB & Python must be configured)

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome!

---

## 📄 License
Copyright (c) 2025 Davis Thomas Daniel

This project is licensed under the [MIT LICENSE](./LICENSE).
