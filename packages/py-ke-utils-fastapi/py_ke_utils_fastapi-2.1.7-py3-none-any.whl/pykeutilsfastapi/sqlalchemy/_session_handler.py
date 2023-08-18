import logging
from typing import Annotated

from alembic import command
from alembic.config import Config
from fastapi import Header, HTTPException, status
from sqlalchemy import inspect, text, Engine,create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeMeta

from ..tenant import tenant_extractor


class SessionHandler:
    """
    Dependency class for FastAPI. It handles the sessions for API.
    :param session_local: The SessionMaker of the API.
    :param engine: The SQLAlchemy Database engine.
    :param base_metadata: DeclarativeMeta (Base used to create tables).
    :param default_tenant: Default tenant.
    :param db_url: database url to connect to
    """

    def __init__(
            self,
            session_local: sessionmaker,
            engine: Engine,
            base_metadata: DeclarativeMeta,
            default_tenant: str = 'public',
            db_url: str = "",
    ):
        self.session_local = session_local
        self.engine = engine
        self.base_metadata= base_metadata
        self.default_tenant = default_tenant
        self.db_url = db_url

    def __call__(
            self,
            x_tenant_id: Annotated[str | None, Header()] = None,
            origin: Annotated[str | None, Header()] = None,
    ) -> Session:
        session = self.session_local()
        try:
            subdomain = f"tenant_{tenant_extractor(str(origin), x_tenant_id, self.default_tenant)}"
            if subdomain not in inspect(self.engine).get_schema_names():
                logging.error(f"Schema - {subdomain} is not in the database.")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Schema {subdomain} does not exists in the database",
                )
            logging.info("Changing Schema.")
            session.execute(text(f"SET search_path TO {subdomain}"))
            table_engine = create_engine(
                self.db_url,
                connect_args={'options': f'-csearch_path={subdomain}'},
            )
            self.base_metadata.metadata.create_all(table_engine)
            logging.info("Upgrading Database.")
            yield session
        finally:
            session.close()
