from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# --- Make sure Alembic can find your app and .env regardless of CWD ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # folder containing alembic.ini
APP_ROOT = PROJECT_ROOT  # adjust if your app/ lives elsewhere

# Ensure project root is on sys.path for "from app ..." imports
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

# Ensure Settings reads the correct .env
os.environ.setdefault("ENV_FILE", str(PROJECT_ROOT / ".env"))

# --- Import your models Base & settings AFTER path/env setup ---
from app.db.session import Base
from app.db.models import *  # noqa: F401,F403
from app.core.config import settings

# --- Alembic config ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Optional: set sqlalchemy.url so Alembic logs show the target DSN (it won't be used for async connect)
url_sync = settings.mysql_dsn.replace("+asyncmy", "+pymysql")
config.set_main_option("sqlalchemy.url", url_sync.replace("%", "%%"))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.mysql_dsn
    # Alembic offline mode doesn't support async drivers; swap to sync URL for rendering if needed
    url_sync = url.replace("+asyncmy", "+pymysql")

    context.configure(
        url=url_sync,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable: AsyncEngine = create_async_engine(
        settings.mysql_dsn,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
