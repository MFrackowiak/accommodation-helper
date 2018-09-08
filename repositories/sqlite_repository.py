from dataclasses import asdict
from functools import wraps
from typing import List, Optional, Callable, Dict

from sqlalchemy import DateTime, String, Integer, Column, Table, MetaData, \
    Boolean
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from models.property import AdvertisedProperty
from repositories.property import AdvertisedPropertyIRepository


class SqliteAdvertisedPropertyRepository(AdvertisedPropertyIRepository):
    def __init__(self, db_name, auto_commit=True):
        self.db_name = db_name
        self.auto_commit = auto_commit

        self.session = None

        self.engine = create_engine(
            f'postgresql+psycopg2://dublin:dublin@localhost/dublin',
            encoding='utf-8',
            echo=True)
        self.session_maker = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        metadata = MetaData()

        self.properties = Table(
            'properties', metadata,
            Column('property_id', Integer, primary_key=True),
            Column('url', String(200)),
            Column('address', String(200)),
            Column('price', Integer),
            Column('provided_by', String(10)),
            Column('entered', DateTime),
            Column('ok', Boolean, default=False),
            Column('row', Integer, nullable=True),
            Column('commute', Integer, default=0),
            Column('flagged', Boolean, default=False),
            Column('sent_email', Boolean, default=False),
            sqlite_autoincrement=True)

        metadata.create_all(self.engine)

    def _property_to_dict(self, advertised: AdvertisedProperty) -> Dict:
        as_dict = asdict(advertised)
        as_dict.pop('property_id', None)
        return as_dict

    def save(self, advertised_property: AdvertisedProperty):
        insert = self.properties.insert().values(
            **self._property_to_dict(advertised_property),
        )
        result = self.session.execute(insert)
        advertised_property.property_id = result.inserted_primary_key[0]

    def update(self, advertised_property: AdvertisedProperty):
        pass

    def get(self, property_id: int) -> Optional[AdvertisedProperty]:
        select = self.properties.select(
            self.properties.c.property_id == property_id)
        result = self.session.execute(select)
        if result.rowcount == 0:
            return None
        return result.fetchone()

    def list_flagged(self) -> List[AdvertisedProperty]:
        pass

    def list_mail_sent(self) -> List[AdvertisedProperty]:
        pass

    def list_all(self) -> List[AdvertisedProperty]:
        select = self.properties.select()
        result = self.session.execute(select)
        return result.fetchall()

    def delete_all(self):
        pass

    def get_last_from(self, provider) -> Optional[AdvertisedProperty]:
        pass

    def list_ok(self) -> List[AdvertisedProperty]:
        pass

    def init_session(self):
        self.session = self.session_maker()

    def finalize_session(self):
        if self.session:
            self.session.close()
            self.session = None

    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()

    def rollback(self):
        self.session.rollback()
