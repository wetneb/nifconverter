import requests_mock
import pytest
import requests
from nifconverter.utils import retry_request

def test_retry_request_error():
    with requests_mock.mock() as mocker:
        mocker.get('http://somehost.sometld/', status_code=500)
        with pytest.raises(requests.RequestException):
            retry_request('http://somehost.sometld/', delay=0)
            
def test_retry_request_successful():
    with requests_mock.mock() as mocker:
        mocker.get('http://somehost.sometld/', text='hello')
        req = retry_request('http://somehost.sometld/', delay=0)
        assert req.text == 'hello'
            