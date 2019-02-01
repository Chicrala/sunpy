import pytest
import unittest
import mock
from unittest.mock import patch
from unittest.mock import MagicMock

import astropy.units as u
from astropy.time import TimeDelta
from astropy.time import Time

from sunpy.time.timerange import TimeRange
from sunpy.net.dataretriever.client import QueryResponse
import sunpy.net.dataretriever.sources.norh as norh
from sunpy.net.fido_factory import UnifiedResponse
from sunpy.net import Fido
from sunpy.net import attrs as a

from hypothesis import given

from sunpy.net.tests.strategies import time_attr, range_time


@pytest.mark.remote_data
@pytest.mark.parametrize("timerange,url_start,url_end", [
    (TimeRange('2012/4/21', '2012/4/21'),
     'ftp://anonymous:data@sunpy.org@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/2012/04/tca120421',
     'ftp://anonymous:data@sunpy.org@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/2012/04/tca120421'
     ),
    (TimeRange('2012/12/1', '2012/12/2'),
     'ftp://anonymous:data@sunpy.org@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/2012/12/tca121201',
     'ftp://anonymous:data@sunpy.org@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/2012/12/tca121202'
     ),
    (TimeRange('2012/3/7', '2012/3/14'),
     'ftp://anonymous:data@sunpy.org@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/2012/03/tca120307',
     'ftp://anonymous:data@sunpy.org@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/2012/03/tca120314'
     )
])
def test_get_url_for_time_range(timerange, url_start, url_end):
    urls = norh.NoRHClient()._get_url_for_timerange(timerange, wavelength=17*u.GHz)
    assert isinstance(urls, list)
    assert urls[0] == url_start
    assert urls[-1] == url_end


@given(time_attr())
def test_can_handle_query(time):
    ans1 = norh.NoRHClient._can_handle_query(time, a.Instrument('norh'))
    assert ans1 is True
    ans1 = norh.NoRHClient._can_handle_query(time, a.Instrument('norh'),
                                             a.Wavelength(10*u.GHz))
    assert ans1 is True
    ans2 = norh.NoRHClient._can_handle_query(time)
    assert ans2 is False


@pytest.mark.remote_data
@pytest.mark.parametrize("wave", [a.Wavelength(17*u.GHz), a.Wavelength(34*u.GHz)])
@given(time=range_time(Time('1992-6-1')))
def test_query(time, wave):
    qr1 = norh.NoRHClient().search(time, a.Instrument('norh'), wave)
    assert isinstance(qr1, QueryResponse)
    # Not all hypothesis queries are going to produce results, and
    if qr1:
        # There are no observations everyday
        #  so the results found have to be equal or later than the queried time
        #  (looking at the date because it may search for miliseconds, but only date is available)
        assert qr1.time_range().start.strftime('%Y-%m-%d') >= time.start.strftime('%Y-%m-%d')
        #  and the end time equal or smaller.
        # hypothesis can give same start-end, but the query will give you from start to end (so +1)
        assert qr1.time_range().end <= time.end + TimeDelta(1*u.day)
        
#@patch('sunpy.net.dataretriever.sources.norh.NoRHClient.search', return_value='www.example.com')
def test_query_mock(time, wave):
    # Creating a context for this mock.
    with mock.patch('sunpy.net.dataretriever.sources.norh.NoRHClient.search', 
                    return_value='www.example.com') as mock_search:
        
        # Defining the atributes of it.
        mock_search.instance = QueryResponse
        
        qr1 = norh.NoRHClient().search(time, a.Instrument('norh'), wave)
        assert isinstance(qr1, QueryResponse)
        # Not all hypothesis queries are going to produce results, and
        if qr1:
            # There are no observations everyday
            #  so the results found have to be equal or later than the queried time
            #  (looking at the date because it may search for miliseconds, but only date is available)
            assert qr1.time_range().start.strftime('%Y-%m-%d') >= time.start.strftime('%Y-%m-%d')
            #  and the end time equal or smaller.
            # hypothesis can give same start-end, but the query will give you from start to end (so +1)
            assert qr1.time_range().end <= time.end + TimeDelta(1*u.day)


# Don't use time_attr here for speed.
def test_query_no_wave():
    c = norh.NoRHClient()
    with pytest.raises(ValueError):
        c.search(a.Time("2016/10/1", "2016/10/2"), a.Instrument('norh'))


def test_wavelength_range():
    with pytest.raises(ValueError):
        norh.NoRHClient().search(
            a.Time("2016/10/1", "2016/10/2"), a.Instrument('norh'),
            a.Wavelength(17 * u.GHz, 34 * u.GHz))


def test_query_wrong_wave():
    c = norh.NoRHClient()
    with pytest.raises(ValueError):
        c.search(a.Time("2016/10/1", "2016/10/2"), a.Instrument('norh'),
                a.Wavelength(50*u.GHz))


@pytest.mark.remote_data
@pytest.mark.parametrize("time,instrument,wave", [
    (a.Time('2012/10/4', '2012/10/6'), a.Instrument('norh'), a.Wavelength(17*u.GHz)),
    (a.Time('2013/10/5', '2013/10/7'), a.Instrument('norh'), a.Wavelength(34*u.GHz))])
def test_get(time, instrument, wave):
    LCClient = norh.NoRHClient()
    qr1 = LCClient.search(time, instrument, wave)
    res = LCClient.fetch(qr1)
    download_list = res.wait(progress=False)
    assert len(download_list) == len(qr1)


@pytest.mark.remote_data
@pytest.mark.parametrize(
    "time, instrument, wave",
    [(a.Time('2012/10/4', '2012/10/6'), a.Instrument('norh'), a.Wavelength(17*u.GHz)),
     (a.Time('2013/10/5', '2013/10/7'), a.Instrument('norh'), a.Wavelength(34*u.GHz))])
def test_fido(time, instrument, wave):
    qr = Fido.search(time, instrument, wave)
    assert isinstance(qr, UnifiedResponse)
    response = Fido.fetch(qr)
    assert len(response) == qr._numfile
    
class TestNoRHClient(unittest.TestCase):
    '''
    This class will have the methods to test the functions above that make use 
    of remote servers using mock objects. Should we make a class to insert
    the mock tests with the structure featured below?
    '''
    
    def setUp(self):
        '''
        This function will set up the attributes that will be tested by the 
        other functions on this class.
        '''
        print('setUp')
        # Creating an attribute of the NoRHClient class.
        self.LCClient = norh.NoRHClient()
        
    def tearDown(self):
        '''
        If necessary this function will make a clean slate for further testing.
        '''
        pass
    
    def test_get(self):
        '''
        Here the test function that gets the data for norh will be tested.
        '''
        print('test_get')
        
        # Patching the LCClient.search
        with patch('__main__.norh.NoRHClient.search') as mock_query:
            qr1 = mock_query(time='YYYYMMDD', instrument='')
        
        

if __name__ == '__main__':
    '''
    My test zone so I can execute the bits here.
    This will be removed before merging.
    
    Notes:
    @pytest.mark.remote_data marks tests that require data from the internet.
    
    Pytest remotedata from astropy:
    https://github.com/astropy/pytest-remotedata
    
    '''
    test_query_mock('2014-11-05: 13:00:00', 17)
    