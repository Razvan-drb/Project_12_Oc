from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    is_signed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Foreign keys
    client_id = Column(Integer, ForeignKey('clients.id'))
    commercial_contact_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    client = relationship("Client", back_populates="contracts")
    commercial_contact = relationship("User", back_populates="contracts")
    event = relationship("Event", back_populates="contract", uselist=False)