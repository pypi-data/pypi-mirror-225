import enum
from typing import Dict, Union

from sqlalchemy.orm import Session, sessionmaker, Query
from sqlalchemy.sql.elements import or_, Label
from sqlalchemy.util import hybridproperty

from .InstancesTags import InstancesTags

try:
    from sqlalchemy import Column, engine, case, func, cast, String, text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.dialects.postgresql import BOOLEAN, FLOAT, INTEGER, BIGINT, \
        JSON, TIMESTAMP, VARCHAR
except ImportError:
    raise ImportError("sqlalchemy is required by zesty.zbs-api but needs to be vendored separately. Add postgres-utils to your project's requirements that depend on zbs-api.")


Base = declarative_base()


class EbsVolumeConfig(enum.Enum):
    none = 'None'
    unattached = 'Unattached'
    potentialZesty = 'Potential ZestyDisk'


class EbsVolume(Base):
    # TODO: Move this model into our Alembic system
    # when a modification of this model is needed.
    __tablename__ = "disks"

    volume_id = Column(VARCHAR, primary_key=True)
    org_id = Column(VARCHAR, index=True)
    account_uuid = Column(VARCHAR, index=True)
    account_id = Column(VARCHAR, index=True)
    region = Column(VARCHAR, index=True)
    volume_type = Column(VARCHAR, index=True)
    cloud = Column(VARCHAR, index=True)
    availability_zone = Column(VARCHAR)
    create_time = Column(TIMESTAMP)
    encrypted = Column(BOOLEAN)
    size = Column(INTEGER)
    snapshot_id = Column(VARCHAR)
    state = Column(VARCHAR)
    iops = Column(INTEGER)
    tags = Column(JSON)
    attachments = Column(JSON)
    attached_to = Column(JSON)
    monthly_cost = Column(FLOAT, default=0)
    is_unused_resource = Column(INTEGER, default=0)
    unused_since = Column(VARCHAR)
    agent_installed = Column(BOOLEAN, default=False)
    _zbs_supported_os = Column(INTEGER)
    potential_savings = Column(FLOAT, default=0)

    # dict for custom_order_by class method
    col_to_actual_sorting_col = {"instance_tags": "instance_tags_keys"}

    def __init__(
            self,
            volume_aws_schema: Dict,
            account_uuid: str = None):
        if account_uuid:
            self.account_uuid = account_uuid
        else:
            self.account_uuid = volume_aws_schema["account_uuid"]

        self.volume_id = volume_aws_schema["volume_id"]
        self.org_id = volume_aws_schema["org_id"]
        self.account_id = volume_aws_schema["account_id"]
        self.cloud = volume_aws_schema["cloud"]
        self.region = volume_aws_schema["region"]
        self.volume_type = volume_aws_schema["volume_type"]
        self.availability_zone = volume_aws_schema["availability_zone"]
        self.create_time = volume_aws_schema["create_time"]
        self.encrypted = volume_aws_schema["encrypted"]
        self.size = volume_aws_schema["size"]
        self.snapshot_id = volume_aws_schema["snapshot_id"]
        self.state = volume_aws_schema["state"]
        self.iops = volume_aws_schema.get("iops", 0)
        self.tags = volume_aws_schema.get("tags", {})
        self.attachments = volume_aws_schema.get("attachments", [])
        self.attached_to = volume_aws_schema.get("attached_to", [])
        self.monthly_cost = volume_aws_schema.get("monthly_cost", 0)
        self.is_unused_resource = volume_aws_schema.get(
            "is_unused_resource", 0)
        self.unused_since = volume_aws_schema.get("unused_since", None)
        self.agent_installed = volume_aws_schema.get("agent_installed", False)
        self._zbs_supported_os = volume_aws_schema.get("_zbs_supported_os")
        self.potential_savings = volume_aws_schema.get("potential_savings", 0)

    def __repr__(self):
        return f"{self.__tablename__}:{self.volume_id}"

    @classmethod
    def instance_id_filter(cls, query: Query, value: str):
        val = f'%{value}%'
        query = query.filter(
            case((or_(cls.attached_to == None, func.json_array_length(cls.attached_to) == 0), False),
                 else_=cast(cls.attached_to, String).ilike(val)))
        return query

    @classmethod
    def instance_name_filter(cls, query: Query, value: str):
        subq = query.session.query(InstancesTags.instance_name)
        val = '%{}%'.format(value.replace("%", "\\%"))
        query = query.filter((subq.scalar_subquery().where(
            (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) & (
                cls.account_id == InstancesTags.account_id))).ilike(val))
        return query

    @classmethod
    def instance_tags_filter(cls, query: Query, value: str):
        session = query.session
        subq = session.query(InstancesTags.instance_tags)

        python_types_to_pg = {int: BIGINT, float: FLOAT, bool: BOOLEAN}
        for key_val in value:
            key = key_val.get('key')
            val = key_val.get('value')
            if key is not None and val is not None:
                if not isinstance(val, str):
                    query = query.filter(cast(cast(func.jsonb(subq.scalar_subquery().where(
                        (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) & (cls.account_id == InstancesTags.account_id)).op('->')(key)), String), python_types_to_pg[type(val)]) == val)
                else:
                    val = f'%{val}%'
                    query = query.filter(cast(func.jsonb(subq.scalar_subquery().where(
                        (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) & (cls.account_id == InstancesTags.account_id)).op('->')(key)), String).ilike(val))
            elif key is not None:
                query = query.filter(func.jsonb(subq.scalar_subquery().where(
                        (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) & (cls.account_id == InstancesTags.account_id))).op('?')(key))
            elif val is not None:
                if isinstance(val, str):
                    query = query.filter(cast(subq.scalar_subquery().where(
                            (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) & (cls.account_id == InstancesTags.account_id)), String)
                                         .regexp_replace(r'.+\: "[^"]*(' + str(val) + r')[^"]*"[,\s}].*', "\\1") == f"{val}")
                else:
                    if isinstance(val, bool):
                        val = f'"{val}"'
                    query = query.filter(cast(subq.scalar_subquery().where(
                            (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) & (cls.account_id == InstancesTags.account_id)), String)
                                         .regexp_replace(r'.+\: (' + str(val) + r')[,\s}].*', "\\1") == f"{val}")
        return query

    # Custom query
    @classmethod
    def custom_query(cls, session: Union[Session, sessionmaker]) -> Query:
        q = session.query(cls)
        subq_2 = session.query(func.json_object_keys(InstancesTags.instance_tags))
        subq_3 = session.query(InstancesTags.instance_tags)

        instance_name_clause = "regexp_replace(cast(array((select instances_tags.instance_name from instances_tags " \
                               "inner join json_array_elements(disks.attached_to) as attached_to_set " \
                               "on instances_tags.instance_id = replace(cast(attached_to_set.value as varchar), '\"', '') " \
                               "and instances_tags.account_id = disks.account_id)) as varchar), '[\\{\\}\"]', '', 'g')"

        q = q.add_columns(case((or_(cls.attached_to == None, func.json_array_length(cls.attached_to) == 0), ''),
                               else_=cast(cls.attached_to, String).regexp_replace(r'[\[\]"]', '', 'g'))
                          .label("instance_id"),
                          Label('instance_name', text(instance_name_clause)),
                          func.array(subq_2.scalar_subquery().where(
                              (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) &
                              (cls.account_id == InstancesTags.account_id)))
                          .label('instance_tags_keys'),
                          subq_3.scalar_subquery().where(
                              (func.jsonb(cls.attached_to).op('->>')(0) == InstancesTags.instance_id) &
                              (cls.account_id == InstancesTags.account_id))
                          .label('instance_tags'))

        return q

    @classmethod
    def custom_order_by(cls, sorting_column: str, sorting_order: str) -> str:
        actual_sorting_column = cls.col_to_actual_sorting_col.get(sorting_column, sorting_column)

        return f"{actual_sorting_column} {sorting_order}"

    def get_volume_id(self):
        return self.volume_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @hybridproperty
    def configuration(self):
        if self.attached_to and self.volume_type in ["gp2", "gp3", "io1", "io2"] and self.size > 100:
            return EbsVolumeConfig.potentialZesty.value
        if not self.attached_to:
            return EbsVolumeConfig.unattached.value
        return EbsVolumeConfig.none.value


def create_tables(engine: engine.base.Engine) -> None:  #type: ignore
    Base.metadata.create_all(engine, checkfirst=True)
