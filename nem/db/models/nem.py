
from decimal import Decimal
from typing import List, Optional

from dictalchemy import DictableModel
from geoalchemy2 import Geometry
from shapely import wkb
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    Numeric,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from nem.utils.sql import time_bucket

Base = declarative_base(cls=DictableModel)
metadata = Base.metadata

class BaseModel(object):
    """
    Base model for both NEM and WEM

    """

    created_by = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class FacilityScada(Base, BaseModel):
    """
    Facility Scada
    """

    __tablename__ = "facility_scada"

    def __str__(self) -> str:
        return "<{}: {} {} {}>".format(
            self.__class__,
            self.trading_interval,
            self.network_id,
            self.facility_code,
        )

    def __repr__(self) -> str:
        return "{}: {} {} {}".format(
            self.__class__,
            self.trading_interval,
            self.network_id,
            self.facility_code,
        )

    network_id = Column(
        Text,
        ForeignKey("network.code", name="fk_balancing_summary_network_code"),
        primary_key=True,
        nullable=False,
    )
    network = relationship("Network")

    trading_interval = Column(
        TIMESTAMP(timezone=True), index=True, primary_key=True, nullable=False
    )

    facility_code = Column(Text, nullable=False, primary_key=True, index=True)
    generated = Column(Numeric, nullable=True)
    is_forecast = Column(Boolean, default=False, primary_key=True)
    eoi_quantity = Column(Numeric, nullable=True)
    energy_quality_flag = Column(Numeric, nullable=False, default=0)

    __table_args__ = (
        Index(
            "idx_facility_scada_facility_code_trading_interval",
            facility_code,
            trading_interval.desc(),
        ),
        Index("idx_facility_scada_network_id", network_id),
        Index(
            "idx_facility_scada_network_id_trading_interval", network_id, trading_interval.desc()
        ),
        Index(
            "idx_facility_scada_trading_interval_facility_code", trading_interval, facility_code
        ),
        # This index is used by aggregate tables
        Index(
            "idx_facility_scada_trading_interval_desc_facility_code",
            time_bucket("'00:30:00'::interval", trading_interval).desc(),
            facility_code,
        ),
    )