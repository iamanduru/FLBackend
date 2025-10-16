import os, json
from typing import Optional, List, Any
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_CORS = ["http://localhost:3000", "http://localhost:5173"]


class Settings(BaseSettings):
    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        case_sensitive=True,
        extra="ignore",  # ignore S3_* or other extras
    )

    # --- App ---
    app_name: str = Field(default="FinLens API", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")

    # IMPORTANT: keep this as a STRING to avoid Pydantic's auto-JSON decode for lists
    app_cors_origins_raw: Optional[str] = Field(
        default=None,
        alias="APP_CORS_ORIGINS",
        description="Comma-separated or JSON list string",
    )

    # --- Security ---
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_alg: str = Field(default="HS256", alias="JWT_ALG")
    access_token_expire_minutes: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=30, alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # --- DB ---
    mysql_dsn: str = Field(..., alias="MYSQL_DSN")

    # --- Optional integrations ---
    redis_url: Optional[str] = Field(default=None, alias="REDIS_URL")
    s3_endpoint_url: Optional[str] = Field(default=None, alias="S3_ENDPOINT_URL")
    s3_access_key: Optional[str] = Field(default=None, alias="S3_ACCESS_KEY")
    s3_secret_key: Optional[str] = Field(default=None, alias="S3_SECRET_KEY")
    s3_bucket: Optional[str] = Field(default=None, alias="S3_BUCKET")

    # Expose a computed, always-a-list property for CORS
    @property
    def cors_origins(self) -> List[str]:
        v = self.app_cors_origins_raw
        if not v or not v.strip():
            return DEFAULT_CORS
        v = v.strip()
        if v.startswith("["):            # JSON list case
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(s).strip() for s in parsed if str(s).strip()]
            except Exception:
                pass
        # Comma-separated fallback
        return [s.strip() for s in v.split(",") if s.strip()]


settings = Settings()
