from pathlib import Path

from ai_job_hunter_pro.config.loader import load_config


def test_load_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
        environment: test
        database_url: sqlite:///test.db
        resume_paths: [resumes]
        job_sources:
          - name: local
            plugin: json
            settings:
              path: data/sample_jobs.json
        """
    )

    config = load_config(config_file)

    assert config.environment == "test"
    assert config.database_url == "sqlite:///test.db"
    assert len(config.job_sources) == 1
    assert config.job_sources[0].plugin == "json"
