from dataclasses import asdict
from functools import wraps
from typing import List, Optional, Callable, Dict

from sqlalchemy import DateTime, String, Integer, Column, Table, MetaData, \
    Boolean
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from models.advertised_property import AdvertisedProperty
from repositories.base import AdvertisedPropertyRepository


def _in_session(func) -> Callable:
    @wraps(func)
    def session_wrapper(self, *args, **kwargs):
        if self.session is None:
            self.init_session()
        try:
            result = func(self, *args, **kwargs)
            if self.auto_commit:
                self.commit()
            else:
                self.flush()
            return result
        except:
            self.rollback()
            raise
        finally:
            if self.auto_commit:
                self.finalize_session()

    return session_wrapper


class SqlAdvertisedPropertyRepository(AdvertisedPropertyRepository):
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
            Column('flagged', Boolean, default=False),
            Column('sent_email', Boolean, default=False),
            sqlite_autoincrement=True)
        self.properties_columns = [
            column.name for column in self.properties.c
        ]

        metadata.create_all(self.engine)

    def _property_to_dict(self, advertised: AdvertisedProperty) -> Dict:
        as_dict = asdict(advertised)
        as_dict.pop('property_id', None)
        return as_dict

    def _row_to_obj(self, row: tuple) -> AdvertisedProperty:
        return AdvertisedProperty(
            **dict(zip(self.properties_columns, row))
        )

    @_in_session
    def save(self, advertised_property: AdvertisedProperty):
        insert = self.properties.insert().values(
            **self._property_to_dict(advertised_property),
        )
        result = self.session.execute(insert)
        advertised_property.property_id = result.inserted_primary_key[0]

    @_in_session
    def update(self, advertised_property: AdvertisedProperty):
        update = self.properties.update(
            self.properties.c.property_id == advertised_property.property_id
        ).values(
            **self._property_to_dict(advertised_property)
        )
        self.session.execute(update)

    @_in_session
    def get(self, property_id: int) -> Optional[AdvertisedProperty]:
        select = self.properties.select(
            self.properties.c.property_id == property_id)
        result = self.session.execute(select)
        if result.rowcount == 0:
            return None
        return self._row_to_obj(result.fetchone())

    @_in_session
    def list_flagged(self) -> List[AdvertisedProperty]:
        select = self.properties.select(self.properties.c.flagged == True)
        result = self.session.execute(select)
        return [self._row_to_obj(row) for row in result.fetchall()]

    @_in_session
    def list_all(self) -> List[AdvertisedProperty]:
        select = self.properties.select()
        result = self.session.execute(select)
        return [self._row_to_obj(row) for row in result.fetchall()]

    @_in_session
    def delete_all(self):
        delete = self.properties.delete()
        self.session.execute(delete)

    @_in_session
    def get_last_from(self, provider) -> Optional[AdvertisedProperty]:
        select = self.properties.select(
            self.properties.c.provided_by == provider
        ).order_by(
            self.properties.c.entered.desc(),
        )
        result = self.session.execute(select)
        return self._row_to_obj(result.fetchone())

    @_in_session
    def list_ok(self) -> List[AdvertisedProperty]:
        select = self.properties.select(self.properties.c.ok == True)
        result = self.session.execute(select)
        return [self._row_to_obj(row) for row in result.fetchall()]

    @_in_session
    def list_with_url(self, url: str) -> List[AdvertisedProperty]:
        select = self.properties.select(self.properties.c.url == url)
        result = self.session.execute(select)
        return [self._row_to_obj(row) for row in result.fetchall()]

    @_in_session
    def list_with_similar_address(
            self, address: str, similarity_threshold: float=0.5
    )-> List[AdvertisedProperty]:
        select = self.properties.select(
            self.properties.c.address.ilike(f'%{address}%'))
        result = self.session.execute(select)
        return [self._row_to_obj(row) for row in result.fetchall()]

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
