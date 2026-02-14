# HealthOS Tracker - Deployment Guide

This guide explains how to deploy HealthOS Tracker to various hosting platforms, with special attention to privacy considerations for public repositories.

## 📋 Prerequisites

- GitHub account (for GitHub Pages)
- Basic familiarity with Git

## 🚀 GitHub Pages Deployment

### Step 1: Create a New Repository
1. Go to [GitHub](https://github.com) and create a new repository named `health-tracker`
2. Make it **public** (required for GitHub Pages)
3. Do **NOT** initialize with README, .gitignore, or license (we'll add these)

### Step 2: Push Your Code
```bash
# Clone your repository
git clone https://github.com/YOUR-USERNAME/health-tracker.git
cd health-tracker

# Copy all HealthOS Tracker files to this directory
# (Copy all files from the health-tracker folder)

# Add, commit, and push
git add .
git commit -m "Initial commit: HealthOS Tracker v2.0"
git push origin main
```

### Step 3: Configure GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Select **main** branch and **/ (root)** folder
5. Click **Save**

### Step 4: Access Your Site
Your site will be available at:
```
https://YOUR-USERNAME.github.io/health-tracker/
```

## 🔒 Privacy Considerations for GitHub Pages

### Important: GitHub Pages is Public
- GitHub Pages sites are **always public**
- Anyone can view your repository contents
- **DO NOT** commit personal health data

### Protected Files
The repository is configured with `.gitignore` to exclude:
- `data.json` (your personal health data)
- `consolidated_health_data.csv`
- `consolidated_health_data.json`
- `timestamps.json`
- `data/` directory
- Personal documentation files

### Using Your Own Data Locally
1. **Keep personal data local**: Your `data.json` stays on your computer
2. **GitHub uses example data**: The deployed site uses `example_data.json`
3. **Local development**: When running locally, the app will use your `data.json` if present

## 🌐 Alternative Hosting Options

### Netlify
1. Push your code to GitHub
2. Go to [Netlify](https://netlify.com)
3. Click **Add new site** → **Import from Git**
4. Select your repository
5. Deploy with default settings

### Vercel
1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Click **Add New Project**
4. Import your repository
5. Deploy with default settings

### Traditional Web Hosting
1. Upload all files to your web server
2. Ensure `.htaccess` (Apache) or equivalent is configured for SPA routing
3. Access via your domain

## 🔧 Configuration for Different Hosts

### Static Hosting (GitHub Pages, Netlify, Vercel)
- Use `API_BASE = ''` in `app.js` (default)
- Data stored in browser's localStorage
- No backend required

### With Flask Backend (Self-Hosted)
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Update `app.js` to use your server URL:
   ```javascript
   const API_BASE = 'http://your-domain.com:5000';
   ```

## 📊 Data Migration

### Moving from Local to Hosted
1. **Export** your data from the local app
2. **Import** into the hosted version
3. Data persists in browser localStorage per domain

### Backing Up Your Data
1. Regularly use the **Export** feature
2. Save the JSON file to a secure location
3. Consider encrypted cloud storage for backups

## 🐛 Troubleshooting Deployment

### Common Issues

**"Page not found" on GitHub Pages**
- Ensure you're using the correct URL: `username.github.io/repository-name/`
- Check that `index.html` is in the root of your repository
- Wait a few minutes after enabling GitHub Pages

**"Charts not loading"**
- GitHub Pages serves over HTTPS, ensure all resources use HTTPS
- Check browser console for mixed content errors

**"Service worker not registering"**
- Service workers require HTTPS or localhost
- GitHub Pages provides HTTPS automatically
- Clear browser cache if issues persist

**"Data not saving between sessions"**
- With static hosting, data is stored in browser localStorage
- Different browsers/devices have separate storage
- Use the Flask backend for multi-device sync

## 🔐 Security Best Practices

1. **Never commit personal data** to the repository
2. **Use strong passwords** if adding authentication
3. **Enable HTTPS** on all deployments
4. **Regular backups** of your data
5. **Keep dependencies updated**

## 📞 Support

For deployment issues:
- Check the [GitHub Pages documentation](https://docs.github.com/en/pages)
- Review browser console for errors
- Open an issue in the repository

---

**Remember**: Your health data is personal and sensitive. The public repository contains only example data. Your personal `data.json` should remain on your local machine and never be committed to Git.