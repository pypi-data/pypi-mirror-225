import numpy as np
import datetime
import time
from geopy.geocoders import Nominatim    # type: ignore[import]
from geopy.exc import GeocoderUnavailable    # type: ignore[import]
from orion import optional_packages
import ssl
import logging
from urllib3 import connectionpool as cp

logger = logging.getLogger('orion_logger')


def derivative(x, t, **kwargs):
    dt = np.diff(t)
    dt = np.append(dt, dt[-1:], axis=0)
    return np.gradient(x, t, **kwargs)


def parse_usgs_event_page(search_days, event_id):
    if 'csep' not in optional_packages:
        logger.warning('The optional csep package is required to parse usgs event ID/URL data')
        return

    if not event_id:
        logger.warning('USGS event request requires either a url or id as input')
        return

    if '/' in event_id:
        expected_header = 'https://earthquake.usgs.gov/earthquakes'
        if event_id.startswith(expected_header):
            event_id = event_id.split('/')[5]
        else:
            logger.error(f'url should start with: {expected_header}')
            return

    ta = time.time() - 60 * 60 * 24 * search_days
    tb = time.time() + 60 * 60 * 24 * 2
    from csep.utils import comcat    # type: ignore[import]
    res = comcat.search(starttime=datetime.date.fromtimestamp(ta),
                        endtime=datetime.date.fromtimestamp(tb),
                        productcode=event_id,
                        verbose=True)

    if res:
        event = res[0]
        return event.time.timestamp(), event.latitude, event.longitude, event.depth, event.magnitude
    else:
        logger.warning('Target event not found!')


def parse_zip_code(location, country='United States of America'):
    if len(location) != 5:
        return

    cp.log.setLevel(logging.ERROR)
    zip_code = int(location)
    res = ''
    try:
        geolocator = Nominatim(user_agent="orion")
        res = geolocator.geocode({'postalcode': zip_code, 'country': country})
    except GeocoderUnavailable as e:
        if 'self signed certificate in certificate chain' in str(e):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                geolocator = Nominatim(user_agent="orion", ssl_context=ctx)
                res = geolocator.geocode({'postalcode': zip_code, 'country': country})
            except Exception as e:
                print(e)
                return 0.0, 0.0, ''
    except Exception as e:
        print(e)
        return 0.0, 0.0, ''

    if res:
        return res.latitude, res.longitude, res.address
    else:
        logger.error('Failed to parse the zip code')


def estimate_address(location):
    res = ''
    try:
        geolocator = Nominatim(user_agent="orion")
        res = geolocator.reverse(location)
    except GeocoderUnavailable as e:
        if 'self signed certificate in certificate chain' in str(e):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                geolocator = Nominatim(user_agent="orion", ssl_context=ctx)
                res = geolocator.reverse(location)
            except Exception as e:
                print(e)
                return ''
    except Exception as e:
        print(e)
        return ''

    if res:
        return res.address
    else:
        print('Failed to parse the location string')


def parse_location_str(location, country='United States of America'):
    tmp = location.split(',')
    if (len(tmp) == 1):
        if ('.' not in location):
            return parse_zip_code(location, country=country)
    else:
        lat = float(tmp[0])
        lon = float(tmp[1])
        address = estimate_address(location)
        return lat, lon, address
