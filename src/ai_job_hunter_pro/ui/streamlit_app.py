from __future__ import annotations
import os
from pathlib import Path
from typing import List

import streamlit as st
import pandas as pd

from types import SimpleNamespace

from ai_job_hunter_pro.config.loader import load_config
from ai_job_hunter_pro.adapters.sqldb import SqlAlchemyJobRepository, SqlAlchemyMatchRepository
from ai_job_hunter_pro.use_cases.collect_jobs import JobCollectorService
from ai_job_hunter_pro.use_cases.filter_jobs import JobFilterService


@st.cache_resource
def get_config():
    """Load config from file or environment, with fallback to defaults.

    Return a plain SimpleNamespace built from the validated config data so
    Streamlit caching doesn't pickle pydantic internals across environments.
    """
    config_path = os.getenv("AI_JOB_HUNTER_CONFIG_PATH", "config/config.yaml")

    if not Path(config_path).exists():
        config_path = "config/config.yaml"

    config = load_config(config_path)

    if os.getenv("OPENAI_API_KEY"):
        # update the validated model, but expose via the namespace
        config.openai_api_key = os.getenv("OPENAI_API_KEY")

    # Convert pydantic model to plain dict (supports v2 `.model_dump()` or v1 `.dict()`)
    if hasattr(config, "model_dump"):
        cfg_dict = config.model_dump()
    else:
        cfg_dict = config.dict()

    def _to_namespace(obj, parent_key: str | None = None):
        if isinstance(obj, dict):
            # Preserve settings dictionaries for collectors that call .get()
            if parent_key == "settings":
                return obj
            return SimpleNamespace(
                **{
                    k: _to_namespace(v, parent_key=k)
                    for k, v in obj.items()
                }
            )
        if isinstance(obj, list):
            return [_to_namespace(v, parent_key=parent_key) for v in obj]
        return obj

    return _to_namespace(cfg_dict)


def load_data(config, force_refresh: bool = False):
    """Load jobs and matches from database, optionally refreshing from sources."""
    job_repo = SqlAlchemyJobRepository(config.database_url)
    match_repo = SqlAlchemyMatchRepository(config.database_url)
    jobs = job_repo.list_jobs()
    warnings: list[str] = []
    if force_refresh or not jobs:
        collector = JobCollectorService(config)
        source_jobs, warnings = collector.collect()
        if source_jobs:
            job_repo.save_jobs(source_jobs)
        jobs = source_jobs
    matches = match_repo.list_matches()
    return jobs, matches, warnings


def render_dashboard():
    st.set_page_config(
        page_title="AI Job Hunter Pro",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    config = get_config()
    jobs, matches, warnings = load_data(config)

    st.title("🔍 AI Job Hunter Pro")
    st.write("A dashboard for job collection, filtering, and matching results.")

    for warning_message in warnings:
        st.warning(warning_message)

    if not jobs:
        st.info("📊 No jobs found. Configure job sources in `config/config.yaml` to get started.")
        return

    col1, col2 = st.columns([1, 4])
    with col1:
        st.sidebar.header("🔎 Search Jobs")
        with st.sidebar.form("search_form"):
            role = st.text_input("Job role", value=getattr(config.filter, "role", ""))
            keywords_input = st.text_input(
                "Keywords",
                value=", ".join(getattr(config.filter, "keywords", [])),
                help="Comma-separated keywords, e.g. Logic Apps, Azure Functions",
            )
            location_input = st.text_input("Location", value=", ".join(getattr(config.filter, "location", [])))
            company_input = st.text_input(
                "Company (optional)",
                value=", ".join(getattr(config.filter, "company", [])),
                help="Leave blank to search across all companies.",
            )
            fortune_filter = st.checkbox(
                "Only Fortune 500 companies",
                value=getattr(config.filter, "fortune_500_only", False),
                help="Show only jobs from the Fortune 500 list when checked.",
            )
            experience = st.number_input(
                "Experience (years)",
                min_value=0.0,
                value=float(getattr(config.filter, "experience_min", 0.0)),
                step=0.5,
            )
            last_24_hours = st.checkbox(
                "Only jobs from last 24 hours",
                value=getattr(config.filter, "last_24_hours", False),
            )
            submitted = st.form_submit_button("Search")

        if submitted:
            config.filter.role = role
            config.filter.keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
            config.filter.location = [l.strip() for l in location_input.split(",") if l.strip()]
            config.filter.company = [c.strip() for c in company_input.split(",") if c.strip()]
            config.filter.fortune_500_only = fortune_filter
            config.filter.experience_min = experience
            config.filter.last_24_hours = last_24_hours
            jobs, matches, warnings = load_data(config, force_refresh=True)
            for warning_message in warnings:
                st.sidebar.warning(warning_message)
            st.sidebar.success("Search applied and job sources refreshed")
        else:
            st.sidebar.info("Update filters and click Search to refresh results.")

    filter_service = JobFilterService(config.filter)
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
