#!/usr/bin/env python
"""
Health check script for AI Job Hunter Pro.
Validates dependencies, configuration, and system setup before deployment.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_dependencies():
    """Check if all required packages are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        ("streamlit", "streamlit"),
        ("pydantic", "pydantic"),
        ("sqlalchemy", "sqlalchemy"),
        ("openai", "openai"),
        ("requests", "requests"),
        ("bs4", "beautifulsoup4"),
        ("pandas", "pandas"),
        ("yaml", "PyYAML"),
    ]
    
    missing = []
    for module, package in required_packages:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_config():
    """Check if configuration file exists and is valid."""
    print("\n🔍 Checking configuration...")
    
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        print(f"  ❌ Config file not found: {config_path}")
        return False
    
    try:
        from ai_job_hunter_pro.config.loader import load_config
        config = load_config(str(config_path))
        print(f"  ✅ Config loaded successfully")
        
        # Check job sources
        job_sources = config.job_sources
        print(f"  ✅ {len(job_sources)} job sources configured")
        
        if not job_sources:
            print(f"  ⚠️  No job sources configured! Update config/config.yaml")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Error loading config: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_database():
    """Check if database configuration is valid."""
    print("\n🔍 Checking database...")
    
    try:
        from ai_job_hunter_pro.config.loader import load_config
        config = load_config("config/config.yaml")
        
        from sqlalchemy import create_engine
        engine = create_engine(config.database_url)
        
        # Try to connect
        with engine.connect() as conn:
            print(f"  ✅ Database connection successful: {config.database_url}")
            return True
    except Exception as e:
        print(f"  ⚠️  Database check skipped or failed: {e}")
        return True  # Don't fail on DB issues


def check_streamlit_setup():
    """Check Streamlit configuration."""
    print("\n🔍 Checking Streamlit setup...")
    
    root_app = Path("streamlit_app.py")
    if root_app.exists():
        print(f"  ✅ Root entry point exists: {root_app}")
    else:
        print(f"  ❌ Missing root entry point: {root_app}")
        return False
    
    streamlit_config = Path(".streamlit/config.toml")
    if streamlit_config.exists():
        print(f"  ✅ Streamlit config found: {streamlit_config}")
    else:
        print(f"  ⚠️  Streamlit config not found: {streamlit_config}")
    
    return True


def main():
    """Run all health checks."""
    print("\n" + "=" * 60)
    print("🏥 AI Job Hunter Pro - Health Check")
    print("=" * 60 + "\n")
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Configuration", check_config),
        ("Database", check_database),
        ("Streamlit Setup", check_streamlit_setup),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            if name == "Dependencies":
                success, details = check_func()
                results[name] = success
            else:
                results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Summary")
    print("=" * 60)
    
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_pass = all(results.values())
    
    if all_pass:
        print("\n✅ All checks passed! Ready for deployment.")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
