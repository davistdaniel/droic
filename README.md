
# droic

<div align="center">
  <img src="./assets/droic_logo.svg" alt="kurup logo" width="200"/>
  <br/>
  <br/>
  
  ![License](https://img.shields.io/badge/license-MIT-blue.svg)
  ![Version](https://img.shields.io/badge/version-0.1b0-orange.svg)
  ![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
  
  *Monitoring dashboard for android device metrics*
</div>

**Droic** is a Python application that interfaces with Android devices via **ADB** (USB or Wi-Fi) to extract and visualize real-time system metrics like **CPU usage, memory**, and **tasks data**. Built with **Dash** and **Plotly**, it offers a UI and **local SQLite database** logging for historical insights.

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
- **ADB (Android device Bridge) must installed and added to your system's PATH**
  - Installation of ADB varies according to your operating system. Please follow instructions which apply to you operating system.
  - For droic to work, the command `adb` should work.
  - This can be checked easily by executing in a terminal:
      ```bash
      adb --version
      adb devices
      ```
    These should print the ADB version and list connected devices (or start the daemon if not running).
- **Android device(s) with USB debugging enabled.** 
  - For enabling USB-debugging, you would likely have to first enable Developer options on your device.
  - Depending on your device model, this may vary. Please follow instructions specific to your device model.
- **Initially, device must be connected via USB.** 
  - Once the USB status shows in droic, you can try connecting via Wi-Fi by clicking on the Wi-Fi Connect button.
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

## Supported metrics



## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome!

---

## 📄 License
Copyright (c) 2025 Davis Thomas Daniel

This project is licensed under the [MIT LICENSE](./LICENSE).
