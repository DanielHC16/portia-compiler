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

### 1. Clone the repository
```bash
git clone https://github.com/<your-org>/portia.git
cd portia
```

### 2. Setup the backend
```bash
cd backend python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate pip install -r requirements.txt
```

### 3. Run the backend
```bash
uvicorn app.main:app --reload
```
or
```bash
npm start
```
### 4. Set up the frontend (React + Vite + TypeScript)
```bash
cd ../frontend npm install
```

### 5. Run the frontend
```bash
npm run dev
```

TODO List
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
