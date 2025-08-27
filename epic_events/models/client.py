from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Foreign keys
    commercial_contact_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    commercial_contact = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")
