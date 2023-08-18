import json
import time
from datetime import datetime
from typing import Dict, Union

from .ManagedFS import Base, BaseMixin

try:
    from sqlalchemy import (Column, PrimaryKeyConstraint, String, case, cast,
                            engine, func, or_, select, text)
    from sqlalchemy.dialects.postgresql import (BIGINT, BOOLEAN, FLOAT, JSON,
                                                VARCHAR)
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import Query, Session, aliased, sessionmaker
except ImportError:
    raise ImportError(
        "sqlalchemy is required by zesty.zbs-api but needs to be vendored separately. Add postgres-utils to your project's requirements that depend on zbs-api.")


class InstancesTags(BaseMixin, Base):
    __tablename__ = "instances_tags"

    instance_id = Column(VARCHAR, primary_key=True)
    account_id = Column(VARCHAR, index=True, default=None)
    account_uuid = Column(VARCHAR, index=True, default=None)
    instance_name = Column(VARCHAR, default=None)
    instance_tags = Column(JSON, default=None)
    expired_at = Column(BIGINT, default=None)

    __table_args__ = (
        PrimaryKeyConstraint('instance_id', name='instances_tags_pkey'),)

    def __init__(
            self,
            instance_id: str,
            account_id: str = None,
            account_uuid: str = None,
            instance_name: str = None,
            instance_tags: dict = None,
            expired_at: int = None
    ):
        self.instance_id = instance_id
        self.account_id = account_id
        self.account_uuid = account_uuid
        self.instance_name = instance_name
        self.instance_tags = instance_tags
        self.expired_at = expired_at or int(datetime.utcnow().timestamp()) + 3 * 3600

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash(''.join(map(lambda c: getattr(self, c.name) or '',
                                filter(lambda c: c.name not in ['instance_tags', 'expired_at', 'created_at', 'updated_at'],
                                       self.__table__.columns))) +
                    json.dumps(self.instance_tags))

    def __repr__(self) -> str:
        return f"{self.__tablename__}:{self.instance_id}"

    def asdict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict(self) -> dict:
        return self.asdict()


def create_tables(engine: engine.base.Engine) -> None:
    Base.metadata.create_all(engine, checkfirst=True)
