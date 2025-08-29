from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(200), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Foreign keys
    client_id = Column(Integer, ForeignKey('clients.id'))
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    support_contact_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="event")
    support_contact = relationship("User", back_populates="events")
