# GitHub Upload Instructions

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `DocGenius`
   - **Description**: "AI Document Assistant - 100% Private, Offline Q&A with PDFs/DOCX using Ollama + LangChain"
   - **Visibility**: Public (or Private if you prefer)
   - ⚠️ **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Link Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Set your remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/DocGenius.git

# Rename branch to main (optional, if you prefer main over master)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Or if you kept the master branch:
```bash
git remote add origin https://github.com/YOUR-USERNAME/DocGenius.git
git push -u origin master
```

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed automatically on the repository homepage

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Open GitHub Desktop
3. Go to **File** → **Add Local Repository**
4. Select the DocGenius folder
5. Click **Publish repository**
6. Choose visibility (public/private) and click **Publish**

## Step 4: Update README (Optional)

After uploading, you might want to update the README to replace:
- `https://github.com/yourusername/DocGenius.git` with your actual repository URL
- Add screenshots or demo GIFs
- Add your contact information

## Future Updates

When you make changes to your code:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with a message
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Common Git Commands

```bash
# View commit history
git log --oneline

# Check repository status
git status

# View remote URL
git remote -v

# Pull latest changes (if working with others)
git pull
```

## Troubleshooting

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/DocGenius.git
```

**Error: "failed to push some refs"**
```bash
git pull origin main --rebase
git push origin main
```

**Authentication Issues**
- Use GitHub Personal Access Token instead of password
- Or set up SSH keys for easier authentication

## Next Steps

After uploading to GitHub:
1. ⭐ Consider adding a `CHANGELOG.md` to track version changes
2. 📸 Add screenshots to make README more attractive
3. 🏷️ Create releases/tags for versions
4. 📊 Add GitHub Actions for CI/CD (optional)
5. 🎨 Add repository topics/tags for discoverability

---

**Your repository is ready to go! 🚀**
