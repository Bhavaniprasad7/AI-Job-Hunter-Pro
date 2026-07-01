from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional

import typer

from ai_job_hunter_pro.adapters.email_sender import SmtpEmailSender
from ai_job_hunter_pro.adapters.sqldb import SqlAlchemyJobRepository, SqlAlchemyMatchRepository
from ai_job_hunter_pro.config.loader import load_config
from ai_job_hunter_pro.use_cases.collect_jobs import JobCollectorService
from ai_job_hunter_pro.use_cases.email_summary import DailySummaryService
from ai_job_hunter_pro.use_cases.filter_jobs import JobFilterService
from ai_job_hunter_pro.use_cases.match_jobs import JobMatchingService
from ai_job_hunter_pro.use_cases.parse_resumes import ResumeParsingService
from ai_job_hunter_pro.use_cases.reporting import ReportingService

app = typer.Typer()

logger = logging.getLogger("ai_job_hunter_pro")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def init_repositories(config):
    job_repo = SqlAlchemyJobRepository(config.database_url)
    match_repo = SqlAlchemyMatchRepository(config.database_url)
    return job_repo, match_repo


def init_email_sender(config):
    return SmtpEmailSender(
        sender=config.email.sender,
        smtp_server=config.email.smtp_server,
        smtp_port=config.email.smtp_port,
        username=config.email.username,
        password=config.email.password,
        use_tls=config.email.use_tls,
    )


@app.command()
def run_all(config_path: Optional[Path] = typer.Option("config/config.yaml", exists=True)) -> None:
    config = load_config(config_path)
    logger.info("Loading configuration from %s", config_path)

    job_repo, match_repo = init_repositories(config)
    collector = JobCollectorService(config)
    parser = ResumeParsingService(config)
    filter_service = JobFilterService(config.filter)
    matcher = JobMatchingService(config)
    email_sender = init_email_sender(config)
    summary_service = DailySummaryService(config.email, email_sender)
    reporting_service = ReportingService(config.report)

    jobs = filter_service.filter(collector.collect())
    logger.info("Collected %d jobs after filtering", len(jobs))

    resumes = parser.parse_all()
    logger.info("Parsed %d resumes", len(resumes))

    job_repo.save_jobs(jobs)
    matches = matcher.match(resumes, jobs)
    match_repo.save_matches(matches)

    reporting_service.generate_reports(matches)
    summary_service.send_summary(matches)
    logger.info("Run completed successfully")


@app.command()
def serve_dashboard() -> None:
    typer.echo("Run the Streamlit app with: streamlit run src/ai_job_hunter_pro/ui/streamlit_app.py")


if __name__ == "__main__":
    app()
