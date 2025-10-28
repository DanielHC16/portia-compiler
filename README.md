# PORTIA Programming Language  
### Written by: BSCS 3‑3 A.Y. 2025‑2026 | LoomVI  

PORTIA takes its name from the Portia spider — renowned for patience, precision, and calculated strategy. Just as the spider weaves its web with intent, PORTIA weaves rules and logic into a unified and purposeful structure.

PORTIA is a **high‑level, procedural, statically typed programming language** built around clarity and discipline. Programs are written as tightly defined statements, with explicit scoping and language features that emphasize order, readability, and precision.

- **From C** → procedural structure, explicit scoping, disciplined statement design  
- **From Python** → readability, consistency, avoidance of ambiguity  
- **From Lua** → intuitive string handling  

Like a web, PORTIA programs form deliberate, interconnected patterns of intent.

---

## 📑 Table of Contents
- [🛠 Tech Stack](#-tech-stack)
- [⚙️ Quick Start](#️-quick-start)
- [📦 Detailed Installation](#-detailed-installation)
  - [Prerequisites](#prerequisites)
  - [Clone Repository](#1-clone-the-repository)
  - [Backend Setup](#2-backend-setup)
  - [Frontend Setup](#3-frontend-setup)
  - [Running the App](#4-running-the-application)
- [📁 Project Structure](#-project-structure)
- [🎨 Features](#-features)
- [🔧 Contributing Guide](#-contributing-guide)
  - [Git Workflow](#git-workflow)
  - [Making Changes](#making-changes)
  - [Best Practices](#best-practices)
- [🐛 Troubleshooting](#-troubleshooting)
- [📋 TODO List](#-todo-list)

---

## 🛠 Tech Stack
- **Backend**: Python · FastAPI · Uvicorn  
- **Frontend**: React · Vite · TypeScript · Monaco Editor  

---

## ⚙️ Quick Start

**TL;DR** - Get up and running in 5 minutes:

```bash
# 1. Clone the repo
git clone https://github.com/DanielHC16/portia-compiler.git
cd portia-compiler

# 2. Setup backends (3 terminals)
cd lexer-backend && python -m venv venv && venv\Scripts\Activate.ps1 && pip install fastapi uvicorn
cd parser-backend && python -m venv venv && venv\Scripts\Activate.ps1 && pip install fastapi uvicorn
cd semantic-backend && python -m venv venv && venv\Scripts\Activate.ps1 && pip install fastapi uvicorn

# 3. Setup frontend (1 terminal)
cd app-frontend && npm install

# 4. Run everything (4 terminals)
cd lexer-backend && venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload --port 8000
cd parser-backend && venv\Scripts\Activate.ps1 && uvicorn main:app --reload --port 8001
cd semantic-backend && venv\Scripts\Activate.ps1 && uvicorn main:app --reload --port 8002
cd app-frontend && npm run dev

# 5. Open browser at http://localhost:5173
```

> For detailed step-by-step instructions, see [📦 Detailed Installation](#-detailed-installation)

---

## 📦 Detailed Installation

### Prerequisites
Before you begin, ensure you have the following installed:
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/DanielHC16/portia-compiler.git
cd portia-compiler
```

> **📌 Note**: The repository includes a [`.gitignore`](.gitignore) that prevents committing unwanted files. See [Contributing Guide](#-contributing-guide) for Git workflow.

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

---

## 🐛 Troubleshooting

<details>
<summary><b>Port Already in Use</b></summary>

If you get a "port already in use" error:
- **Option 1**: Kill the process using that port
- **Option 2**: Change the port using `--port` flag:
  ```bash
  uvicorn app.main:app --reload --port 8005
  ```
</details>

<details>
<summary><b>Virtual Environment Issues</b></summary>

**Windows PowerShell script execution error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Python not found:**
- Ensure Python is installed and added to PATH
- Run `python --version` to verify

**Wrong Python version:**
```bash
python3 -m venv venv  # Use python3 explicitly
```
</details>

<details>
<summary><b>Module Not Found Errors</b></summary>

Ensure you:
1. ✅ Activated the virtual environment
2. ✅ Installed dependencies: `pip install fastapi uvicorn`
3. ✅ Are in the correct directory
4. ✅ Using the correct Python interpreter

Check active environment:
```bash
which python  # macOS/Linux
where python  # Windows
```
</details>

<details>
<summary><b>Frontend Won't Start</b></summary>

**Node modules error:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 in use:**
```bash
# Vite will automatically try next available port
npm run dev
```
</details>

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

## 🔧 Contributing Guide

We welcome contributions! Follow this workflow to contribute to PORTIA.

### Git Workflow

#### 1️⃣ Fork & Clone
```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/portia-compiler.git
cd portia-compiler

# Add upstream remote to sync with main repo
git remote add upstream https://github.com/DanielHC16/portia-compiler.git
```

#### 2️⃣ Create a Feature Branch
```bash
# Always branch from main
git checkout main
git pull upstream main

# Create your feature branch
git checkout -b feature/your-feature-name
# Examples:
#   feature/add-syntax-analyzer
#   fix/lexer-comment-bug
#   docs/update-readme
```

#### 3️⃣ Make Your Changes
```bash
# Make your code changes
# Test your changes locally

# Check what files changed
git status

# View your changes
git diff
```

#### 4️⃣ Commit Your Changes
```bash
# Stage your changes
git add .
# Or stage specific files:
git add lexer-backend/app/lexer/lexer.py

# Commit with a descriptive message
git commit -m "Add: feature description"
# Examples:
#   git commit -m "Add: multi-line comment support in lexer"
#   git commit -m "Fix: error highlighting not resetting on reset button"
#   git commit -m "Docs: update installation instructions"
```

#### 5️⃣ Push & Create Pull Request
```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request from your fork to the main repo
```

#### 6️⃣ Keep Your Fork Updated
```bash
# Switch to main branch
git checkout main

# Fetch and merge upstream changes
git fetch upstream
git merge upstream/main

# Push updates to your fork
git push origin main

# Update your feature branch (if needed)
git checkout feature/your-feature-name
git rebase main
```

### Making Changes

#### Adding a New Feature
```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature
```

#### Fixing a Bug
```bash
git checkout -b fix/bug-description
# Fix the bug
git add .
git commit -m "Fix: bug description and solution"
git push origin fix/bug-description
```

#### Updating Documentation
```bash
git checkout -b docs/what-you-updated
# Update docs
git add README.md
git commit -m "Docs: describe what was updated"
git push origin docs/what-you-updated
```

### Best Practices

#### ✅ DO:
- Create a new branch for each feature/fix
- Write clear, descriptive commit messages
- Test your changes before committing
- Keep commits focused and atomic
- Pull latest changes before starting work
- Update documentation if needed

#### ❌ DON'T:
- Commit directly to `main` branch
- Commit large, unrelated changes together
- Include generated files (`.gitignore` handles this)
- Push sensitive data (API keys, passwords)
- Commit without testing

### What the `.gitignore` Excludes

The [`.gitignore`](.gitignore) automatically prevents committing:

| Category | Files |
|----------|-------|
| **Python** | `venv/`, `.venv/`, `__pycache__/`, `*.pyc` |
| **Node.js** | `node_modules/`, `dist/`, `*.log` |
| **IDEs** | `.vscode/*`, `.idea/`, `*.suo` |
| **OS** | `.DS_Store`, `Thumbs.db` |
| **Env** | `.env`, `.env.local` |

### Commit Message Format

Use this format for consistency:

```
<type>: <short description>

[optional detailed description]

[optional breaking changes]
```

**Types:**
- `Add:` - New feature or functionality
- `Fix:` - Bug fix
- `Update:` - Modify existing feature
- `Docs:` - Documentation changes
- `Style:` - Code style/formatting (no logic change)
- `Refactor:` - Code restructuring (no behavior change)
- `Test:` - Adding or updating tests
- `Chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "Add: syntax tree visualization"
git commit -m "Fix: reset button not clearing errors"
git commit -m "Update: improve error highlighting performance"
git commit -m "Docs: add contributing guidelines to README"
```

---

## 🔧 Git Best Practices

### Understanding `.gitignore`
The repository includes a comprehensive [`.gitignore`](.gitignore) file that automatically excludes:

- **Python files**: Virtual environments (`venv/`, `.venv/`), compiled files (`__pycache__/`, `*.pyc`)
- **Node.js files**: Dependencies (`node_modules/`), build outputs (`dist/`)
- **IDE files**: Editor-specific configurations and caches
- **OS files**: System-generated files (`.DS_Store`, `Thumbs.db`)
- **Environment files**: `.env` files containing sensitive data

### Setting Up Git After Cloning

After cloning, you can start contributing:

```bash
# Check current status
git status

# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Make your changes, then stage them
git add .

# Commit with a descriptive message
git commit -m "Add: your feature description"

# Push to your branch
git push origin feature/your-feature-name
```

### What NOT to Commit

The `.gitignore` file handles this automatically, but be aware:

❌ **Never commit:**
- Virtual environments (`venv/`, `.venv/`)
- `node_modules/` directory
- Build outputs (`dist/`, `__pycache__/`)
- Environment variables (`.env` files)
- IDE-specific settings (except shared configurations)
- Compiled Python files (`*.pyc`, `*.pyo`)

✅ **Always commit:**
- Source code files (`.py`, `.ts`, `.tsx`)
- Configuration files (`package.json`, `tsconfig.json`)
- Documentation (`README.md`, comments)
- Shared VSCode settings (`.vscode/settings.json`)

### Keeping Your Fork Updated

If you've forked the repository:

```bash
# Add upstream remote (only needed once)
git remote add upstream https://github.com/DanielHC16/portia-compiler.git

# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your main branch
git checkout main
git merge upstream/main

# Push updates to your fork
git push origin main
```

---

## 📋 TODO List

### Backend
- [ ] Verify lexer correctness against full PORTIA spec
- [ ] Double‑check token classification
- [ ] Add robust error handling and edge‑case coverage
- [ ] Implement parser (syntax analyzer)
- [ ] Implement semantic analyzer

### Frontend
- [ ] Add syntax tree visualization
- [ ] Enhanced error messages with suggestions
- [ ] Code completion support
- [ ] Export/import code functionality

### General
- [ ] Complete CFG (Context-Free Grammar) definition
- [ ] Add comprehensive test suite
- [ ] Create language specification document
- [ ] Add example PORTIA programs

---

## 📄 License

This project is part of an academic requirement for BSCS 3-3 A.Y. 2025-2026.

---

## 👥 Team LoomVI

**BSCS 3-3 | A.Y. 2025-2026**

For questions or contributions, please open an issue or submit a pull request.

---

<div align="center">

**[⬆ Back to Top](#portia-programming-language)**

Made with 🕷️ by Team LoomVI

</div>
