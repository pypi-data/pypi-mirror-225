import urllib.parse

from conftest import TEST_API_KEY, EXPECTED_EVENT_URL, EXPECTED_OFFLINE_CONVERSION_URL


def parse_qs(url):
    """Return URL parameters as a dictionary of name/value pairs."""
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))

def test_track_custom_event_provides_proper_parameters(direqt, requests_mock):
    """SDK provides expected parameters for custom event endpoint.
    :param direqt.DireqtClient direqt: default Direqt test client
    """
    mock_response = {
        'messageId': 'xx',
        'eventName': 'xx',
        'eventData': { 'foo': 'bar' }
    }
    adapter = requests_mock.post(EXPECTED_EVENT_URL, json=mock_response)

    custom_event_data = {
        'thing_one': 'foo',
        'thing_two': 'bar'
    }
    result = direqt.track_custom_event('test-message-id', 'custom-event-name', custom_event_data)

    assert adapter.call_count == 1
    qs = parse_qs(adapter.last_request.url)
    assert qs['key'] == TEST_API_KEY

    request_body = adapter.last_request.json()
    assert request_body['messageId'] == 'test-message-id'
    assert request_body['eventName'] == 'custom-event-name'
    assert request_body['eventData']['thing_one'] == 'foo'
    assert request_body['eventData']['thing_two'] == 'bar'

    assert result == mock_response

def test_offline_conversion_provides_proper_parameters(direqt, requests_mock):
    """SDK provides expected parameters for custom event endpoint.
    :param direqt.DireqtClient direqt: default Direqt test client
    """
    adapter = requests_mock.post(EXPECTED_OFFLINE_CONVERSION_URL)

    custom_event_data = {
        'thing_one': 'foo',
        'thing_two': 'bar'
    }
    result = direqt.offline_conversion('test-message-id', custom_event_data)

    assert adapter.call_count == 1
    qs = parse_qs(adapter.last_request.url)
    assert qs['key'] == TEST_API_KEY

    request_body = adapter.last_request.json()
    assert request_body['messageId'] == 'test-message-id'
    assert request_body['eventName'] == 'Conversion'
    assert request_body['eventData']['thing_one'] == 'foo'
    assert request_body['eventData']['thing_two'] == 'bar'

    assert result == True