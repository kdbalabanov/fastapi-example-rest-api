from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Date
from sqlalchemy.orm import relationship

from app.api.database import Base


class Ticker(Base):
    """
    Defines the tickers database table
    """
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    historical_prices = relationship('HistoricalData')


class HistoricalData(Base):
    """
    Defines the historical database table
    """
    __tablename__ = "historical"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=False, index=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'))
    low = Column(Numeric, unique=False)
    high = Column(Numeric, unique=False)
    open = Column(Numeric, unique=False)
    close = Column(Numeric, unique=False)
    volume = Column(Numeric, unique=False)
