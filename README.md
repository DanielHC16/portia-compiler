# PORTIA Programming Language  
### Written by: BSCS 3‑3 A.Y. 2025‑2026 | LoomVI  

PORTIA takes its name from the Portia spider — renowned for patience, precision, and calculated strategy. Just as the spider weaves its web with intent, PORTIA weaves rules and logic into a unified and purposeful structure.

PORTIA is a **high‑level, procedural, statically typed programming language** built around clarity and discipline. Programs are written as tightly defined statements, with explicit scoping and language features that emphasize order, readability, and precision.

- **From C** → procedural structure, explicit scoping, disciplined statement design  
- **From Python** → readability, consistency, avoidance of ambiguity  
- **From Lua** → intuitive string handling  

Like a web, PORTIA programs form deliberate, interconnected patterns of intent.

---

## 🛠 Tech Stack
- **Backend**: Python · FastAPI · Uvicorn  
- **Frontend**: React · Vite · TypeScript · Monaco Editor  

---

## ⚙️ Installation & Setup

### Prerequisites
Before you begin, ensure you have the following installed:
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)

### 1. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/DanielHC16/portia-compiler.git
cd portia-compiler
```

### 2. Backend Setup

#### Lexer Backend
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

#### Parser Backend
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

#### Semantic Backend
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

### 3. Frontend Setup
```bash
cd ../app-frontend
npm install
```

### 4. Running the Application

You have two options to run the application:

#### Option A: Using Scripts (Recommended)
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

#### Option B: Manual Setup
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

### 5. Access the Application
Once all services are running, open your browser and navigate to:
```
http://localhost:5173
```

The application should now be fully functional with:
- **Lexer Backend** running on `http://localhost:8000`
- **Parser Backend** running on `http://localhost:8001`
- **Semantic Backend** running on `http://localhost:8002`
- **Frontend** running on `http://localhost:5173`

### Troubleshooting

#### Port Already in Use
If you get a "port already in use" error, you can either:
- Kill the process using that port
- Change the port by modifying the respective `main.py` files or using `--port` flag

#### Virtual Environment Issues
If you have trouble activating the virtual environment:
- On Windows, you may need to enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Ensure Python is properly installed and added to PATH

#### Module Not Found Errors
If you get module import errors, ensure you:
1. Activated the virtual environment
2. Installed all dependencies with `pip install fastapi uvicorn`
3. Are in the correct directory

---

## 📁 Project Structure
```
portia-compiler/
├── app-frontend/          # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api.ts        # Backend API calls
│   │   └── main.tsx      # Entry point
│   └── package.json
├── lexer-backend/         # Lexical analyzer
│   ├── app/
│   │   ├── lexer/        # Lexer implementation
│   │   └── main.py       # FastAPI server
│   └── package.json
├── parser-backend/        # Syntax analyzer
│   ├── parser/
│   │   └── syntax_analyzer.py
│   └── main.py
├── semantic-backend/      # Semantic analyzer
│   ├── semantic/
│   │   └── semantic_analyzer.py
│   └── main.py
└── scripts/              # Startup scripts
    ├── start-lexer.ps1
    ├── start-parser.ps1
    └── start-semantic.ps1
```

---

## 🎨 Features
- **Lexical Analysis**: Real-time tokenization with syntax highlighting
- **Syntax Analysis**: Parse tree generation (TBA)
- **Semantic Analysis**: Type checking and validation (TBA)
- **Theme Toggle**: Switch between light and dark modes
- **Persistent State**: Code persists across tab switches
- **Error Highlighting**: Visual feedback for lexical errors

---

## TODO List
Backend
- Verify lexer correctness against the full PORTIA spec
- Double‑check token classification 
- Add more robust error handling and edge‑case coverage

Frontend
- Theme Picker Integration
- Add buttons for: Semantic and Syntax Analyzer

General
- Include Syntax and Semantic Analyzer Buttons. 
- Finalize and Verify CFG

Next Step: Semantic -> Syntax
