# HealthOS Tracker

![HealthOS Tracker](https://img.shields.io/badge/version-2.0-blue)
![PWA](https://img.shields.io/badge/PWA-✓-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A modern, privacy-focused Progressive Web App for tracking weight, waist measurements, and nutrition macros with beautiful visualizations and goal tracking.

## ✨ Features

- **📊 Weight Tracking** - Daily weight logging with trend analysis
- **📏 Waist Measurements** - Circumference tracking with separate charts
- **🥗 Macro Monitoring** - Calories and protein intake tracking
- **🎯 Goal Progress** - Visual progress toward weight goals (100kg, 95kg)
- **📈 Interactive Charts** - Dual-axis charts with Chart.js
- **📱 PWA Ready** - Installable, works offline, mobile-optimized
- **🔄 Data Sync** - Optional Flask backend for multi-device sync
- **💾 Export/Import** - JSON data backup and restore
- **🌙 Dark Theme** - Easy-on-the-eyes dark interface

## 🚀 Quick Start

### Option 1: Static Hosting (No Backend Required)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/health-tracker.git
   cd health-tracker
   ```
2. Serve the files with any static server:
   ```bash
   python -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser

### Option 2: With Flask Backend (Multi-device Sync)
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Flask server:
   ```bash
   python server.py
   ```
3. Open `http://localhost:5000` in your browser

## 📦 Installation Options

### GitHub Pages Deployment
1. Fork this repository
2. Go to Settings → Pages
3. Set source to "Deploy from a branch"
4. Select `main` branch and `/ (root)` folder
5. Your site will be available at `https://yourusername.github.io/health-tracker`

### Netlify / Vercel Deployment
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/health-tracker)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/health-tracker)

### Traditional Web Server
Simply upload all files to your web server's public directory.

## 🖥️ Usage

### Adding Daily Entries
1. Click the "Log Today" button
2. Enter your weight (kg), waist measurement (cm), calories, and protein
3. Click "Save Entry" - data is saved immediately

### Viewing Trends
- Switch between 30-day, 90-day, and "All" views using the tab buttons
- Hover over chart points to see detailed values
- Goal lines show progress toward 100kg and 95kg targets

### Data Management
- **Export**: Click "Export" to download all data as JSON
- **Import**: Click "Import" to restore from a JSON backup
- **Sync**: With backend enabled, data syncs automatically between devices

## 🏗️ Project Structure

```
health-tracker/
├── index.html              # Main PWA interface
├── app.js                  # Core application logic (644 lines)
├── example_data.json       # Example dataset (synthetic demo data)
├── manifest.json           # PWA configuration
├── sw.js                   # Service worker for offline support
├── server.py               # Optional Flask backend
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
└── .gitignore             # Git ignore patterns (excludes personal data)
```

### Data Files
- `example_data.json` - Synthetic demo data included in repository
- `data.json` - **Your personal data** (excluded via .gitignore, create your own)
- `consolidated_health_data.csv` - Consolidated data export (excluded)
- `consolidated_health_data.json` - Consolidated JSON export (excluded)

### Optional Analysis Scripts
The repository includes Python scripts for advanced data analysis:
- `analyze_health_data.py` - Comprehensive health data analysis
- `analyze_macros.py` - Macro nutrient pattern analysis
- `estimate_bodyfat.py` - Body fat estimation
- `process_health_data.py` - Data processing utilities

## 📊 Using Your Own Data

This repository is configured for public sharing with example data. To use your own personal health data:

### Option 1: Static Mode (No Backend)
1. Create a `data.json` file in the project root with your data
2. The app will load it automatically from localStorage or your file
3. Your `data.json` is excluded from Git via `.gitignore`

### Option 2: With Flask Backend
1. Place your `data.json` in the project root
2. Start the Flask server: `python server.py`
3. The server will automatically seed from your `data.json` on first run
4. Your data stays local and is never uploaded to GitHub

### Data Format
Your `data.json` should follow this structure:
```json
[
  {
    "date": "2023-01-01T00:00:00.000",
    "weight": 85.0,
    "notes": "Optional note",
    "type": "weight_history",
    "waist_cm": 95.0,
    "hips_cm": 105.0,
    "biceps_l": 32.0,
    "biceps_r": 31.5,
    "calories": 2200,
    "protein_g": 150,
    "carbs_g": 200,
    "fat_g": 80
  }
]
```

### Privacy Protection
- Personal data files (`data.json`, `consolidated_health_data.csv`, etc.) are excluded via `.gitignore`
- The repository includes only synthetic `example_data.json` for demonstration
- Your personal health data remains on your local machine
- GitHub Pages deployment uses example data only

## 🔧 Development

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- For backend: Python 3.8+ with Flask

### Local Development
1. Clone the repository
2. For backend development:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python server.py
   ```
3. For frontend-only development, use any static file server

### Building for Production
The app is ready for production as-is. For optimized deployment:

1. **Static Hosting**: All files in root directory are production-ready
2. **Backend Hosting**: Deploy `server.py` with WSGI server (gunicorn, uWSGI)
3. **PWA Optimization**: Service worker is already configured

## 🔌 API Reference (Backend)

If using the Flask backend:

### GET `/api/data`
Returns all health data as JSON array.

**Response:**
```json
[
  {
    "date": "2025-01-15",
    "weight": 104.5,
    "waist_cm": 98.0,
    "calories": 2400,
    "protein_g": 180
  }
]
```

### PUT `/api/data`
Replace all health data. Requires JSON array in request body.

**Request Body:** JSON array of health entries
**Response:**
```json
{
  "ok": true,
  "count": 42,
  "synced": "2025-01-15T12:30:45Z"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "entries": 42
}
```

## 📱 PWA Features

### Installation
- **Chrome/Edge**: Click the install icon in address bar
- **Safari**: Tap Share → Add to Home Screen
- **Android Chrome**: Menu → Add to Home Screen
- **iOS Safari**: Share button → Add to Home Screen

### Offline Support
- Service worker caches essential assets
- Works without internet connection after first load
- Data stored in localStorage when offline, syncs when back online

## 🔒 Privacy & Data Security

- **Local-First**: Data stored in your browser by default
- **Optional Sync**: Backend sync is opt-in
- **No Analytics**: No tracking or analytics scripts
- **Export Control**: You own your data, can export anytime
- **Open Source**: Transparent code, no hidden data collection
- **GitHub Safe**: Repository contains only example data, personal data excluded via `.gitignore`
- **Public Repository Ready**: Safe for public GitHub Pages deployment
- **Your Data Stays Local**: Personal `data.json` never uploaded to GitHub

## 🐛 Troubleshooting

### Common Issues

**"Service worker not registering"**
- Ensure you're accessing via HTTPS or localhost
- Clear browser cache and reload

**"Charts not loading"**
- Check internet connection (CDN dependencies)
- Try refreshing the page

**"Data not saving"**
- Check browser console for errors
- Ensure localStorage is not disabled
- Try exporting data as backup

**"Backend not connecting"**
- Verify Flask server is running (`python server.py`)
- Check CORS settings if hosting on different domains

### Browser Support
- Chrome 60+ ✓
- Firefox 55+ ✓
- Safari 11+ ✓
- Edge 79+ ✓
- iOS Safari 11+ ✓
- Android Chrome 60+ ✓

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style
- Add comments for complex logic
- Update documentation as needed
- Test changes in multiple browsers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Chart.js](https://www.chartjs.org/) for beautiful visualizations
- [Lucide Icons](https://lucide.dev/) for clean icons
- [Flask](https://flask.palletsprojects.com/) for lightweight backend
- All contributors and users of HealthOS

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/health-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/health-tracker/discussions)

---

**HealthOS Tracker** - Your personal health companion. Track progress, achieve goals, stay healthy. 🏋️‍♂️