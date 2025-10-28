# 🔧 Contributing Guide

We welcome contributions to PORTIA! This guide will help you get started with contributing to the project.

---

## Git Workflow

### 1️⃣ Fork & Clone

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/portia-compiler.git
cd portia-compiler

# Add upstream remote to sync with main repo
git remote add upstream https://github.com/DanielHC16/portia-compiler.git
```

### 2️⃣ Create a Feature Branch

```bash
# Always branch from main
git checkout main
git pull upstream main

# Create your feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features (e.g., `feature/add-syntax-analyzer`)
- `fix/` - Bug fixes (e.g., `fix/lexer-comment-bug`)
- `docs/` - Documentation updates (e.g., `docs/update-readme`)
- `refactor/` - Code refactoring (e.g., `refactor/lexer-cleanup`)
- `test/` - Adding tests (e.g., `test/add-parser-tests`)

### 3️⃣ Make Your Changes

```bash
# Make your code changes
# Test your changes locally

# Check what files changed
git status

# View your changes
git diff
```

### 4️⃣ Commit Your Changes

```bash
# Stage your changes
git add .
# Or stage specific files:
git add lexer-backend/app/lexer/lexer.py

# Commit with a descriptive message
git commit -m "Add: feature description"
```

See [Commit Message Format](#commit-message-format) below for guidelines.

### 5️⃣ Push & Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request from your fork to the main repository.

### 6️⃣ Keep Your Fork Updated

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

---

## Making Changes

### Adding a New Feature

```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature
```

### Fixing a Bug

```bash
git checkout -b fix/bug-description
# Fix the bug
git add .
git commit -m "Fix: bug description and solution"
git push origin fix/bug-description
```

### Updating Documentation

```bash
git checkout -b docs/what-you-updated
# Update docs
git add README.md
git commit -m "Docs: describe what was updated"
git push origin docs/what-you-updated
```

---

## Commit Message Format

Use this format for consistency:

```
<type>: <short description>

[optional detailed description]
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `Add:` | New feature or functionality | `Add: syntax tree visualization` |
| `Fix:` | Bug fix | `Fix: reset button not clearing errors` |
| `Update:` | Modify existing feature | `Update: improve error highlighting` |
| `Docs:` | Documentation changes | `Docs: add contributing guidelines` |
| `Style:` | Code style/formatting | `Style: format code with prettier` |
| `Refactor:` | Code restructuring | `Refactor: simplify lexer logic` |
| `Test:` | Adding or updating tests | `Test: add lexer edge cases` |
| `Chore:` | Maintenance tasks | `Chore: update dependencies` |

### Examples

```bash
git commit -m "Add: multi-line comment support in lexer"
git commit -m "Fix: error highlighting not resetting on reset button"
git commit -m "Update: reduce debounce delay to 50ms for faster highlighting"
git commit -m "Docs: add installation instructions for macOS"
git commit -m "Refactor: extract token classification into separate function"
```

---

## Best Practices

### ✅ DO:

- ✅ Create a new branch for each feature/fix
- ✅ Write clear, descriptive commit messages
- ✅ Test your changes before committing
- ✅ Keep commits focused and atomic
- ✅ Pull latest changes before starting work
- ✅ Update documentation if needed
- ✅ Add comments for complex logic
- ✅ Follow existing code style
- ✅ Write tests for new features

### ❌ DON'T:

- ❌ Commit directly to `main` branch
- ❌ Commit large, unrelated changes together
- ❌ Include generated files (`.gitignore` handles this)
- ❌ Push sensitive data (API keys, passwords)
- ❌ Commit without testing
- ❌ Use vague commit messages ("fixed stuff", "updates")
- ❌ Break existing functionality
- ❌ Ignore linting errors

---

## What the `.gitignore` Excludes

The [`.gitignore`](../.gitignore) automatically prevents committing:

| Category | Files |
|----------|-------|
| **Python** | `venv/`, `.venv/`, `__pycache__/`, `*.pyc` |
| **Node.js** | `node_modules/`, `dist/`, `*.log` |
| **IDEs** | `.vscode/*`, `.idea/`, `*.suo` |
| **OS** | `.DS_Store`, `Thumbs.db` |
| **Env** | `.env`, `.env.local` |

### What TO Commit

✅ **Always commit:**
- Source code files (`.py`, `.ts`, `.tsx`)
- Configuration files (`package.json`, `tsconfig.json`)
- Documentation (`README.md`, `.md` files)
- Shared VSCode settings (`.vscode/settings.json`)
- Test files
- Scripts

---

## Code Style Guidelines

### Python
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### TypeScript/React
- Use functional components with hooks
- Follow existing naming conventions
- Use TypeScript types, avoid `any`
- Keep components small and reusable

---

## Pull Request Guidelines

When creating a Pull Request:

1. **Title**: Use the same format as commit messages
   - Example: `Add: syntax tree visualization component`

2. **Description**: Include:
   - What changes you made
   - Why you made them
   - How to test them
   - Screenshots (if UI changes)

3. **Link Issues**: Reference related issues
   - Example: `Fixes #123` or `Closes #45`

4. **Checklist**:
   ```markdown
   - [ ] Code follows project style guidelines
   - [ ] All tests pass
   - [ ] Documentation updated (if needed)
   - [ ] No merge conflicts
   - [ ] Tested locally
   ```

---

## Getting Help

- 📫 Open an [issue](https://github.com/DanielHC16/portia-compiler/issues) for bugs or questions
- 💬 Join discussions in pull requests
- 📚 Check existing issues before creating new ones

---

## Additional Resources

- [Installation Guide](INSTALLATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Main README](../README.md)

---

**Thank you for contributing to PORTIA! 🕷️**

[← Back to README](../README.md)
