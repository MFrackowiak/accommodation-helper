import sqlite3
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

        self.engine = create_engine(f'sqlite:///{db_name}', encoding='utf-8',
                                    echo=True)
        self.session_maker = sessionmaker(bind=self.engine)
        self._init_db()

    def _in_session(func) -> Callable:
        @wraps(func)
        def session_wrapper(self, *args, **kwargs):
            if self.session is None:
                self.init_session()
            try:
                func(self, *args, **kwargs)
                if self.auto_commit:
                    self.commit()
            except:
                self.rollback()
                raise
            finally:
                if self.auto_commit:
                    self.finalize_session()
        return session_wrapper

    def _init_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

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

    @_in_session
    def save(self, advertised_property: AdvertisedProperty):

        insert = self.properties.insert().values(
            **self._property_to_dict(advertised_property),
        )
        result = self.session.execute(insert)
        advertised_property.property_id = result.inserted_primary_key[0]

    @_in_session
    def update(self, advertised_property: AdvertisedProperty):
        pass

    @_in_session
    def get(self, property_id: int) -> AdvertisedProperty:
        pass

    @_in_session
    def list_flagged(self) -> List[AdvertisedProperty]:
        pass

    @_in_session
    def list_mail_sent(self) -> List[AdvertisedProperty]:
        pass

    @_in_session
    def list_all(self) -> List[AdvertisedProperty]:
        pass

    @_in_session
    def delete_all(self):
        pass

    @_in_session
    def get_last_from(self, provider) -> Optional[AdvertisedProperty]:
        pass

    @_in_session
    def list_ok(self) -> List[AdvertisedProperty]:
        pass

    def init_session(self):
        self.session = self.session_maker()

    def finalize_session(self):
        self.session.close()
        self.session = None

    def rollback(self):
        if self.session:
            self.session.rollback()

    def commit(self):
        if self.session:
            self.session.commit()
