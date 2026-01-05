# 🌐 API Web Monitoring Guide

## 📍 Project URL
**https://github.com/maksim4351/api-health-monitor**

---

## 🚀 Quick Start Web Dashboard

### ⚡ Simplest Way (Windows)

**Just double-click the file:**
```
run_web_monitoring.bat
```

**What will happen:**
1. ✅ Automatically checks for Python (python, python3, py)
2. ✅ Installs dependencies from `requirements.txt`
3. ✅ Checks for `config.yaml`
4. ✅ Prompts for check interval (or uses from config.yaml)
5. ✅ Starts web server
6. ✅ Automatically opens browser at `http://localhost:8080`
7. ✅ Automatically finds free port if 8080 is busy

**💡 Important:**
- If port 8080 is busy, system automatically finds a free port (8081, 8082, etc.)
- Browser opens on the correct port automatically
- Press `Ctrl+C` in command line window to stop

---

## 📋 What `run_web_monitoring.bat` Does

### Step-by-step Description:

1. **Python Check**
   - Searches for `python`, `python3`, or `py`
   - Shows Python version
   - Shows error if Python not found

2. **Dependency Installation**
   - Automatically installs packages from `requirements.txt`
   - Works quietly (no extra output)

3. **Configuration Check**
   - Checks for `config.yaml`
   - Shows error if file not found

4. **Interval Prompt**
   - Asks for check interval in seconds
   - Press Enter to use interval from config.yaml
   - Example: `60` = check every minute

5. **Web Server Start**
   - Starts built-in HTTP server
   - Automatically finds free port (starting from 8080)
   - Shows access address

6. **Automatic Browser Opening**
   - Opens default browser
   - Navigates to web dashboard address
   - Ready to use!

---

## 🌐 Web Dashboard - Features

### 📊 "Monitoring" Tab

**Real-time Statistics:**
- Total APIs in monitoring
- Successful checks
- Failed checks
- Success rate

**Results Table:**
- Status of each API with color indicators:
  - 🟢 Green = API working (OK)
  - 🔴 Red = API unavailable (FAIL)
- HTTP status codes
- Latencies in milliseconds
- Error messages

**Auto-update:**
- Data updates every 5 seconds automatically
- No need to refresh page manually
- Changes visible immediately

### 🎛️ "API Management" Tab

**Adding New APIs:**
- Form with validation
- Fields:
  - **API Name** — display name (required)
  - **URL** — API address (required)
  - **Method** — HTTP method (GET, POST, PUT, DELETE, PATCH)
  - **Timeout** — wait time in seconds (default 5.0)
  - **Expected Status** — successful HTTP response code (default 200)
- Information hints ("i" icons) for each field
- Automatic saving to `config.yaml`

**Popular APIs:**
- List of 20 popular APIs for quick addition
- Google, GitHub, JSONPlaceholder, HTTPBin, Reddit, and others
- One click to fill the form
- Quick addition to monitoring

**Current API Management:**
- View all added APIs
- Edit existing APIs (✏️ button)
- Delete APIs (🗑️ button) with confirmation
- Automatic change saving

**Notifications:**
- ✅ Successful API addition
- ⚠️ Warning if API already exists
- ⏳ Addition process indicator

### 📚 "About Project" Tab

- Project description and features
- Version information
- Documentation links
- Technologies and dependencies

### 📖 OpenAPI Documentation

- **Swagger UI** available at `/api/docs` or `/swagger`
- **OpenAPI specification** at `/api/swagger.json`
- Interactive documentation for all REST API endpoints
- Ability to test API directly from browser

---

## 🔔 Notifications

### Browser Push Notifications
- Automatic notifications on API errors
- Service recovery notifications
- Configurable notification types

### Email Notifications (if configured)
- Sending to specified email addresses
- HTML and text versions of emails
- Configurable notification conditions

---

## 🛠️ Alternative Launch Methods

### Via Command Line

```bash
# With interval from config.yaml
api-monitor watch config.yaml --web

# With custom interval (every 30 seconds)
api-monitor watch config.yaml --web --interval 30

# With custom port
api-monitor watch config.yaml --web --port 9000

# Combination: interval + port
api-monitor watch config.yaml --web --interval 60 --port 3000
```

### Via Python Directly

```bash
# With interval from config.yaml
python -m api_monitor.cli watch config.yaml --web

# With custom interval
python -m api_monitor.cli watch config.yaml --web --interval 30
```

---

## 🔧 Configuration

### Changing Port

If port 8080 is busy, specify another:

```bash
api-monitor watch config.yaml --web --port 9000
```

Or in `run_web_monitoring.bat` change command to:
```bash
%PYTHON_CMD% -m api_monitor.cli watch config.yaml --web --port 9000
```

### Changing Interval

**In config.yaml:**
```yaml
interval: 60  # Check every 60 seconds
```

**Or via command line:**
```bash
api-monitor watch config.yaml --web --interval 30
```

### Notification Configuration

**In config.yaml:**
```yaml
notifications:
  email:
    enabled: true
    smtp_host: smtp.gmail.com
    smtp_port: 587
    smtp_user: your-email@gmail.com
    smtp_password: your-app-password
    to: [admin@example.com]
  push:
    enabled: true  # Browser notifications
```

---

## 📱 Access from Other Devices

If you're on a local network, you can open the dashboard from other devices:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. Open in browser on another device:
   ```
   http://YOUR_IP:8080
   ```

   For example:
   ```
   http://192.168.1.100:8080
   ```

---

## 🔍 Troubleshooting

### Port Busy

**Automatic Solution:**
- System automatically finds free port
- You'll see message: `✅ Free port found: 8081`
- Browser opens on correct port

**Manual Solution:**
1. Specify another port: `--port 9000`
2. Close program using port 8080
3. Run as administrator (if needed)

### Browser Doesn't Open

Open manually:
```
http://localhost:8080
```

Or check which port is used (see command line output).

### Data Not Updating

- Check internet connection
- Ensure APIs are accessible
- Check console for errors
- Refresh page manually (F5)

### Error "config.yaml not found"

Create `config.yaml` file in project root. Example:
```yaml
output_format: table
apis:
  - name: Google
    url: https://www.google.com
    method: GET
    timeout: 5.0
    expected_status: 200
```

---

## 📊 REST API Endpoints

Web server provides REST API:

- `GET /` - Dashboard main page
- `GET /api/data` - Monitoring JSON data
- `GET /api/stats` - Statistics
- `GET /api/project` - Project information
- `GET /api/apis` - List of current APIs
- `GET /api/popular` - List of popular APIs
- `POST /api/apis` - Add new API
- `PUT /api/apis/{name}` - Update existing API
- `DELETE /api/apis/{name}` - Delete API
- `GET /api/refresh` - Force monitoring refresh
- `GET /api/docs` or `/swagger` - Swagger UI documentation
- `GET /api/swagger.json` - OpenAPI specification

---

## 🎯 Usage Examples

### Monitoring Every Minute in Browser
```bash
run_web_monitoring.bat
# Enter: 60
```

### Monitoring on Different Port
```bash
api-monitor watch config.yaml --web --port 3000
```

### Monitoring with Short Interval (Every 10 Seconds)
```bash
api-monitor watch config.yaml --web --interval 10
```

---

## 🛑 Stopping

Press `Ctrl+C` in the command line window where monitoring is running.

---

## 💡 Tips

1. **Use web dashboard** for visual monitoring
2. **Add APIs via web interface** - easier than editing YAML
3. **Use popular APIs** for quick start
4. **Configure notifications** for automatic alerts
5. **Open Swagger UI** to explore API: `/api/docs`

---

## 🔗 Useful Links

- **Repository:** https://github.com/maksim4351/api-health-monitor
- **Documentation:** https://github.com/maksim4351/api-health-monitor#readme
- **Issues:** https://github.com/maksim4351/api-health-monitor/issues
- **Discussions:** https://github.com/maksim4351/api-health-monitor/discussions

---

**Enjoy visual monitoring! 🎉**
