# 🐛 Troubleshooting Guide

Common issues and solutions when setting up or running PORTIA compiler.

---

## Port Already in Use

**Problem**: Error message like `Address already in use` or `Port 8000 is already in use`

**Solutions**:

### Option 1: Kill the Process
**Windows:**
```powershell
# Find process using the port
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Option 2: Use a Different Port
```bash
# Run on a different port
uvicorn app.main:app --reload --port 8005
```

---

## Virtual Environment Issues

### PowerShell Script Execution Error

**Problem**: `cannot be loaded because running scripts is disabled on this system`

**Solution**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Not Found

**Problem**: `'python' is not recognized as an internal or external command`

**Solutions**:
1. Install Python from [python.org](https://python.org/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### Wrong Python Version

**Problem**: Need Python 3.8+ but have an older version

**Solution**:
```bash
# Use python3 explicitly
python3 -m venv venv

# Or on Windows
py -3 -m venv venv
```

### Virtual Environment Won't Activate

**Windows (PowerShell)**:
```powershell
# Full path activation
C:\Users\YourName\portia-compiler\lexer-backend\venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
# Full path activation
source /path/to/portia-compiler/lexer-backend/venv/bin/activate
```

---

## Module Not Found Errors

### `ModuleNotFoundError: No module named 'fastapi'`

**Problem**: Dependencies not installed

**Solution**:
```bash
# Ensure virtual environment is activated
# You should see (venv) in your terminal prompt

# Install dependencies
pip install fastapi uvicorn

# Verify installation
pip list
```

### Wrong Python Interpreter

**Problem**: Using system Python instead of virtual environment

**Check active environment**:
```bash
# Windows
where python

# macOS/Linux  
which python
```

Should show path to `venv/Scripts/python` or `venv/bin/python`

**Solution**: Activate virtual environment first
```bash
# Windows
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

---

## Frontend Issues

### Node Modules Error

**Problem**: `Cannot find module` or corrupted `node_modules`

**Solution**:
```bash
# Remove old files
rm -rf node_modules package-lock.json  # macOS/Linux
# or
rmdir /s /q node_modules & del package-lock.json  # Windows

# Reinstall
npm install
```

### Port 5173 Already in Use

**Problem**: Vite dev server port is occupied

**Solution**:
Vite will automatically try the next available port (5174, 5175, etc.)

Or specify a port:
```bash
npm run dev -- --port 3000
```

### `npm` Command Not Found

**Problem**: Node.js not installed or not in PATH

**Solution**:
1. Install Node.js from [nodejs.org](https://nodejs.org/)
2. Verify installation:
   ```bash
   node --version
   npm --version
   ```

---

## Backend API Connection Issues

### Frontend Can't Connect to Backend

**Problem**: CORS errors or connection refused

**Checklist**:
1. ✅ Is the backend running?
   ```bash
   # Check if backend is running
   curl http://localhost:8000
   ```

2. ✅ Correct port numbers?
   - Lexer: `8000`
   - Parser: `8001`
   - Semantic: `8002`

3. ✅ Check environment variables:
   ```bash
   # In app-frontend/.env (if exists)
   VITE_LEXER_BACKEND_URL=http://localhost:8000
   VITE_PARSER_BACKEND_URL=http://localhost:8001
   VITE_SEMANTIC_BACKEND_URL=http://localhost:8002
   ```

---

## Git Issues

### Cannot Push to Repository

**Problem**: `Permission denied` or `Authentication failed`

**Solutions**:

1. **Check remote URL**:
   ```bash
   git remote -v
   ```

2. **Use HTTPS with Personal Access Token**:
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/portia-compiler.git
   ```

3. **Use SSH**:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/portia-compiler.git
   ```

### Merge Conflicts

**Problem**: Conflicts when pulling/merging

**Solution**:
```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# If conflicts occur, resolve them manually
# Then:
git add .
git commit -m "Merge: resolve conflicts"
```

---

## Import/Path Issues

### Python Import Errors

**Problem**: `ImportError: attempted relative import with no known parent package`

**Solution**: Ensure you're running from the correct directory
```bash
# For lexer backend
cd lexer-backend
uvicorn app.main:app --reload

# Not from project root
```

### TypeScript Path Errors

**Problem**: Cannot find module imports

**Solution**: Check `tsconfig.json` paths are correct
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## Performance Issues

### Slow Syntax Highlighting

**Problem**: Highlighting updates are laggy

**Current debounce**: 20ms (in `LexerPanel.tsx`)

If still slow, check:
1. Browser performance (too many tabs?)
2. Backend response time
3. Large file size

### Backend Slow to Start

**Problem**: `uvicorn` takes long to start

**Solutions**:
- Ensure virtual environment is activated
- Check for port conflicts
- Use `--reload` only in development

---

## Environment-Specific Issues

### macOS: Command Line Tools

**Problem**: Build errors on macOS

**Solution**:
```bash
xcode-select --install
```

### Windows: Long Path Issues

**Problem**: `FileNotFoundError` with long paths

**Solution**: Enable long paths in Windows
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Linux: Permission Errors

**Problem**: Permission denied when running scripts

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.ps1

# Or run with bash
bash scripts/start-lexer.ps1
```

---

## Still Having Issues?

If none of these solutions work:

1. 📝 Check existing [GitHub Issues](https://github.com/DanielHC16/portia-compiler/issues)
2. 🆕 Open a new issue with:
   - Your OS and version
   - Python version (`python --version`)
   - Node version (`node --version`)
   - Complete error message
   - Steps to reproduce
3. 💬 Include screenshots if relevant

---

## Useful Debugging Commands

```bash
# Check Python version
python --version

# Check Node version
node --version

# Check npm version
npm --version

# List installed Python packages
pip list

# List installed npm packages
npm list

# Check if port is in use (Windows)
netstat -ano | findstr :8000

# Check if port is in use (macOS/Linux)
lsof -i :8000

# Test backend API
curl http://localhost:8000

# Check git status
git status

# Check git remotes
git remote -v
```

---

[← Back to README](../README.md)
