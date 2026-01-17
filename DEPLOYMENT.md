# Deploying Smart Resume Analyzer to Streamlit Cloud

This guide will help you deploy your Smart Resume Analyzer to Streamlit Cloud for free.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Streamlit Cloud account (free - sign up at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Prepare Your Repository

Ensure your repository has these files:

```
smartresumeanlyzer/
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── download_nltk_data.py       # NLTK data downloader (optional)
├── packages.txt                # System packages (can be empty)
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── README.md                   # Documentation
```

### Key Files for Deployment:

#### 1. **requirements.txt** ✅
Already configured with all necessary dependencies:
- streamlit
- pandas
- pdfplumber
- docx2txt
- scikit-learn
- sentence-transformers
- nltk
- torch
- transformers
- numpy

#### 2. **packages.txt** ✅
Created (empty) - no system-level packages needed for this app.

#### 3. **.streamlit/config.toml** ✅
Already configured with your premium dark theme.

#### 4. **app.py** ✅
Updated with robust NLTK data downloading that works on Streamlit Cloud.

## Step 2: Push to GitHub

If you haven't already, push your code to GitHub:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Streamlit Cloud deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign in**: Use your GitHub account to sign in

3. **Create New App**:
   - Click "New app" button
   - Select your repository
   - Choose the branch (usually `main`)
   - Set the main file path: `app.py`
   - Click "Deploy"

4. **Wait for Deployment**:
   - Streamlit Cloud will install dependencies (this takes 2-5 minutes on first deployment)
   - NLTK data will be downloaded automatically during startup
   - The sentence transformer model will be downloaded on first run

## Step 4: Configure Advanced Settings (Optional)

In Streamlit Cloud dashboard:

1. Click the three dots (⋮) next to your app
2. Select "Settings"
3. You can configure:
   - **Python version**: 3.9+ recommended
   - **Secrets**: Add any API keys if needed in future
   - **Resources**: Adjust if needed (free tier is sufficient)

## Important Notes for Cloud Deployment

### ✅ What's Already Handled:

1. **NLTK Data**: The app now downloads required NLTK data automatically on startup
2. **SSL Certificates**: Handled for cloud environments
3. **Model Caching**: Sentence transformer model is cached using `@st.cache_resource`
4. **Theme**: Premium dark theme is pre-configured

### ⚠️ First Run Considerations:

- **Initial Load Time**: First deployment takes 2-5 minutes
- **Model Download**: The sentence-transformers model (~90MB) downloads on first run
- **Subsequent Loads**: Much faster due to caching

### 🔧 Troubleshooting:

If you encounter issues:

1. **Check Logs**: In Streamlit Cloud, click "Manage app" → "Logs" to see detailed error messages

2. **NLTK Errors**: If NLTK data fails to download, the app will print warnings but continue running

3. **Memory Issues**: The free tier has 1GB RAM. If you hit limits:
   - The app is optimized to use `all-MiniLM-L6-v2` (small model)
   - Consider upgrading to Streamlit Cloud Pro if needed

4. **Torch Installation**: PyTorch is large (~700MB). Deployment may take longer but should succeed.

## Your App URL

After deployment, your app will be available at:
```
https://YOUR_USERNAME-YOUR_REPO_NAME-BRANCH-HASH.streamlit.app
```

You can customize this URL in Streamlit Cloud settings.

## Updating Your App

Any push to your GitHub repository will automatically trigger a redeployment:

```bash
# Make changes to your code
git add .
git commit -m "Update feature X"
git push
```

Streamlit Cloud will detect the changes and redeploy automatically.

## Sharing Your App

Once deployed, you can share your app URL with anyone! No authentication required for viewers.

## Cost

- **Free Tier**: Sufficient for this app
  - 1 GB RAM
  - 1 CPU
  - Unlimited viewers
  - Community support

- **Upgrade Options**: Available if you need more resources

## Support

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)

---

## Quick Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` is complete
- [ ] `packages.txt` exists (can be empty)
- [ ] `.streamlit/config.toml` configured
- [ ] Signed up for Streamlit Cloud
- [ ] Created new app in Streamlit Cloud
- [ ] Deployment successful
- [ ] Tested app functionality
- [ ] Shared app URL

---

**Ready to deploy!** 🚀

Your Smart Resume Analyzer is now cloud-ready and will work seamlessly on Streamlit Cloud.
