from datetime import date, timedelta

from ai_job_hunter_pro.domain.entities import JobPost
from ai_job_hunter_pro.use_cases.filter_jobs import JobFilterService
from ai_job_hunter_pro.config.settings import FilterConfig


def test_job_filter_matches_role_keywords_location_and_24h():
    config = FilterConfig(
        role="Azure Integration developer",
        keywords=["Logic apps"],
        location=["Pan india"],
        experience_min=5.0,
        last_24_hours=True,
        max_age_days=30,
        fortune_500_only=False,
    )

    jobs = [
        JobPost(
            id="1",
            title="Azure Integration Developer",
            description="Design and build Logic Apps solutions",
            company="Contoso",
            location="India",
            posted_date=date.today(),
            url="http://example.com",
            source="test",
        ),
        JobPost(
            id="2",
            title="Java Developer",
            description="Backend work",
            company="Fabrikam",
            location="India",
            posted_date=date.today(),
            url="http://example.com",
            source="test",
        ),
    ]

    filtered = JobFilterService(config).filter(jobs)

    assert len(filtered) == 1
    assert filtered[0].title == "Azure Integration Developer"
    assert filtered[0].location == "India"
