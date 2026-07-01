from __future__ import annotations
from pathlib import Path
from typing import List

import streamlit as st
import pandas as pd

from ai_job_hunter_pro.config.loader import load_config
from ai_job_hunter_pro.adapters.sqldb import SqlAlchemyJobRepository, SqlAlchemyMatchRepository
from ai_job_hunter_pro.use_cases.collect_jobs import JobCollectorService
from ai_job_hunter_pro.use_cases.filter_jobs import JobFilterService


def load_data(config):
    job_repo = SqlAlchemyJobRepository(config.database_url)
    match_repo = SqlAlchemyMatchRepository(config.database_url)
    jobs = job_repo.list_jobs()
    if not jobs:
        collector = JobCollectorService(config)
        jobs = collector.collect()
        if jobs:
            job_repo.save_jobs(jobs)
    matches = match_repo.list_matches()
    return jobs, matches


def render_dashboard():
    config = load_config("config/config.yaml")
    jobs, matches = load_data(config)

    st.title("AI Job Hunter Pro")
    st.write("A dashboard for job collection and matching results.")

    filter_service = JobFilterService(config.filter)
    filtered_jobs = filter_service.filter(jobs)

    st.sidebar.header("Filters")
    company = st.sidebar.multiselect("Company", sorted({job.company for job in jobs if job.company}))
    location = st.sidebar.multiselect("Location", sorted({job.location for job in jobs if job.location}))
    if company or location:
        config.filter.company = company
        config.filter.location = location
        filtered_jobs = filter_service.filter(jobs)

    st.subheader("Jobs")
    if filtered_jobs:
        st.dataframe(pd.DataFrame([job.__dict__ for job in filtered_jobs]))
    else:
        st.write("No jobs available with the current filters.")

    st.subheader("Matches")
    if matches:
        st.dataframe(pd.DataFrame([{
            "resume_id": match.resume_id,
            "job_id": match.job_id,
            "score": match.score,
            "ats_score": match.ats_score,
            "job_title": match.job_post.title,
            "company": match.job_post.company,
            "location": match.job_post.location,
        } for match in matches]))
    else:
        st.write("No matches have been generated yet.")


if __name__ == "__main__":
    render_dashboard()
