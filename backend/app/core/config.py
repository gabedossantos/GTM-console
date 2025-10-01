"""Application configuration settings."""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the JourneyLens backend."""

    app_name: str = "JourneyLens API"
    api_version: str = "1.0.0"
    auth_token: str = "demo-token"
    database_url: str = "sqlite:///./backend_data/journeylens.db"
    demo_data_accounts: Path = Path("demo_accounts.csv")
    demo_data_contacts: Path = Path("demo_contacts.csv")
    demo_data_interactions: Path = Path("demo_interactions.csv")
    demo_data_expected: Path = Path("demo_expected_insights.csv")

    model_config = SettingsConfigDict(case_sensitive=False)

    def model_post_init(self, __context: object) -> None:
        base_dir = Path(__file__).resolve().parents[3]
        object.__setattr__(self, "demo_data_accounts", (base_dir / self.demo_data_accounts).resolve())
        object.__setattr__(self, "demo_data_contacts", (base_dir / self.demo_data_contacts).resolve())
        object.__setattr__(self, "demo_data_interactions", (base_dir / self.demo_data_interactions).resolve())
        object.__setattr__(self, "demo_data_expected", (base_dir / self.demo_data_expected).resolve())


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    settings = Settings()

    # Ensure the database directory exists for SQLite
    if settings.database_url.startswith("sqlite"):
        db_path = Path(settings.database_url.split("sqlite:///")[-1]).resolve()
        db_dir = db_path.parent
        db_dir.mkdir(parents=True, exist_ok=True)

    return settings
