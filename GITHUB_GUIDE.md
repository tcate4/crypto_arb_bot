# Pushing Your Cryptocurrency Arbitrage Bot to GitHub

This guide provides step-by-step instructions for pushing your cryptocurrency arbitrage bot to GitHub.

## Prerequisites

Before pushing your code to GitHub, you need:

1. **Git**: Installed on your system
2. **GitHub Account**: Create one at [github.com](https://github.com) if you don't have one
3. **GitHub CLI** (optional): For easier authentication

## Important: Protecting Sensitive Information

Your repository contains sensitive API keys in `kraken_api.txt` and potentially other files. Before pushing to GitHub:

1. **Add sensitive files to .gitignore**:
   ```
   # Add to .gitignore
   kraken_api.txt
   .env
   bot.log
   ```

2. **Remove sensitive information from tracked files**:
   If you've already committed sensitive files, you'll need to remove them from Git's history.

## Step-by-Step Guide

### 1. Initialize Git Repository

```powershell
# Navigate to your project directory
cd C:\Users\T\PycharmProjects\crypto-arb-bot

# Initialize Git repository
git init
```

### 2. Create .gitignore File

Create a `.gitignore` file to exclude sensitive files:

```powershell
# Create .gitignore file
@"
# Sensitive information
kraken_api.txt
.env
bot.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db
"@ | Out-File -FilePath .gitignore -Encoding utf8
```

### 3. Add Files to Git

```powershell
# Add all files except those in .gitignore
git add .

# Verify what will be committed
git status
```

### 4. Make Initial Commit

```powershell
# Commit the files
git commit -m "Initial commit of cryptocurrency arbitrage bot"
```

### 5. Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the "+" icon in the top-right corner and select "New repository"
3. Enter a repository name (e.g., "crypto-arb-bot")
4. Choose public or private repository
5. Do NOT initialize with README, .gitignore, or license (we'll push our existing code)
6. Click "Create repository"

### 6. Link Local Repository to GitHub

After creating the repository, GitHub will show commands to push an existing repository. Use these commands:

```powershell
# Add the GitHub repository as remote
git remote add origin https://github.com/yourusername/crypto-arb-bot.git

# Push your code to GitHub
git push -u origin master
```

If you're using `main` as your default branch instead of `master`:

```powershell
git push -u origin main
```

### 7. Authentication

When pushing to GitHub, you'll need to authenticate:

#### Option 1: Username and Password/Token
- If you have two-factor authentication enabled, you'll need to use a personal access token instead of your password
- Create a token at GitHub → Settings → Developer settings → Personal access tokens

#### Option 2: GitHub CLI
```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Login to GitHub
gh auth login

# Follow the prompts to authenticate
```

#### Option 3: SSH Keys
```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to ssh-agent
# Start the ssh-agent in the background
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add the SSH key to your GitHub account
# Copy the SSH key to your clipboard
clip < ~/.ssh/id_ed25519.pub

# Then add it in GitHub → Settings → SSH and GPG keys
```

### 8. Verify the Push

After pushing, refresh your GitHub repository page to verify that your code has been uploaded successfully.

## Updating Your Repository

After making changes to your code:

```powershell
# Check what files have changed
git status

# Add the changes
git add .

# Commit the changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Setting Up GitHub Actions (Optional)

You can set up GitHub Actions to automatically test or deploy your bot:

1. Create a `.github/workflows` directory in your repository
2. Add a workflow file (e.g., `test.yml`) with your CI/CD configuration

## Best Practices for Maintaining Your Repository

1. **Regular Updates**: Commit and push changes regularly
2. **Meaningful Commit Messages**: Write clear, descriptive commit messages
3. **Branching**: Use branches for new features or bug fixes
4. **Pull Requests**: Use pull requests for code review before merging to main branch
5. **Documentation**: Keep README.md and other documentation up to date
6. **Security**: Never commit sensitive information like API keys

## Troubleshooting

### Authentication Issues
- Ensure you're using the correct username and password/token
- If using SSH, verify your SSH key is added to your GitHub account

### Push Rejected
- Pull the latest changes before pushing: `git pull origin main --rebase`
- Force push (use with caution): `git push -f origin main`

### Large Files
- GitHub has a file size limit of 100 MB
- For larger files, consider using Git LFS or exclude them from the repository
