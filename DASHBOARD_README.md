# AI Agents Research Dashboard

A modern, dark-themed dashboard for tracking AI Agents and Web3 projects with real-time cryptocurrency news.

## Features

- **Project Tracking**: Monitor AI Agents, DePIN, and Infra projects
- **Market Data**: Real-time price, volume, and market cap data from CoinGecko
- **Crypto News Feed**: Latest cryptocurrency news with sentiment analysis from CryptoPanic
- **Dark Terminal Theme**: Modern glassmorphism design with terminal aesthetics
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Option 1: CORS Proxy (Easiest)
The dashboard uses `corsproxy.io` to bypass CORS restrictions. Simply open `index.html` in your browser.

**Note**: If the proxy is rate-limited or unavailable, use the local server option below.

### Option 2: Local Development Server (Recommended)
For better performance and no CORS issues:

#### Windows (Batch)
```cmd
start-server.bat
```

#### Windows (PowerShell)
```powershell
.\start-server.ps1
```

#### Manual Python Server
```bash
python -m http.server 8000
```

Then open: `http://localhost:8000`

### Option 3: Browser CORS Extension
Install a CORS extension for Chrome/Firefox:
- **Chrome**: [CORS Unblock](https://chrome.google.com/webstore/detail/cors-unblock/lfhmikememgdcahcdlaciloancbhjino)
- **Firefox**: [CORS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/cors-everywhere/)

## CORS Solutions

### Why CORS Issues Occur
When opening HTML files directly in the browser (`file://` protocol), browsers block cross-origin requests for security.

### Solutions Summary

1. **CORS Proxy** (Default): Uses `corsproxy.io` service
   - ✅ Works immediately in most cases
   - ✅ No setup required
   - ⚠️ May have rate limits

2. **Local Server**: Serve files via HTTP server
   - ✅ No CORS issues
   - ✅ Better performance
   - ✅ Recommended for development

3. **Browser Extension**: Disable CORS in browser
   - ✅ Quick for development
   - ⚠️ Only for testing (security risk)

## API Keys

The dashboard uses these APIs:
- **CoinGecko**: Free tier (no key required)
- **CryptoPanic**: Uses API key with `&public=true` parameter for public access

## Customization

Edit `index.html` to:
- Add/remove projects in the `defaultProjectsData` array
- Modify API endpoints
- Adjust refresh intervals
- Customize styling

## Troubleshooting

### News Feed Not Loading
1. Check browser console for errors
2. Try the local server option
3. Verify internet connection
4. CORS proxy may be rate-limited

### Market Data Not Updating
1. Check CoinGecko API status
2. Verify project IDs in the code
3. Check browser console

## Technologies Used

- **HTML5/CSS3**: Modern web standards
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript (ES6+)**: Vanilla JS with fetch API
- **Font Awesome**: Icons
- **Google Fonts**: Inter and JetBrains Mono fonts