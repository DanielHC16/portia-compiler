# 📦 Installation Guide

Complete step-by-step installation instructions for PORTIA compiler.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)

---

## 1. Clone the Repository

```bash
git clone https://github.com/DanielHC16/portia-compiler.git
cd portia-compiler
```

> **📌 Note**: The repository includes a [`.gitignore`](../.gitignore) that prevents committing unwanted files. See [Contributing Guide](CONTRIBUTING.md) for Git workflow.

---

## 2. Backend Setup

### Lexer Backend
```bash
cd lexer-backend
python -m venv venv

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate

pip install fastapi uvicorn
```

### Parser Backend
```bash
cd ../parser-backend
python -m venv venv

# Activate virtual environment (same commands as above)
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate

pip install fastapi uvicorn
```

### Semantic Backend
```bash
cd ../semantic-backend
python -m venv venv

# Activate virtual environment (same commands as above)
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate

pip install fastapi uvicorn
```

---

## 3. Frontend Setup

```bash
cd ../app-frontend
npm install
```

---

## 4. Running the Application

You have two options to run the application:

### Option A: Using Scripts (Recommended)

Open **three separate terminal windows** and run:

**Terminal 1 - Lexer Backend:**
```bash
# From the project root directory
cd scripts
./start-lexer.ps1      # On Windows
# or
bash start-lexer.ps1   # On macOS/Linux
```

**Terminal 2 - Parser Backend:**
```bash
# From the project root directory
cd scripts
./start-parser.ps1     # On Windows
# or
bash start-parser.ps1  # On macOS/Linux
```

**Terminal 3 - Semantic Backend:**
```bash
# From the project root directory
cd scripts
./start-semantic.ps1   # On Windows
# or
bash start-semantic.ps1 # On macOS/Linux
```

**Terminal 4 - Frontend:**
```bash
# From the project root directory
cd app-frontend
npm run dev
```

### Option B: Manual Setup

Open **four separate terminal windows** and run:

**Terminal 1 - Lexer Backend:**
```bash
cd lexer-backend
# Activate virtual environment
venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate   # macOS/Linux

uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Parser Backend:**
```bash
cd parser-backend
# Activate virtual environment
venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate   # macOS/Linux

uvicorn main:app --reload --port 8001
```

**Terminal 3 - Semantic Backend:**
```bash
cd semantic-backend
# Activate virtual environment
venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate   # macOS/Linux

uvicorn main:app --reload --port 8002
```

**Terminal 4 - Frontend:**
```bash
cd app-frontend
npm run dev
```

---

## 5. Access the Application

Once all services are running, open your browser and navigate to:
```
http://localhost:5173
```

The application should now be fully functional with:
- **Lexer Backend** running on `http://localhost:8000`
- **Parser Backend** running on `http://localhost:8001`
- **Semantic Backend** running on `http://localhost:8002`
- **Frontend** running on `http://localhost:5173`

---

## Next Steps

- See [Troubleshooting Guide](TROUBLESHOOTING.md) if you encounter issues
- Read [Contributing Guide](CONTRIBUTING.md) to start making changes
- Check out [Features](../README.md#-features) to see what's available

---

[← Back to README](../README.md)
