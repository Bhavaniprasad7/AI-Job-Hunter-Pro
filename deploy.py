#!/usr/bin/env python
"""
Quick deployment preparation script for Streamlit Cloud.
Verifies all components and provides deployment guidance.
"""

import sys
from pathlib import Path
from datetime import datetime

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"🚀 {title}")
    print("=" * 70)

def print_section(title):
    """Print a formatted section."""
    print(f"\n📌 {title}")
    print("-" * 70)

def check_file_exists(path, description):
    """Check if a file exists and print status."""
    if Path(path).exists():
        print(f"  ✅ {description}: {path}")
        return True
    else:
        print(f"  ❌ {description}: {path}")
        return False

def main():
    print_header("Streamlit Cloud Deployment Checklist")
    
    # Check essential files
    print_section("Essential Files for Cloud Deployment")
    
    essential_files = [
        ("streamlit_app.py", "Root entry point"),
        (".streamlit/config.toml", "Streamlit configuration"),
        (".streamlit/secrets.toml.example", "Secrets template"),
        ("config/config.yaml", "Job search configuration"),
        ("requirements.txt", "Python dependencies"),
        (".gitignore", "Git ignore rules"),
    ]
    
    all_files_exist = True
    for filepath, description in essential_files:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    # Check documentation
    print_section("Documentation Files")
    
    docs = [
        ("README.md", "Features and quick start"),
        ("DEPLOYMENT.md", "Detailed deployment guide"),
        ("DEPLOYMENT_CHECKLIST.md", "Pre/post deployment checklist"),
        ("CLOUD_READY.md", "Cloud deployment summary"),
    ]
    
    all_docs_exist = True
    for filepath, description in docs:
        if not check_file_exists(filepath, description):
            all_docs_exist = False
    
    # Deployment status
    print_section("Deployment Status")
    
    if all_files_exist and all_docs_exist:
        print("  ✅ All essential files are in place")
        print("  ✅ All documentation is available")
        status = "READY"
    else:
        print("  ❌ Some files are missing (see above)")
        status = "INCOMPLETE"
    
    # Quick deployment steps
    print_section("Quick Deployment Steps")
    
    steps = [
        ("1. Verify locally", [
            "Run: python health_check.py",
            "Test: streamlit run streamlit_app.py",
            "Check dashboard loads on http://localhost:8501"
        ]),
        ("2. Push to GitHub", [
            "git add .",
            "git commit -m 'Ready for Streamlit Cloud'",
            "git push origin main",
            "Verify on GitHub: all files present"
        ]),
        ("3. Create Streamlit Cloud app", [
            "Go to: https://share.streamlit.io",
            "Click: New app",
            "Connect: your-username/AI-Job-Hunter-Pro",
            "Main file: streamlit_app.py",
            "Deploy and wait 1-3 minutes"
        ]),
        ("4. Configure secrets", [
            "Click: ☰ (menu) → Settings",
            "Go to: Secrets tab",
            "Add: OPENAI_API_KEY = 'sk-...'",
            "(Optional) Add EMAIL credentials",
            "Save and restart app"
        ]),
        ("5. Test on cloud", [
            "Dashboard loads: ✓",
            "Filters work: ✓",
            "Jobs appear (1-3 min): ✓",
            "No errors in logs: ✓"
        ]),
    ]
    
    for step_title, step_details in steps:
        print(f"\n{step_title}:")
        for detail in step_details:
            print(f"  → {detail}")
    
    # Important notes
    print_section("Important Notes")
    
    notes = [
        "📍 GitHub repo must be PUBLIC (free Streamlit Cloud requirement)",
        "🔐 Never commit .streamlit/secrets.toml (added to .gitignore)",
        "🗄️  Database: SQLite NOT persisted (restart = fresh data)",
        "⚡ First load: 1-3 min (job collection), then fast (cached)",
        "⏱️  Portal scrapers: Set max_pages: 2-3 to avoid blocking",
        "🔑 OpenAI API key: Required for job matching",
    ]
    
    for note in notes:
        print(f"  {note}")
    
    # Success indicators
    print_section("Success Indicators After Deployment")
    
    indicators = [
        "✅ App available at: https://share.streamlit.io/your-username/AI-Job-Hunter-Pro",
        "✅ Dashboard loads with purple/red theme",
        "✅ Sidebar shows Company and Location filters",
        "✅ Job listings appear (may take 1-3 min first time)",
        "✅ No errors in logs (☰ → Manage app → Logs)",
        "✅ Filters update results when selected",
    ]
    
    for indicator in indicators:
        print(f"  {indicator}")
    
    # Resources
    print_section("Resources & Support")
    
    resources = [
        ("README.md", "Features overview and quick start"),
        ("DEPLOYMENT.md", "Step-by-step deployment guide"),
        ("DEPLOYMENT_CHECKLIST.md", "Complete pre/post deployment checklist"),
        ("CLOUD_READY.md", "Cloud deployment package summary"),
        ("health_check.py", "Run: python health_check.py"),
    ]
    
    for resource, description in resources:
        print(f"  📖 {resource}")
        print(f"     → {description}")
    
    # Final status
    print_header(f"Status: ✅ {status}")
    
    if status == "READY":
        print("""
Your application is READY for Streamlit Cloud deployment!

Next steps:
1. Run: python health_check.py
2. Run: streamlit run streamlit_app.py (test locally)
3. Run: git push origin main (push to GitHub)
4. Go to: https://share.streamlit.io (deploy)

See DEPLOYMENT.md for detailed instructions.
""")
        return 0
    else:
        print("""
Please address the missing files above before deployment.
See DEPLOYMENT.md for detailed setup instructions.
""")
        return 1

if __name__ == "__main__":
    sys.exit(main())
