# AI Job Hunter Pro

🔍 **An intelligent job search platform that collects jobs from multiple portals, filters by skills and preferences, and generates matching reports.**

## Features

✅ **Multi-Portal Job Scraping**
- Naukri.com (India's largest job portal)
- Indeed.com (Global job site)
- LinkedIn (with configurable selectors)
- Company career pages (generic scraper)
- RSS feeds (custom job feeds)

✅ **Intelligent Job Filtering**
- Filter by experience level
- Skills-based matching (any/all)
- Fortune 500 company filtering
- Location and company preferences
- Salary range filtering

✅ **AI-Powered Job Matching**
- OpenAI-powered resume-job matching
- ATS score calculation
- Comprehensive match reports

✅ **Email Delivery & Reports**
- Daily summary emails
- Excel report generation
- Job match attachments
- SMTP configuration support

✅ **Dashboard & Analytics**
- Streamlit-based web interface
- Interactive filters
- Job and match visualization
- Cloud-ready deployment

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/AI-Job-Hunter-Pro.git
   cd AI-Job-Hunter-Pro
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure job sources:**
   Edit `config/config.yaml` and set up your desired job sources:
   ```yaml
   job_sources:
     - type: naukri
       enabled: true
       query: "Python Developer"
       location: "Bangalore"
   ```

5. **Run the dashboard:**
   ```bash
   streamlit run streamlit_app.py
   ```

   The app will open at `http://localhost:8501`

### Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive Streamlit Cloud deployment instructions.

Quick summary:
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets (OpenAI API key, email credentials)
4. Deploy!

## Configuration

### config/config.yaml

```yaml
# OpenAI settings
openai_api_key: "your-key-here"
openai_model: "gpt-4"

# Database
database_url: "sqlite:///jobs.db"

# Job sources
job_sources:
  - type: naukri
    enabled: true
    query: "Azure Developer"
    location: "India"
    max_pages: 3
  - type: indeed
    enabled: true
    query: "Cloud Engineer"
    location: "United States"

# Filtering
filter:
  experience_min: 5
  experience_max: 15
  skills_all: ["Azure", "Python"]
  skills_any: ["Kubernetes", "Docker"]
  fortune_500_only: true

# Email (optional)
email:
  enabled: false
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender: "noreply@example.com"
```

## Project Structure

```
AI-Job-Hunter-Pro/
├── src/ai_job_hunter_pro/
│   ├── adapters/              # External service adapters
│   │   ├── portal_collectors.py    # Job portal scrapers
│   │   ├── email_sender.py         # SMTP email service
│   │   └── sqldb.py               # Database layer
│   ├── domain/                # Core business logic
│   │   ├── entities.py            # JobPost, Resume models
│   │   └── ports.py               # Interface definitions
│   ├── use_cases/             # Application services
│   │   ├── collect_jobs.py        # Job collection orchestration
│   │   ├── filter_jobs.py         # Job filtering logic
│   │   └── email_summary.py       # Email delivery service
│   ├── ui/                    # User interfaces
│   │   └── streamlit_app.py       # Web dashboard
│   └── config/                # Configuration
│       ├── loader.py              # Config file parser
│       └── settings.py            # Pydantic models
├── config/
│   └── config.yaml            # Job search configuration
├── streamlit_app.py           # Cloud entry point
├── requirements.txt           # Python dependencies
└── DEPLOYMENT.md              # Cloud deployment guide
```

## Supported Job Portals

| Portal | Status | Notes |
|--------|--------|-------|
| Naukri.com | ✅ Fully Functional | India-focused, high volume |
| Indeed.com | ✅ Fully Functional | Global coverage |
| LinkedIn | ⚠️ Requires tuning | Anti-bot protection may apply |
| Company Pages | ✅ Functional | Generic scraper, configurable |
| RSS Feeds | ✅ Functional | Custom feed URLs |

## CLI Usage

Collect jobs and generate daily summary:

```bash
python -m ai_job_hunter_pro.main collect-and-email
```

Or use Python directly:

```python
from ai_job_hunter_pro.config.loader import load_config
from ai_job_hunter_pro.use_cases.collect_jobs import JobCollectorService

config = load_config("config/config.yaml")
collector = JobCollectorService(config)
jobs = collector.collect()
print(f"Collected {len(jobs)} jobs")
```

## Requirements

- Python 3.10+
- Dependencies: See [requirements.txt](requirements.txt)

**Key Libraries:**
- `streamlit>=1.30.0` - Web dashboard
- `pydantic>=2.5.2` - Configuration validation
- `sqlalchemy>=2.0` - Database ORM
- `openai>=1.0` - AI matching
- `requests`, `beautifulsoup4` - Web scraping
- `pandas`, `openpyxl` - Excel reports

## Environment Variables

```bash
# Required for job matching
OPENAI_API_KEY="sk-..."

# For email delivery
EMAIL_SMTP_SERVER="smtp.gmail.com"
EMAIL_SMTP_PORT="587"
EMAIL_USERNAME="your-email@gmail.com"
EMAIL_PASSWORD="your-app-password"
EMAIL_RECIPIENTS="recipient@example.com"

# Optional
AI_JOB_HUNTER_CONFIG_PATH="config/config.yaml"
```

## API Key Setup

### OpenAI API Key

1. Sign up at https://platform.openai.com/signup
2. Create API key at https://platform.openai.com/api-keys
3. Set in `config/config.yaml` or environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

### Gmail Setup (for email delivery)

1. Enable 2-factor authentication on your Google account
2. Generate app-specific password: https://myaccount.google.com/apppasswords
3. Use the generated password (not your regular password) for `EMAIL_PASSWORD`

## Troubleshooting

### Jobs not collecting?
- Check `config/config.yaml` has valid `job_sources` with `enabled: true`
- Verify internet connectivity
- Check collector logs for HTTP errors

### Email not sending?
- Verify SMTP credentials (use app-specific password for Gmail)
- Check `email.enabled: true` in config
- Review email configuration in environment variables
- Check spam folder

### Dashboard not loading?
- Run `streamlit run streamlit_app.py` from repo root
- Check Python path includes `src/` (automatic via `streamlit_app.py`)
- Verify `config/config.yaml` exists
- Check terminal for error messages

## Development

### Adding a New Job Portal

1. Create collector class in `src/ai_job_hunter_pro/adapters/portal_collectors.py`:
   ```python
   from ai_job_hunter_pro.plugins import register_collector
   from ai_job_hunter_pro.domain.ports import JobSourceCollector

   @register_collector
   class MyPortalCollector(JobSourceCollector):
       def __init__(self, config):
           self.config = config
       
       def collect(self) -> List[JobPost]:
           # Implement scraping logic
           pass
   ```

2. Update `src/ai_job_hunter_pro/adapters/__init__.py` to import the new collector

3. Configure in `config/config.yaml`:
   ```yaml
   job_sources:
     - type: myportal
       enabled: true
       query: "Your search"
   ```

### Running Tests

```bash
pytest  # Run all tests
pytest -v  # Verbose output
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support & Feedback

For issues, suggestions, or questions:
- Create a GitHub Issue
- Check existing issues for solutions
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for cloud-specific help