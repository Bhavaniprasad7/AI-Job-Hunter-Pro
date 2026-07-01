from __future__ import annotations
import os
from pathlib import Path
from typing import List

import streamlit as st
import pandas as pd

from ai_job_hunter_pro.config.loader import load_config
from ai_job_hunter_pro.adapters.sqldb import SqlAlchemyJobRepository, SqlAlchemyMatchRepository
from ai_job_hunter_pro.use_cases.collect_jobs import JobCollectorService
from ai_job_hunter_pro.use_cases.filter_jobs import JobFilterService


@st.cache_resource
def get_config():
    """Load config from file or environment, with fallback to defaults."""
    config_path = os.getenv("AI_JOB_HUNTER_CONFIG_PATH", "config/config.yaml")
    
    if not Path(config_path).exists():
        config_path = "config/config.yaml"
    
    config = load_config(config_path)
    
    if os.getenv("OPENAI_API_KEY"):
        config.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    return config


def load_data(config):
    """Load jobs and matches from database."""
    job_repo = SqlAlchemyJobRepository(config.database_url)
    match_repo = SqlAlchemyMatchRepository(config.database_url)
    jobs = job_repo.list_jobs()
    if not jobs:
        try:
            collector = JobCollectorService(config)
            jobs = collector.collect()
            if jobs:
                job_repo.save_jobs(jobs)
        except Exception as e:
            st.warning(f"Error collecting jobs: {str(e)}")
    matches = match_repo.list_matches()
    return jobs, matches


def render_dashboard():
    st.set_page_config(
        page_title="AI Job Hunter Pro",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    config = get_config()
    jobs, matches = load_data(config)

    st.title("🔍 AI Job Hunter Pro")
    st.write("A dashboard for job collection, filtering, and matching results.")

    if not jobs:
        st.info("📊 No jobs found. Configure job sources in `config/config.yaml` to get started.")
        return

    filter_service = JobFilterService(config.filter)
    filtered_jobs = filter_service.filter(jobs)

    col1, col2 = st.columns([1, 4])
    with col1:
        st.sidebar.header("🔎 Filters")
        company = st.sidebar.multiselect("Company", sorted({job.company for job in jobs if job.company}))
        location = st.sidebar.multiselect("Location", sorted({job.location for job in jobs if job.location}))
        if company or location:
            config.filter.company = company
            config.filter.location = location
            filtered_jobs = filter_service.filter(jobs)

    st.subheader(f"💼 Jobs ({len(filtered_jobs)})")
    if filtered_jobs:
        df = pd.DataFrame([
            {
                "Title": job.title,
                "Company": job.company,
                "Location": job.location,
                "Source": job.source,
                "URL": job.url,
            }
            for job in filtered_jobs
        ])
        st.dataframe(df, use_container_width=True)
    else:
        st.write("❌ No jobs available with the current filters.")

    if matches:
        st.subheader(f"⭐ Matches ({len(matches)})")
        matches_df = pd.DataFrame([
            {
                "Resume": match.resume_id,
                "Job Title": match.job_post.title,
                "Company": match.job_post.company,
                "Score": f"{match.score:.1f}",
                "ATS Score": f"{match.ats_score:.1f}",
            }
            for match in matches
        ])
        st.dataframe(matches_df, use_container_width=True)


if __name__ == "__main__":
    render_dashboard()
