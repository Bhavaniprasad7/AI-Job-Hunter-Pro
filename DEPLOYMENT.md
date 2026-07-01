# Streamlit Cloud Deployment Guide

This guide provides step-by-step instructions for deploying **AI Job Hunter Pro** to Streamlit Cloud.

## Prerequisites

- A GitHub account (for connecting the repository)
- A Streamlit Cloud account (free at https://streamlit.io/cloud)
- The source code pushed to GitHub in the `main` branch
- Required secrets prepared (API keys, email credentials)

## Local Testing Before Deployment

Before deploying to Streamlit Cloud, test the application locally:

```bash
# From the repository root
streamlit run streamlit_app.py
```

This should:
1. Load the dashboard with styling
2. Display the Streamlit interface on `http://localhost:8501`
3. Load jobs from configured sources (if any)
4. Show filtering options in the sidebar

**Troubleshooting Local Errors:**
- If you get import errors, ensure `src/` is in Python path (done automatically by `streamlit_app.py`)
- If jobs don't load, check `config/config.yaml` for valid job sources and API keys
- If the dashboard crashes, check the terminal for detailed error messages

## Deployment Steps

### Step 1: Prepare the GitHub Repository

1. Ensure all code is committed and pushed to `main` branch:
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. Verify the repo structure on GitHub:
   - `streamlit_app.py` exists in the root directory
   - `.streamlit/config.toml` exists
   - `requirements.txt` is in the root directory
   - `config/config.yaml` contains valid job sources

### Step 2: Create Streamlit Cloud App

1. Go to https://share.streamlit.io
2. Click **"New app"** button
3. Select your GitHub repository
4. Specify these settings:
   - **Repository:** `your-username/AI-Job-Hunter-Pro`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Click **"Deploy"** button

Streamlit will automatically:
- Install dependencies from `requirements.txt`
- Run `streamlit run streamlit_app.py`
- Deploy the app (this takes 1-3 minutes)

### Step 3: Configure Secrets

After deployment, the app will appear with a "No secrets" warning. Configure them:

1. Click the **☰ (menu)** button in the top-right
2. Select **Settings**
3. Go to the **Secrets** tab
4. Copy the contents of `.streamlit/secrets.toml.example`:
   ```toml
   OPENAI_API_KEY = "your-api-key"
   EMAIL_ENABLED = true
   EMAIL_SMTP_SERVER = "smtp.gmail.com"
   EMAIL_SMTP_PORT = 587
   EMAIL_USERNAME = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-app-specific-password"
   EMAIL_RECIPIENTS = ["recipient@example.com"]
   ```
5. Replace placeholders with actual values
6. Click **Save**

The app will automatically restart with the new secrets.

### Step 4: Configure Job Sources

1. Update `config/config.yaml` in your repository with your desired job sources:
   ```yaml
   job_sources:
     - type: naukri
       enabled: true
       query: "Azure Integration Developer"
       location: "India"
       max_pages: 3
     - type: indeed
       enabled: true
       query: "Azure Developer"
       location: "United States"
   ```

2. Commit and push changes:
   ```bash
   git add config/config.yaml
   git commit -m "Update job sources"
   git push origin main
   ```

3. Streamlit Cloud will automatically redeploy (check the "Manage app" section for deployment status)

## Environment Variables

The application supports these environment variables for cloud deployment:

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_KEY` | Required for job matching | `sk-...` |
| `EMAIL_ENABLED` | Enable/disable email | `true`/`false` |
| `EMAIL_SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | SMTP port | `587` |
| `EMAIL_USERNAME` | Email account | `user@gmail.com` |
| `EMAIL_PASSWORD` | Email password or app-specific password | `xxxx xxxx xxxx xxxx` |
| `EMAIL_RECIPIENTS` | Email recipients (comma-separated) | `user@example.com` |
| `AI_JOB_HUNTER_CONFIG_PATH` | Config file path | `config/config.yaml` |

**Note:** For Gmail, use an [app-specific password](https://myaccount.google.com/apppasswords) instead of your regular password.

## Important Considerations for Streamlit Cloud

### 1. **Storage**
- Streamlit Cloud runs in an **ephemeral file system**
- The SQLite database (`jobs.db`) is NOT persisted between app restarts
- For persistent storage, consider:
  - Hosting a database (PostgreSQL, Cloud SQL, etc.)
  - Using a cloud storage service (S3, GCS, etc.)
  - Re-collecting jobs on each run (simple but slower)

### 2. **Rate Limiting**
- Portal scrapers (Naukri, Indeed) may rate-limit requests
- The app includes backoff in collectors
- To avoid blocking, set `max_pages: 2-3` per source

### 3. **Performance**
- The first load will be slow as it collects jobs
- Subsequent reloads (with cache) will be faster
- For production, implement a background job collector

### 4. **Logs**
- View logs in Streamlit Cloud by clicking the **☰** menu → **Manage app** → **Settings** → **Logs**
- Logs are cleared when the app restarts

## Monitoring and Troubleshooting

### Common Issues

**Issue:** App shows "No jobs found"
- **Solution:** Check `config/config.yaml` has `enabled: true` for at least one source
- Check job source credentials and connectivity

**Issue:** "OpenAI API key not found"
- **Solution:** Ensure `OPENAI_API_KEY` is set in Streamlit Cloud secrets
- Restart the app (click **☰** → **Always rerun** or clear cache)

**Issue:** Email not sending
- **Solution:** Check `EMAIL_ENABLED = true` in secrets
- Verify SMTP credentials are correct
- Check spam/junk folders
- For Gmail, ensure app-specific password is used

**Issue:** Collector is very slow
- **Solution:** Reduce `max_pages` in `config/config.yaml`
- Consider disabling slow sources (LinkedIn)

### Logs

Check app logs for detailed errors:
1. Click **☰** menu in top-right
2. Select **Manage app**
3. Select **Settings**
4. Go to **Logs** tab

## Next Steps

1. **Enhance UI:** Customize colors and layout in `.streamlit/config.toml`
2. **Add Persistence:** Migrate to a cloud database
3. **Schedule Jobs:** Use a background service to collect jobs periodically
4. **Advanced Filtering:** Add resume upload and matching in the dashboard
5. **Export Reports:** Integrate Excel report generation with email delivery

## Support

For issues or questions:
- Check Streamlit documentation: https://docs.streamlit.io
- Review app logs for error details
- Test locally with `streamlit run streamlit_app.py` before deploying
