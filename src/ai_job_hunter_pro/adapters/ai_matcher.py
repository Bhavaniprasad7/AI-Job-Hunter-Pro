from __future__ import annotations
import os
from typing import List

import openai

from ai_job_hunter_pro.domain.entities import JobPost, MatchResult, Resume
from ai_job_hunter_pro.domain.ports import Matcher


class OpenAIAdapter(Matcher):
    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo"):
        if api_key:
            openai.api_key = api_key
        elif os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")

        if not openai.api_key:
            raise ValueError("OpenAI API key is required for the AI matcher.")

        self.model = model

    def match(self, resume: Resume, job_post: JobPost) -> MatchResult:
        prompt = self._build_prompt(resume, job_post)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a job matching assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.0,
        )
        answer = response.choices[0].message.content.strip()
        score, ats_score, summary, skill_matches, missing_skills = self._parse_response(answer)
        return MatchResult(
            resume_id=resume.id,
            job_id=job_post.id,
            score=score,
            ats_score=ats_score,
            match_summary=summary,
            skill_matches=skill_matches,
            missing_skills=missing_skills,
            job_post=job_post,
            resume=resume,
        )

    def _build_prompt(self, resume: Resume, job_post: JobPost) -> str:
        return (
            f"Evaluate the compatibility between the resume and the job description."
            f" Provide a numeric match score from 0 to 100, an ATS compatibility score from 0 to 100, a short summary,"
            f" the skills that match, and the skills the candidate is missing.\n\n"
            f"Resume text:\n{resume.text}\n\n"
            f"Job title: {job_post.title}\n"
            f"Company: {job_post.company}\n"
            f"Location: {job_post.location}\n"
            f"Job description:\n{job_post.description}\n"
            f"Only answer in JSON format with keys: score, ats_score, summary, skill_matches, missing_skills."
        )

    def _parse_response(self, answer: str) -> tuple[float, float, str, List[str], List[str]]:
        try:
            import json

            parsed = json.loads(answer)
            return (
                float(parsed.get("score", 0.0)),
                float(parsed.get("ats_score", 0.0)),
                parsed.get("summary", ""),
                parsed.get("skill_matches", []),
                parsed.get("missing_skills", []),
            )
        except Exception:
            return 0.0, 0.0, answer, [], []
