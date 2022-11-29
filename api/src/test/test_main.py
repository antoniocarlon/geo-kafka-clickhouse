import asyncio
import unittest

from unittest import mock

from ..app.main import kproducer, chclient, put_event, get_aggregation


class TestPutEvent(unittest.TestCase):

    @mock.patch.object(kproducer, 'send')
    def test_put_parameters_empty_timestamp(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(put_event(latitude=40.419903, longitude=-3.705793, mname='temperature', mvalue=29.3))

        mock_method.assert_called_once_with('gkch', res)
        assert res['timestamp'] is not None
        assert res['latitude']  == 40.419903
        assert res['longitude']  == -3.705793
        assert res['mname']  == 'temperature'
        assert res['mvalue']  == 29.3

    @mock.patch.object(kproducer, 'send')
    def test_put_parameters_with_timestamp(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(put_event(latitude=40.419903, longitude=-3.705793, mname='temperature', mvalue=29.3, timestamp=1234))

        mock_method.assert_called_once_with('gkch', res)
        assert res['timestamp'] == 1234
        assert res['latitude']  == 40.419903
        assert res['longitude']  == -3.705793
        assert res['mname']  == 'temperature'
        assert res['mvalue']  == 29.3


class TestGetAggregation(unittest.TestCase):

    @mock.patch.object(chclient, 'query')
    def test_get_aggregation_empty(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(get_aggregation())

        mock_method.assert_called_once_with("SELECT avg(mvalue) as mvalue FROM measurements WHERE 1 = 1")
        assert res is not None

    @mock.patch.object(chclient, 'query')
    def test_get_aggregation_agg(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(get_aggregation(aggregation='sum'))

        mock_method.assert_called_once_with("SELECT sum(mvalue) as mvalue FROM measurements WHERE 1 = 1")
        assert res is not None

    @mock.patch.object(chclient, 'query')
    def test_get_aggregation_mname(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(get_aggregation(mname='temperature'))

        mock_method.assert_called_once_with("SELECT avg(mvalue) as mvalue FROM measurements WHERE 1 = 1 AND mname = 'temperature'")
        assert res is not None

    @mock.patch.object(chclient, 'query')
    def test_get_aggregation_timestamp_ini(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(get_aggregation(timestamp_ini=1234))

        mock_method.assert_called_once_with("SELECT avg(mvalue) as mvalue FROM measurements WHERE 1 = 1 AND timestamp >= 1234")
        assert res is not None

    @mock.patch.object(chclient, 'query')
    def test_get_aggregation_timestamp_end(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(get_aggregation(timestamp_end=1234))

        mock_method.assert_called_once_with("SELECT avg(mvalue) as mvalue FROM measurements WHERE 1 = 1 AND timestamp <= 1234")
        assert res is not None

    @mock.patch.object(chclient, 'query')
    def test_get_aggregation_timestamp_polygon(self, mock_method):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(get_aggregation(polygon='random_polygon'))

        mock_method.assert_called_once_with("SELECT avg(mvalue) as mvalue FROM measurements WHERE 1 = 1 AND pointInPolygon((longitude, latitude), random_polygon)")
        assert res is not None
