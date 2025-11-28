# 💓 Heart Rate Monitor - Flet GUI Application

A beautiful, modern desktop application for simulating and visualizing heart rate data with real-time monitoring, activity tracking, and session history.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-Latest-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Heart Rate Monitor** is a Python desktop application built with [Flet](https://flet.dev/) that provides a stunning, interactive interface for monitoring and visualizing heart rate data. 

The app simulates realistic heart rate patterns based on different activity types (Resting, Walking, Running, Gym, Swimming) and provides comprehensive statistics, real-time charts, and session history tracking.

Perfect for:
- 🎓 **Educational purposes** - Learn about heart rate monitoring and data visualization
- 🏥 **Health & Fitness** - Track and analyze heart rate patterns
- 💻 **Flet Framework Demo** - Showcase of modern Python UI capabilities
- 📊 **Data Visualization** - Real-time charting and statistics

---

## ✨ Features

- 🎨 **Modern UI Design** - Dark theme with glassmorphic cards and smooth animations
- 📊 **Real-time Chart** - Live heart rate visualization with smooth curves
- 🏃 **Activity Profiles** - Support for 5 activity types with realistic BPM ranges:
  - 🧘 Resting (60-80 BPM)
  - 🚶 Walking (90-110 BPM)
  - 🏃 Running (130-160 BPM)
  - 🏋️ Gym (110-140 BPM)
  - 🏊 Swimming (100-130 BPM)
- 📈 **Statistics Dashboard** - Real-time Min, Max, and Average BPM tracking
- 📝 **Session History** - Save and review past monitoring sessions
- 👤 **User Profiles** - Store personal information (name, age, height, weight, gender)
- 🚨 **Live Alerts** - Real-time notifications for abnormal heart rates
- 💓 **Heartbeat Animation** - Visual pulse indicator synchronized with BPM
- 🎯 **Momentum-based Simulation** - Realistic heart rate fluctuations
- 📱 **Responsive Design** - Adapts to different screen sizes

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** package manager

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/heart-rate-monitor.git
   cd heart-rate-monitor
   ```

2. **Install Flet:**
   ```bash
   pip install flet
   ```

3. **Run the application:**
   ```bash
   python project2.py
   ```

That's it! The app will launch in a new window.

---

## 💻 Usage

### Step-by-Step Guide

#### 1️⃣ **Create Your Profile**

When you first launch the app, you'll see the User Profile screen:

- Enter your **name**
- Enter your **height** (in cm)
- Enter your **weight** (in kg)
- Select your **gender** from the dropdown
- Enter your **age**
- Click **"Continue →"**

#### 2️⃣ **Select an Activity**

Choose from 5 activity types by clicking on a card:

| Activity | Icon | BPM Range | Description |
|----------|------|-----------|-------------|
| 🧘 Resting | Spa | 60-80 | Relaxed, sitting or lying down |
| 🚶 Walking | Walk | 90-110 | Casual walking pace |
| 🏃 Running | Run | 130-160 | Jogging or running |
| 🏋️ Gym | Fitness | 110-140 | Weight training, exercise |
| 🏊 Swimming | Pool | 100-130 | Swimming laps |

- The selected card will **highlight** with a colored border
- The **"📊 Measure BPM"** button will become enabled

#### 3️⃣ **Monitor Your Heart Rate**

Click **"📊 Measure BPM"** to start monitoring:

**Dashboard Layout:**

**Left Sidebar:**
- 👤 **User Profile** - Your personal information
- 🏃 **Current Activity** - Selected activity with color coding
- 📉 **Min BPM** - Lowest recorded heart rate (cyan card)
- 📈 **Max BPM** - Highest recorded heart rate (pink card)
- 📊 **Avg BPM** - Average heart rate (yellow card)

**Right Panel:**
- 💓 **Current BPM** - Large display with animated heart icon
- 📈 **Real-time Chart** - Live ECG-style line graph
- 🚨 **Live Alerts** - Event log showing alerts and warnings

#### 4️⃣ **Stop Monitoring**

- Click the **← back arrow** in the top-left corner
- Your session data is **automatically saved** to history
- You'll return to the Activity Selection screen

#### 5️⃣ **View Session History** (Future Feature)

- Review past monitoring sessions
- See duration, date, and statistics for each session

---

## 🔧 Technical Details

### Application Architecture

```
┌─────────────────────────────────────────────┐
│           User Interface (Flet)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Profile  │  │ Activity │  │ Monitor  │  │
│  │  Page    │→ │   Page   │→ │   Page   │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│         State Management Layer              │
│         (MonitorState Class)                │
│  • User data  • Activity  • BPM history     │
│  • Statistics • Logs      • Sessions        │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│      Async Simulation (run_simulation)      │
│  • Momentum-based algorithm                 │
│  • Activity-specific profiles               │
│  • Realistic fluctuations                   │
└─────────────────────────────────────────────┘
```

### Key Components

#### 1. **MonitorState Class** (Lines 9-45)
Centralized state management holding:
- User profile data
- Current activity
- Heart rate history
- Statistics (min/max/avg)
- Event logs
- Session data

#### 2. **Async Simulation** (Lines 50-113)
- **Non-blocking** heart rate generation using `asyncio`
- **Momentum-based algorithm** for smooth, realistic transitions
- **Activity profiles** with different BPM ranges and fluctuation patterns
- **Boundary enforcement** (40-190 BPM limits)
- **1-second update interval**

#### 3. **UI Update System** (Lines 147-213)
- **Observer pattern** - `monitor_state.on_update` callback
- Updates all UI elements in sync
- Handles chart data points
- Animates heart icon
- Refreshes statistics

#### 4. **Page Routing** (Lines 550-578)
- **Multi-page navigation** using Flet's routing system
- Routes: `/profile` → `/activity` → `/monitor` → `/history`
- View stack management

### Activity Profiles Algorithm

Each activity has a unique profile:

```python
(min_bpm, max_bpm, momentum, fluctuation)
```

- **min_bpm/max_bpm**: Target heart rate range
- **momentum**: How quickly HR changes (0.0-1.0)
  - Higher = slower transitions (more stable)
  - Lower = faster transitions (more dynamic)
- **fluctuation**: Random noise amplitude

**Example - Running:**
```python
"Running": (130, 160, 0.4, 2.0)
```
- Target: 130-160 BPM
- Momentum: 0.4 (fast changes)
- Fluctuation: ±2.0 BPM random noise

### UI Design Principles

1. **Glassmorphism** - Translucent cards with blur effects
2. **Gradient Backgrounds** - Deep space blue/black theme
3. **Color Coding** - Each activity has a unique color
4. **Smooth Animations** - 200ms transitions
5. **Responsive Layout** - Flexible containers and rows

---

## 🎨 Customization

### Add a New Activity

1. **Add to activity profiles** (Line 54):
```python
activity_profiles = {
    "Cycling": (100, 140, 0.6, 1.3),  # New activity
    # ... existing activities
}
```

2. **Add to activity selection** (Lines 234-238):
```python
build_activity_card("Cycling", "directions_bike", "#00BCD4", monitor_state.activity == "Cycling"),
```

3. **Add color mapping** (Line 384):
```python
activity_colors = {
    "Cycling": "#00BCD4",  # Cyan
    # ... existing colors
}
```

### Change UI Colors

**Modify gradient backgrounds** (Lines 342-344):
```python
colors=["#0A1931", "#152238", "#0A1931"]  # Dark blue
```

**Customize card colors** (Lines 422-429):
```python
colors=["#00BCD4", "#0097A7"]  # Min BPM card (cyan)
colors=["#E91E63", "#C2185B"]  # Max BPM card (pink)
colors=["#FFC107", "#FF9800"]  # Avg BPM card (yellow)
```

### Adjust Simulation Parameters

**Change update frequency** (Line 110):
```python
await asyncio.sleep(1)  # 1 second = 1 Hz update rate
```

**Modify chart history length** (Line 100):
```python
if len(monitor_state.history) > 60:  # Keep last 60 data points
```

**Adjust heart rate boundaries** (Lines 80-85):
```python
if monitor_state.heart_rate < 40:   # Minimum BPM
if monitor_state.heart_rate > 190:  # Maximum BPM
```

---

## 🐛 Troubleshooting

### Common Issues

#### **Problem:** App doesn't start
**Solutions:**
- Ensure Python 3.8+ is installed: `python --version`
- Upgrade Flet: `pip install flet --upgrade`
- Check for errors in terminal output

#### **Problem:** Chart not updating
**Solutions:**
- Verify `monitor_state.on_update` is set (Line 214)
- Check browser console for JavaScript errors
- Restart the application

#### **Problem:** Window size is wrong
**Solutions:**
- Adjust window dimensions (Lines 120-121):
  ```python
  page.window_width = 1920
  page.window_height = 1080
  ```

#### **Problem:** Animations are laggy
**Solutions:**
- Reduce chart history length (Line 100)
- Increase update interval (Line 110)
- Close other resource-intensive applications

#### **Problem:** Session history not showing
**Solutions:**
- Ensure you've completed at least one monitoring session
- Check `monitor_state.history_sessions` is populated
- Navigate to `/history` route (future feature)

---

## 📊 Code Statistics

- **Total Lines:** 581
- **Functions:** 12
- **UI Pages:** 4 (Profile, Activity, Monitor, History)
- **Activity Profiles:** 5
- **UI Components:** 15+
- **Async Tasks:** 1 (simulation loop)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ideas for Contributions

- 🎨 Add new themes (light mode, custom colors)
- 📊 Export data to CSV/JSON
- 🔗 Connect to real hardware (Arduino, fitness trackers)
- 📱 Mobile app version (Flet supports iOS/Android)
- 🌍 Internationalization (multiple languages)
- 📈 Advanced analytics (HRV, trends, predictions)
- 🎵 Sound effects and audio feedback

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add some AmazingFeature'`
6. Push: `git push origin feature/AmazingFeature`
7. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **[Flet Framework](https://flet.dev/)** - Amazing Python UI framework for building beautiful apps
- **Python Community** - For excellent async/await support
- **Heart Rate Science** - Based on real physiological data

---

## 🔮 Future Enhancements

- [ ] Export session data to CSV/PDF
- [ ] Multi-user support with SQLite database
- [ ] Connect to real sensors via serial/Bluetooth
- [ ] Mobile app version (iOS/Android)
- [ ] Heart rate variability (HRV) analysis
- [ ] Integration with fitness APIs (Google Fit, Apple Health)
- [ ] Custom activity creation
- [ ] Dark/Light theme toggle
- [ ] Sound alerts for abnormal heart rates
- [ ] Data visualization improvements (multiple charts)

---

## 📸 Screenshots

> **Note:** Add screenshots of your app here!

```markdown
![Profile Screen](screenshots/profile.png)
![Activity Selection](screenshots/activity.png)
![Monitoring Dashboard](screenshots/monitor.png)
![Session History](screenshots/history.png)
```

---

**⭐ If you find this project useful, please give it a star on GitHub!**

**Made with ❤️ using [Flet](https://flet.dev/)**
