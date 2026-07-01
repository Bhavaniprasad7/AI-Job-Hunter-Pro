from __future__ import annotations
from datetime import date
from pathlib import Path
from typing import Iterable, List, Optional

from sqlalchemy import Column, Date, Float, Integer, JSON, String, Table, Text, create_engine
from sqlalchemy.orm import Mapped, DeclarativeBase, Session, mapped_column

from ai_job_hunter_pro.domain.entities import JobPost, MatchResult, Resume
from ai_job_hunter_pro.domain.ports import JobRepository, MatchRepository


class Base(DeclarativeBase):
    pass


class JobPostModel(Base):
    __tablename__ = "job_posts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    posted_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSON, default={})


class MatchResultModel(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resume_id: Mapped[str] = mapped_column(String, nullable=False)
    job_id: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    ats_score: Mapped[float] = mapped_column(Float, nullable=False)
    match_summary: Mapped[str] = mapped_column(Text, nullable=False)
    skill_matches: Mapped[list[str]] = mapped_column(JSON, default=list)
    missing_skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    job_post: Mapped[dict] = mapped_column(JSON, default={})
    resume: Mapped[dict] = mapped_column(JSON, default={})


class SqlAlchemyJobRepository(JobRepository):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, future=True)
        Base.metadata.create_all(self.engine)

    def save_jobs(self, jobs: Iterable[JobPost]) -> None:
        with Session(self.engine) as session:
            for job in jobs:
                model = JobPostModel(
                    id=job.id,
                    title=job.title,
                    description=job.description,
                    company=job.company,
                    location=job.location,
                    posted_date=job.posted_date,
                    url=job.url,
                    source=job.source,
                    raw_data=job.raw_data,
                )
                session.merge(model)
            session.commit()

    def list_jobs(self, source: Optional[str] = None) -> List[JobPost]:
        with Session(self.engine) as session:
            query = session.query(JobPostModel)
            if source:
                query = query.filter(JobPostModel.source == source)
            results = query.all()
        return [
            JobPost(
                id=row.id,
                title=row.title,
                description=row.description,
                company=row.company,
                location=row.location,
                posted_date=row.posted_date,
                url=row.url,
                source=row.source,
                raw_data=row.raw_data,
            )
            for row in results
        ]


class SqlAlchemyMatchRepository(MatchRepository):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, future=True)
        Base.metadata.create_all(self.engine)

    def save_matches(self, matches: Iterable[MatchResult]) -> None:
        with Session(self.engine) as session:
            for match in matches:
                model = MatchResultModel(
                    resume_id=match.resume_id,
                    job_id=match.job_id,
                    score=match.score,
                    ats_score=match.ats_score,
                    match_summary=match.match_summary,
                    skill_matches=match.skill_matches,
                    missing_skills=match.missing_skills,
                    job_post=match.job_post.__dict__,
                    resume=match.resume.__dict__,
                )
                session.add(model)
            session.commit()

    def list_matches(self, resume_id: Optional[str] = None) -> List[MatchResult]:
        with Session(self.engine) as session:
            query = session.query(MatchResultModel)
            if resume_id:
                query = query.filter(MatchResultModel.resume_id == resume_id)
            results = query.all()
        return [
            MatchResult(
                resume_id=row.resume_id,
                job_id=row.job_id,
                score=float(row.score),
                ats_score=float(row.ats_score),
                match_summary=row.match_summary,
                skill_matches=row.skill_matches,
                missing_skills=row.missing_skills,
                job_post=JobPost(**row.job_post),
                resume=Resume(**row.resume),
            )
            for row in results
        ]
