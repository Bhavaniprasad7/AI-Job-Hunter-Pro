from __future__ import annotations
from datetime import datetime, timedelta
from typing import Iterable, List, Optional
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from ai_job_hunter_pro.domain.entities import JobPost
from ai_job_hunter_pro.domain.ports import JobSourceCollector
from ai_job_hunter_pro.plugins import register_collector

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

DEFAULT_MAX_PAGES = 1


def _parse_date_text(text: str) -> Optional[datetime.date]:
    text = text.strip().lower()
    if not text:
        return None
    if "today" in text or "just" in text:
        return datetime.today().date()
    if "1 day" in text or "1d" in text:
        return datetime.today().date()
    if "days" in text:
        try:
            value = int("".join(ch for ch in text if ch.isdigit()))
            return (datetime.today() - datetime.timedelta(days=value)).date()
        except ValueError:
            return None
    return None


@register_collector("naukri")
class NaukriJobCollector(JobSourceCollector):
    def __init__(self, settings: dict):
        self.query = settings.get("query", "")
        self.location = settings.get("location", "")
        self.company = settings.get("company", "")
        self.max_pages = int(settings.get("max_pages", DEFAULT_MAX_PAGES))

    def _build_url(self, page: int = 1) -> str:
        query = quote_plus(self.query)
        location = quote_plus(self.location)
        return f"https://www.naukri.com/{query}-jobs?k={query}&l={location}&pageno={page}"

    def collect(self) -> Iterable[JobPost]:
        for page in range(1, self.max_pages + 1):
            response = requests.get(self._build_url(page), headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("article.jobTuple, div.jobTuple")
            for card in cards:
                title_el = card.select_one("a.title")
                company_el = card.select_one("a.subTitle")
                location_el = card.select_one("li.location")
                summary_el = card.select_one("div.job-description")
                link = title_el["href"] if title_el and title_el.has_attr("href") else None
                yield JobPost(
                    id=str(link or title_el.text if title_el else card.get_text()),
                    title=title_el.text.strip() if title_el else "",
                    description=summary_el.text.strip() if summary_el else "",
                    company=company_el.text.strip() if company_el else "",
                    location=location_el.text.strip() if location_el else self.location,
                    posted_date=None,
                    url=link,
                    source="naukri",
                    raw_data={
                        "query": self.query,
                        "location": self.location,
                        "company": self.company,
                    },
                )


@register_collector("indeed")
class IndeedJobCollector(JobSourceCollector):
    def __init__(self, settings: dict):
        self.query = settings.get("query", "")
        self.location = settings.get("location", "")
        self.company = settings.get("company", "")
        self.max_pages = int(settings.get("max_pages", DEFAULT_MAX_PAGES))

    def _build_url(self, page: int = 0) -> str:
        q = quote_plus(self.query)
        l = quote_plus(self.location)
        start = page * 10
        return f"https://www.indeed.com/jobs?q={q}&l={l}&start={start}"

    def collect(self) -> Iterable[JobPost]:
        for page in range(self.max_pages):
            response = requests.get(self._build_url(page), headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("div.job_seen_beacon, a.tapItem")
            for card in cards:
                title_el = card.select_one("h2.jobTitle span")
                company_el = card.select_one("span.companyName")
                location_el = card.select_one("div.companyLocation")
                summary_el = card.select_one("div.job-snippet")
                link_el = card.select_one("a.jcs-JobTitle, a.tapItem")
                link = None
                if link_el and link_el.has_attr("href"):
                    href = link_el["href"]
                    link = f"https://www.indeed.com{href}" if href.startswith("/") else href
                yield JobPost(
                    id=str(link or title_el.text if title_el else card.get_text()),
                    title=title_el.text.strip() if title_el else "",
                    description=summary_el.text.strip() if summary_el else "",
                    company=company_el.text.strip() if company_el else "",
                    location=location_el.text.strip() if location_el else self.location,
                    posted_date=None,
                    url=link,
                    source="indeed",
                    raw_data={
                        "query": self.query,
                        "location": self.location,
                        "company": self.company,
                    },
                )


@register_collector("linkedin")
class LinkedInJobCollector(JobSourceCollector):
    def __init__(self, settings: dict):
        self.query = settings.get("query", "")
        self.location = settings.get("location", "")
        self.max_pages = int(settings.get("max_pages", DEFAULT_MAX_PAGES))

    def _build_url(self, page: int = 0) -> str:
        q = quote_plus(self.query)
        l = quote_plus(self.location)
        start = page * 25
        return f"https://www.linkedin.com/jobs/search/?keywords={q}&location={l}&start={start}"

    def collect(self) -> Iterable[JobPost]:
        for page in range(self.max_pages):
            response = requests.get(self._build_url(page), headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("li.result-card, div.base-card")
            for card in cards:
                title_el = card.select_one("h3.base-search-card__title, h3.result-card__title")
                company_el = card.select_one("h4.base-search-card__subtitle, h4.result-card__subtitle")
                location_el = card.select_one("span.job-result-card__location, span.job-search-card__location")
                summary_el = card.select_one("p.job-result-card__snippet, p.base-search-card__description")
                link_el = card.select_one("a.base-card__full-link, a.result-card__full-card-link")
                link = link_el["href"] if link_el and link_el.has_attr("href") else None
                yield JobPost(
                    id=str(link or title_el.text if title_el else card.get_text()),
                    title=title_el.text.strip() if title_el else "",
                    description=summary_el.text.strip() if summary_el else "",
                    company=company_el.text.strip() if company_el else "",
                    location=location_el.text.strip() if location_el else self.location,
                    posted_date=None,
                    url=link,
                    source="linkedin",
                    raw_data={
                        "query": self.query,
                        "location": self.location,
                    },
                )


@register_collector("company_page")
class CompanyCareerPageCollector(JobSourceCollector):
    def __init__(self, settings: dict):
        self.urls = settings.get("urls", [])
        self.selectors = settings.get("selectors", {})

    def collect(self) -> Iterable[JobPost]:
        for url in self.urls:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(self.selectors.get("card", "a"))
            for card in cards:
                title_el = card.select_one(self.selectors.get("title", "h2, h3, .job-title"))
                company_el = card.select_one(self.selectors.get("company", ".company, .employer"))
                location_el = card.select_one(self.selectors.get("location", ".location, .job-location"))
                summary_el = card.select_one(self.selectors.get("description", ".description, .summary, .job-desc"))
                link_el = card if card.name == "a" else card.select_one("a")
                link = link_el["href"] if link_el and link_el.has_attr("href") else url
                yield JobPost(
                    id=str(link),
                    title=title_el.text.strip() if title_el else "",
                    description=summary_el.text.strip() if summary_el else "",
                    company=company_el.text.strip() if company_el else "",
                    location=location_el.text.strip() if location_el else "",
                    posted_date=None,
                    url=link,
                    source="company_page",
                    raw_data={"origin_url": url},
                )
