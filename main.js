// main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
let pythonProcess = null;
let mainWindow = null;

// Create the main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // In development, load from Vite dev server
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // In production, load the built files
    mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
  }
}

// Start Python FastAPI server
function startPythonServer() {
  const pythonScript = path.join(__dirname, 'backend', 'api.py');
  pythonProcess = spawn('python', [pythonScript], {
    stdio: 'pipe'
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });
}

// Start tracking function
function startTracking() {
  const trackingScript = path.join(__dirname, 'backend', 'focus.py');
  const trackingProcess = spawn('python', [trackingScript], {
    stdio: 'pipe'
  });

  trackingProcess.stdout.on('data', (data) => {
    mainWindow.webContents.send('tracking-update', data.toString());
  });

  return trackingProcess;
}

// IPC handlers
ipcMain.on('start-tracking', () => {
  const process = startTracking();
  mainWindow.webContents.send('tracking-started');
  
  // Handle stopping
  ipcMain.once('stop-tracking', () => {
    process.kill();
    mainWindow.webContents.send('tracking-stopped');
  });
});

// App lifecycle
app.whenReady().then(() => {
  createWindow();
  startPythonServer();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (pythonProcess) {
      pythonProcess.kill();
    }
    app.quit();
  }
});