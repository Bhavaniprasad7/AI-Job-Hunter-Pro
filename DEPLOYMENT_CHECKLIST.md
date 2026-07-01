# Streamlit Cloud Deployment Checklist

Complete this checklist before deploying **AI Job Hunter Pro** to Streamlit Cloud.

## Pre-Deployment ✅

- [ ] Run health check: `python health_check.py` (all tests pass)
- [ ] Test locally: `streamlit run streamlit_app.py` (dashboard loads)
- [ ] Verify `config/config.yaml` has at least one job source configured
- [ ] All code committed to `main` branch: `git push origin main`

## GitHub Setup

- [ ] GitHub repository created: https://github.com/your-username/AI-Job-Hunter-Pro
- [ ] Repository is **public** (required for free Streamlit Cloud)
- [ ] All files pushed to `main` branch
- [ ] `.gitignore` configured (secrets not committed)

**Verify with:**
```bash
git remote -v  # Should show your GitHub repo
git branch -a  # Should show main branch
```

## Streamlit Cloud Setup

### Account & App Creation

- [ ] Streamlit Cloud account created at https://share.streamlit.io
- [ ] GitHub account connected to Streamlit Cloud
- [ ] New app created with:
  - **Repository:** `your-username/AI-Job-Hunter-Pro`
  - **Branch:** `main`
  - **Main file path:** `streamlit_app.py`

### Secrets Configuration

After app is created, configure secrets:

1. Click **☰ (menu)** in top-right → **Settings**
2. Go to **Secrets** tab
3. Paste this and fill in actual values:

```toml
# REQUIRED - OpenAI API key (get from https://platform.openai.com/api-keys)
OPENAI_API_KEY = "sk-..."

# OPTIONAL - Enable email delivery
EMAIL_ENABLED = false
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
EMAIL_USERNAME = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-specific-password"
EMAIL_RECIPIENTS = ["recipient@example.com"]
```

**Important:** 
- For Gmail, use [app-specific password](https://myaccount.google.com/apppasswords), NOT your regular password
- Each secret should be on its own line

- [ ] `OPENAI_API_KEY` configured and saved
- [ ] Optional email secrets configured (if email delivery needed)
- [ ] App restarted after secrets saved

## Testing on Streamlit Cloud

After deployment:

- [ ] Dashboard loads at your Streamlit Cloud URL
- [ ] Filters appear in sidebar
- [ ] Jobs display (may take 1-2 min on first load)
- [ ] No error messages in logs (check **☰** → **Manage app** → **Settings** → **Logs**)

## Customization (Optional)

### Job Sources

To modify job search criteria:

1. Edit `config/config.yaml`
2. Update job source queries and locations
3. Commit and push: `git push origin main`
4. Streamlit Cloud auto-redeploys

Example:
```yaml
job_sources:
  - name: python_jobs
    plugin: indeed
    settings:
      query: "Senior Python Developer"
      location: "San Francisco"
      max_pages: 2
```

### Dashboard Styling

Edit `.streamlit/config.toml` to customize:
- Colors (primaryColor, backgroundColor)
- Font and layout
- Page configuration

### Database

**⚠️ Important:** 
- SQLite database is **NOT persisted** in Streamlit Cloud
- Each app restart re-initializes the database
- To persist data, migrate to a cloud database (PostgreSQL, MySQL, etc.)

## Monitoring & Troubleshooting

### View Logs

1. Click **☰** menu
2. Select **Manage app**
3. Go to **Settings** → **Logs**

### Common Issues

| Issue | Solution |
|-------|----------|
| App crashes on load | Check logs, verify OPENAI_API_KEY in secrets |
| "No jobs found" | Ensure job sources in config/config.yaml have valid queries |
| Email not sending | Check EMAIL_ENABLED=true and SMTP credentials in secrets |
| Slow first load | Normal - job collection takes 1-3 minutes on first run |

### Reset App

If the app gets into a bad state:

1. Click **☰** → **Rerun**
2. Or click **☰** → **Always rerun**
3. Or restart from Streamlit Cloud dashboard

## Post-Deployment

### Share the App

Your app URL: `https://share.streamlit.io/your-username/AI-Job-Hunter-Pro`

Share with:
- [ ] Team members
- [ ] Stakeholders
- [ ] Friends

### Monitor Performance

After deployment, monitor:
- [ ] Daily job collection success
- [ ] Dashboard load times
- [ ] Error logs (weekly)
- [ ] Job source availability

### Future Improvements

Consider implementing:
- [ ] Cloud database for persistence
- [ ] Background job scheduling
- [ ] User authentication
- [ ] Resume upload and matching
- [ ] Automated daily email reports
- [ ] Export to ATS systems

## Support

If you encounter issues:

1. **Check local first:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Review logs:**
   - Streamlit Cloud: **☰** → **Manage app** → **Logs**
   - Local: Terminal output

3. **Common solutions:**
   - Ensure Python 3.10+ (see requirements.txt)
   - Clear browser cache (Ctrl+Shift+Delete)
   - Restart app from Streamlit Cloud dashboard
   - Check GitHub repo for latest code

4. **Debug:**
   - Run `python health_check.py` locally
   - Test collectors: `python -c "from src.ai_job_hunter_pro.use_cases.collect_jobs import JobCollectorService; ..."`

## Documentation

- **DEPLOYMENT.md** - Detailed deployment steps
- **README.md** - Quick start and features
- **config/config.yaml** - Configuration examples
- **health_check.py** - System validation script

---

✅ **You're ready to deploy!** Proceed to Streamlit Cloud and follow the setup steps above.

**Questions?** Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
