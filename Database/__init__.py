#!/usr/bin/env python3

from sqlalchemy import Column, Integer, Float, String, ForeignKey, create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pathlib import Path

Base = declarative_base()

path = Path(__file__).parent / "transactions.db"
engine = create_engine(f"sqlite:////{path}")
if not database_exists(engine.url):
    create_database(engine.url)

class Transactors(Base):
    __tablename__ = "transactors"

    name = mapped_column(String, primary_key=True)


class TransactionType(Base):
    __tablename__ = "transaction_type"

    maintype = mapped_column(String, primary_key=True)


class TransactionSubtype(Base):
    __tablename__ = "transaction_subtype"

    subtype = Column(String, primary_key=True)


class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = mapped_column(Integer, primary_key=True)
    transactor = mapped_column(String, ForeignKey("transactors.name"))
    shared = mapped_column(Integer)
    date = mapped_column(String)
    transaction_type = mapped_column(String, ForeignKey("transaction_type.maintype"))
    transaction_subtype = mapped_column(String, ForeignKey("transaction_subtype.subtype"))
    amount = mapped_column(Float)
    description = mapped_column(String)

Base.metadata.create_all(engine)
