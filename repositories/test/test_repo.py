from copy import deepcopy
from datetime import datetime

from models.property import AdvertisedProperty


def create_advertised_1():
    return AdvertisedProperty(
        url='http://somewhere.nice.location',
        address='Nice Location 1',
        price=1200,
        provided_by='rent',
        entered=datetime(2018, 9, 1, 19, 32, 10),
        commute=20,
        flagged=False,
        sent_email=True,
        ok=True,
    )


advertised_1_dict = dict(
    property_id=1,
    url='http://somewhere.nice.location',
    address='Nice Location 1',
    price=1200,
    provided_by='rent',
    entered=datetime(2018, 9, 1, 19, 32, 10),
    commute=20,
    flagged=False,
    sent_email=True,
    ok=True,
    row=None,
)


def create_advertised_2():
    return AdvertisedProperty(
        url='http://ehh.nice.location',
        address='Sandyford Road 3',
        price=1400,
        provided_by='rent',
        entered=datetime(2018, 9, 1, 19, 32, 45),
        commute=20,
        flagged=False,
        sent_email=True,
        ok=True,
    )


def create_advertised_3():
    return AdvertisedProperty(
        url='http://somewhere.nowhere',
        address='Ehhh 1',
        price=1400,
        provided_by='let',
        entered=datetime(2018, 9, 2, 18, 32, 10),
        commute=20,
        flagged=True,
        sent_email=True,
        ok=True,
    )


def create_advertised_4():
    return AdvertisedProperty(
        url='http://somewhere.nice.location',
        address='Nice Location 1',
        price=1200,
        provided_by='let',
        entered=datetime(2017, 9, 1, 19, 32, 10),
        commute=20,
        flagged=False,
        sent_email=False,
        ok=True,
    )


def create_advertised_5():
    return AdvertisedProperty(
        url='http://somewhere.nice.location',
        address='XD 1',
        price=1200,
        provided_by='daft',
        entered=datetime(2018, 9, 1, 19, 32, 10),
        commute=20,
        flagged=True,
        sent_email=False,
        ok=False,
    )


class TestRepository(object):
    def test_property_to_dict(self):
        property_dict = self.repo._property_to_dict(create_advertised_1())
        expected_dict = deepcopy(advertised_1_dict)
        expected_dict['property_id'] = None

        self.assertDictEqual(property_dict, expected_dict)

    def test_property_save(self):
        advertised_1 = create_advertised_1()
        self.repo.save(advertised_1)
        self.assertEqual(advertised_1.property_id, 1)

    def test_property_get(self):
        advertised_1 = create_advertised_1()
        self.repo.save(advertised_1)
        retrieved_1 = self.repo.get(1)

        self.assertEqual(advertised_1, retrieved_1)

    def test_property_update(self):
        advertised_1 = create_advertised_1()
        self.repo.save(advertised_1)
        retrieved_1 = self.repo.get(1)

        advertised_1.url = 'nothing'
        self.assertNotEqual(advertised_1, retrieved_1)

        self.repo.update(advertised_1)
        retrieved_1 = self.repo.get(1)
        self.assertEqual(advertised_1, retrieved_1)

    def _save_all(self):
        for i, obj in enumerate(
                [create_advertised_1(), create_advertised_2(),
                 create_advertised_3(), create_advertised_4(),
                 create_advertised_5()]):
            self.repo.save(obj)
            self.default[i + 1] = obj

    def test_list_all(self):
        self._save_all()
        properties_list = self.repo.list_all()
        self.assertListEqual(
            properties_list,
            [self.default[1], self.default[2], self.default[3],
             self.default[4], self.default[5]]
        )

    def test_list_all_flagged(self):
        self._save_all()
        properties_list = self.repo.list_flagged()
        self.assertListEqual(properties_list,
                             [self.default[3], self.default[5]])

    def test_list_ok(self):
        self._save_all()
        properties_list = self.repo.list_ok()
        self.assertListEqual(properties_list,
                             [self.default[1], self.default[2],
                              self.default[3], self.default[4]])

    def test_list_last_from(self):
        self._save_all()

        self.assertEqual(self.repo.get_last_from('let'), self.default[3])
        self.assertEqual(self.repo.get_last_from('rent'), self.default[2])
        self.assertEqual(self.repo.get_last_from('daft'), self.default[5])
