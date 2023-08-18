import time
from enum import Enum, auto
from typing import Dict, List, Optional, Union
from uuid import UUID as _UUID
from uuid import uuid4

from sqlalchemy import Enum as sa_ENUM
from sqlalchemy import INT
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID

try:
    from sqlalchemy import Column, String, case, cast, engine, func, or_
    from sqlalchemy.dialects.postgresql import (BIGINT, BOOLEAN, FLOAT, JSON,
                                                TIMESTAMP, VARCHAR)
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import Query, Session, aliased, sessionmaker
except ImportError:
    raise ImportError(
        "sqlalchemy is required by zesty.zbs-api but needs to be vendored separately. Add postgres-utils to your project's requirements that depend on zbs-api.")

from ..actions import ZBSAction
from .BlockDevice import BlockDevice
from .Usage import Usage

Base = declarative_base()


class BaseMixin:
    """Base for database models with some default fields"""

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())


class ManagedFsMixin:
    fs_id = Column(VARCHAR, primary_key=True)
    account_id = Column(VARCHAR, index=True, default=None)
    account_uuid = Column(VARCHAR, index=True, default=None)
    agent_update_required = Column(BOOLEAN, default=None)
    btrfs_version = Column(VARCHAR, default=None)
    cloud = Column(VARCHAR, default=None)
    cloud_vendor = Column(VARCHAR, default=None)
    cycle_period = Column(BIGINT, default=None)
    delete_on_termination = Column(BOOLEAN, default=None)
    devices = Column(JSON, default=None)
    encrypted = Column(JSON, default=None)
    existing_actions = Column(JSON, default=None)
    expiredAt = Column(BIGINT, default=None)
    fs_cost = Column(FLOAT, default=None)
    fs_devices_to_count = Column(BIGINT, default=None)
    fs_size = Column(BIGINT, default=None)
    fs_type = Column(VARCHAR, default=None)
    fs_usage = Column(BIGINT, default=None)
    has_unallocated_space = Column(BOOLEAN, default=None)
    inodes = Column(JSON, default=None)
    instance_id = Column(VARCHAR, default=None)
    instance_type = Column(VARCHAR, default=None)
    is_ephemeral = Column(BOOLEAN, default=None)
    is_partition = Column(BOOLEAN, default=None)
    is_zesty_disk = Column(BOOLEAN, default=None)
    label = Column(VARCHAR, default=None)
    last_update = Column(BIGINT, default=None)
    LV = Column(VARCHAR, default=None)
    lvm_path = Column(VARCHAR, default=None)
    mount_path = Column(VARCHAR, default=None)
    name = Column(VARCHAR, default=None)
    org_id = Column(VARCHAR, index=True)
    partition_id = Column(VARCHAR, default=None)
    partition_number = Column(BIGINT, default=None)
    platform = Column(VARCHAR, default=None)
    potential_savings = Column(FLOAT, default=None)
    region = Column(VARCHAR, index=True)
    resizable = Column(BOOLEAN, default=None)
    space = Column(JSON, default=None)
    tags = Column(JSON, default=None)
    unallocated_chunk = Column(BIGINT, default=None)
    update_data_ts = Column(BIGINT, default=0)
    VG = Column(VARCHAR, default=None)
    wrong_fs_alert = Column(BOOLEAN, default=None)
    zesty_disk_iops = Column(BIGINT, default=None)
    zesty_disk_throughput = Column(BIGINT, default=None)
    zesty_disk_vol_type = Column(VARCHAR, default=None)
    max_utilization_in_72_hrs = Column(BIGINT, default=None)
    package_version = Column(VARCHAR, default=None)
    autoupdate_last_execution_time = Column(VARCHAR, default=None)
    policies = Column(JSON, default=None)
    instance_tags = Column(JSON, default=None)
    migration_uuid = Column(UUID(as_uuid=True), nullable=True)
    is_manageable = Column(BOOLEAN, default=False)

    # dict for custom_order_by class method
    col_to_actual_sorting_col = {
        "policies": "policies_name",
        "instance_tags": "instance_tags_keys"}

    def __init__(
            self,
            fs_id: str,
            account_id: str = None,
            account_uuid: str = None,
            agent_update_required: bool = None,
            btrfs_version: str = None,
            cloud: str = None,
            cloud_vendor: str = None,
            cycle_period: int = None,
            delete_on_termination: bool = None,
            devices: Dict[str, BlockDevice] = None,
            encrypted: dict = None,
            existing_actions: Dict[str, ZBSAction] = None,
            expiredAt: int = None,
            fs_cost: float = None,
            fs_devices_to_count: int = None,
            fs_size: int = None,
            fs_type: str = None,
            fs_usage: int = None,
            has_unallocated_space: bool = None,
            inodes: Dict[str, Usage] = None,
            instance_id: str = None,
            instance_type: str = None,
            is_ephemeral: bool = None,
            is_partition: bool = None,
            is_zesty_disk: bool = None,
            label: str = None,
            last_update: int = None,
            LV: str = None,
            lvm_path: str = None,
            mount_path: str = None,
            name: str = None,
            org_id: str = None,
            partition_id: str = None,
            partition_number: int = None,
            platform: str = None,
            potential_savings: float = None,
            region: str = None,
            resizable: bool = None,
            space: Dict[str, Usage] = None,
            tags: Dict[str, str] = None,
            unallocated_chunk: int = None,
            update_data_ts: int = 0,
            VG: str = None,
            wrong_fs_alert: bool = None,
            zesty_disk_iops: int = None,
            zesty_disk_throughput: int = None,
            zesty_disk_vol_type: str = None,
            max_utilization_in_72_hrs: int = None,
            package_version: str = None,
            autoupdate_last_execution_time: str = None,
            statvfs_raw_data: Dict[str, str] = None,  # unused to support initialization with **dict, do not remove
            policies: Dict[str, dict] = None,
            instance_tags: Dict[str, str] = None,
            is_emr: bool = False,  # unused to support initialization with **dict, do not remove
            is_manageable: bool = False,
            **kwargs
    ):
        self.fs_id = fs_id
        self.account_id = account_id
        self.account_uuid = account_uuid
        self.agent_update_required = agent_update_required
        self.btrfs_version = btrfs_version
        if cloud is None and cloud_vendor is None:
            self.cloud = 'Amazon'
            self.cloud_vendor = 'Amazon'
        elif cloud:
            self.cloud = cloud
            self.cloud_vendor = cloud
        elif cloud_vendor:
            self.cloud = cloud_vendor
            self.cloud_vendor = cloud_vendor
        self.cycle_period = cycle_period
        self.delete_on_termination = delete_on_termination
        self.devices = devices
        if devices:
            for dev in self.devices:
                if isinstance(self.devices[dev], BlockDevice):
                    self.devices[dev] = self.devices[dev].asdict()
                else:
                    self.devices[dev] = self.devices.get(dev, {})
        self.encrypted = encrypted
        if existing_actions:
            for action in existing_actions:
                self.existing_actions[action] = self.existing_actions[action].serialize(
                )
        self.expiredAt = expiredAt
        self.fs_cost = fs_cost
        self.fs_devices_to_count = fs_devices_to_count
        self.fs_size = fs_size
        self.fs_type = fs_type
        self.fs_usage = fs_usage
        self.has_unallocated_space = has_unallocated_space
        self.inodes = inodes
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.is_ephemeral = is_ephemeral
        self.is_partition = is_partition
        self.is_zesty_disk = is_zesty_disk
        self.label = label
        if last_update:
            self.last_update = last_update
        else:
            self.last_update = int(time.time()) - 60
        self.LV = LV
        self.lvm_path = lvm_path
        self.mount_path = mount_path
        self.name = name
        self.org_id = org_id
        self.partition_id = partition_id
        self.partition_number = partition_number
        self.platform = platform
        self.potential_savings = potential_savings
        self.region = region
        self.resizable = resizable
        self.space = space
        self.tags = tags
        self.unallocated_chunk = unallocated_chunk
        self.update_data_ts = update_data_ts
        self.VG = VG
        self.wrong_fs_alert = wrong_fs_alert
        self.zesty_disk_iops = zesty_disk_iops
        self.zesty_disk_throughput = zesty_disk_throughput
        self.zesty_disk_vol_type = zesty_disk_vol_type
        self.max_utilization_in_72_hrs = max_utilization_in_72_hrs
        self.package_version = package_version
        self.autoupdate_last_execution_time = autoupdate_last_execution_time
        self.policies = policies
        self.instance_tags = instance_tags
        self.is_manageable = is_manageable

    def __repr__(self) -> str:
        return f"{self.__tablename__}:{self.fs_id}"

    def asdict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict(self) -> dict:
        return self.asdict()

    # Custom filters
    @classmethod
    def policies_filter(cls, query: Query, value: str):
        query = query.filter(
            cast(cls.policies, String).contains(f'"name": "{value}"'))
        return query

    @classmethod
    def instance_name_filter(cls, query: Query, value: str):
        val = '%{}%'.format(value.replace("%", "\\%"))
        query = query.filter(
            case((cls.instance_tags == None, ''), else_=func.replace(cast(cls.instance_tags.op('->')('Name'), String), "\"", "")).ilike(val))
        return query

    # Custom query
    @classmethod
    def custom_query(cls, session: Union[Session, sessionmaker]) -> Query:
        clsb = aliased(cls)
        subq = session.query(func.json_object_keys(clsb.instance_tags))
        q = session.query(cls)
        q = q.add_columns(case((or_(cls.policies == None, cast(cls.policies, String) == 'null'), ''),
                               else_=cast(cls.policies, String).regexp_replace(r'.+"name":\s"([^"]+).+', "\\1"))
                          .label("policies_name"),
                          case((cls.instance_tags == None, ''),
                               else_=func.replace(cast(cls.instance_tags.op('->')('Name'), String), "\"", ""))
                          .label('instance_name'),
                          case((cast(cls.instance_tags, String) == 'null', []),
                               else_=func.array(subq.scalar_subquery().where(cls.fs_id == clsb.fs_id)))
                          .label('instance_tags_keys')
                          )
        return q

    @classmethod
    def custom_order_by(cls, sorting_column: str, sorting_order: str) -> str:
        actual_sorting_column = cls.col_to_actual_sorting_col.get(
            sorting_column, sorting_column)

        return f"{actual_sorting_column} {sorting_order}"


class ManagedFs(ManagedFsMixin, BaseMixin, Base):
    __tablename__ = "managed_filesystems"


class MigrationStatus(Enum):
    Active = auto()
    Aborting = auto()
    Aborted = auto()
    Completed = auto()
    Failed = auto()


class RunningMigrations(BaseMixin, Base):
    __tablename__ = "active_migration"

    fs_id = Column(VARCHAR)
    migration_uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    finished_at = Column(TIMESTAMP, nullable=True)
    account_id = Column(VARCHAR, default=None)
    region = Column(VARCHAR(255))

    reboot = Column(BOOLEAN, default=False)
    # array of day numbers when reboot is allowed 0-6
    days = Column(ARRAY(VARCHAR))
    # timeframe from-to in %I:%M %p
    from_ = Column(VARCHAR)
    to = Column(VARCHAR)

    status = Column(sa_ENUM(MigrationStatus), nullable=False, server_default=MigrationStatus.Active.name)
    is_rebooting = Column(BOOLEAN, default=False)  # TODO: can this be deleted?

    snapshot_id = Column(VARCHAR(255))
    snapshot_remove_after = Column(INT, nullable=True)  # in days
    snapshot_create_started_at = Column(TIMESTAMP, nullable=True)
    snapshot_deleted_at = Column(TIMESTAMP, nullable=True)

    ebs_id = Column(VARCHAR(255))
    ebs_remove_after = Column(INT, nullable=True)  # in days
    ebs_detached_at = Column(TIMESTAMP, nullable=True)
    ebs_deleted_at = Column(TIMESTAMP, nullable=True)

    def __init__(
            self,
            fs_id: str,
            migration_uuid: _UUID,
            account_id: str = None,
            region: str = None,
            days: Optional[List[int]] = None,
            from_: Optional[str] = None,
            to: Optional[str] = None,
            reboot: bool = False,
            status: MigrationStatus = MigrationStatus.Active,
            ebs_remove_after: int = 1,
            snapshot_remove_after: int = 7):
        self.migration_uuid = migration_uuid
        self.fs_id = fs_id
        self.account_id = account_id
        self.region = region
        self.days = days
        self.from_ = from_
        self.to = to
        self.reboot = reboot
        self.status = status
        self.ebs_remove_after = ebs_remove_after
        self.snapshot_remove_after = snapshot_remove_after

    @staticmethod
    def new_migration(
            fs_id,
            days: Optional[List[int]] = None,
            from_: Optional[str] = None,
            to: Optional[str] = None,
            reboot: bool = False,
            ebs_remove_after: int = 1,
            snapshot_remove_after: int = 7) -> 'RunningMigrations':
        return RunningMigrations(
            fs_id,
            uuid4(),
            days, from_,
            to, reboot,
            ebs_remove_after,
            snapshot_remove_after,
        )


class MigrationHistory(BaseMixin, Base):
    __tablename__ = "migration_history"

    time_start = Column(TIMESTAMP)
    time_end = Column(TIMESTAMP)
    status = Column(VARCHAR)
    phase = Column(VARCHAR, primary_key=True)
    progress = Column(FLOAT)
    completed = Column(BOOLEAN)
    failed = Column(BOOLEAN)
    failure_reason = Column(VARCHAR)
    fs_id = Column(VARCHAR)
    migration_uuid = Column(UUID(as_uuid=True), ForeignKey("active_migration.migration_uuid",  ondelete="CASCADE"),
                            nullable=False, primary_key=True, index=True)
    # should be returned from the agent in seconds
    estimated = Column(INT)
    name = Column(VARCHAR)
    weight = Column(INT)
    abortable = Column(BOOLEAN)
    index = Column(INT, primary_key=True)

    def __init__(
            self,
            status: str,
            phase: str,
            progress: int,
            eta: int,
            name: str,
            weight: int,
            abortable: bool,
            start_time: int,
            end_time: int,
            migration_uuid: 'UUID',
            fs_id: str,
            index: int):
        self.status = status
        self.phase = phase
        self.progress = progress
        self.estimated = eta
        self.name = name
        self.weight = weight
        self.time_start = start_time
        self.time_end = end_time
        self.abortable = abortable
        self.index = index

        self.migration_uuid = migration_uuid
        self.fs_id = fs_id


class WrongActionException(Exception):
    pass


class MigrationActions(BaseMixin, Base):
    __tablename__ = "migration_actions"

    id = Column(INT, primary_key=True, autoincrement=True)
    fs_id = Column(VARCHAR)
    migration_uuid = Column(UUID(as_uuid=True), ForeignKey("active_migration.migration_uuid",  ondelete="CASCADE"),
                            nullable=False)
    action = Column(VARCHAR)
    value = Column(VARCHAR)

    allowed_actions = ['start', 'reboot', 'reboot_now', 'abort']

    def __init__(self, fs_id, migration_uuid, action, value):
        self.fs_id = fs_id
        self.migration_uuid = migration_uuid
        self.set_action(action)
        self.value = value

    def set_action(self, action):
        if action not in self.allowed_actions:
            raise WrongActionException
        self.action = action


def create_tables(engine: engine.base.Engine) -> None:
    Base.metadata.create_all(engine, checkfirst=True)
