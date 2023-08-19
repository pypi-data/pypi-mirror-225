import json
import urllib.parse
import requests

from conftest import TEST_API_KEY, EXPECTED_FETCH_URL, TEST_MSISDN, EXPECTED_AGENT_MESSAGE_URL, \
    EXPECTED_FILE_MESSAGE_URL, TEST_MSISDN_MD5, TEST_SUBSCRIBER_ID


def parse_qs(url):
    """Return URL parameters as a dictionary of name/value pairs."""
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))


def create_mock_rbm_response(req):
    """(Eventually) create a response we would expect from RBM given a request."""
    return req


def test_fetch_provides_proper_default_parameters(direqt, requests_mock):
    """SDK provides expected default parameters fetch endpoint.
    :param direqt.DireqtClient direqt: default Direqt test client
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        body = parse_qs(request.body)

        assert body == {}
        assert qs['key'] == TEST_API_KEY
        assert qs['format'] == 'RBMV1.0'
        assert qs['adUnit'] == 'test-ad-unit'
        assert qs['count'] == '1'
        assert 'targeting' not in qs

        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={}, additional_matcher=verify_request)

    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt.ErrorCode.OTHER


def test_fetch_handles_empty_response(direqt, requests_mock):
    """handles empty fetch response.
    :param requests_mock.Mocker requests_mock
    :param direqt.DireqtClient direqt
    """
    requests_mock.post(EXPECTED_FETCH_URL, json={})

    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt.ErrorCode.OTHER


def test_fetch_simple_result(direqt, requests_mock):
    """handles a simple text response.

    Verify that when the Direqt server returns a simple text payload, that payload
    is sent along to RBM as expected.

    :param requests_mock.Mocker requests_mock
    :param direqt.DireqtClient direqt
    """
    rbm_message = {
        'contentMessage': {
            'text': 'Hello, world!'
        }
    }

    direqt_response = {
        'payload': json.dumps(rbm_message)
    }

    def verify_rbm_request(request):
        """:type request: requests.models.PreparedRequest"""
        assert request.body == json.dumps(rbm_message)
        return True

    requests_mock.post(EXPECTED_FETCH_URL, json=direqt_response)  # direqt/fetch
    requests_mock.post(EXPECTED_AGENT_MESSAGE_URL, json=create_mock_rbm_response(rbm_message),
                       additional_matcher=verify_rbm_request)

    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert result is True
    assert requests_mock.call_count == 2


def test_fetch_simple_result_fetch_only_set(direqt, requests_mock):
    """handles a simple text response.

    Verify that when the Direqt server returns a simple text payload, that payload
    is returned to caller when `fetch_only` flag is set.

    :param requests_mock.Mocker requests_mock
    :param direqt.DireqtClient direqt
    """
    rbm_message = {
        'contentMessage': {
            'text': 'Hello, world!'
        }
    }

    direqt_response = {
        'payload': json.dumps(rbm_message)
    }

    requests_mock.post(EXPECTED_FETCH_URL, json=direqt_response)  # direqt/fetch

    result = direqt.fetch('test-ad-unit', TEST_MSISDN, fetch_only=True)

    assert result is not None
    assert result['payload'] == json.dumps(rbm_message)
    assert requests_mock.call_count == 1    # only /fetch; no call to RBM


def test_fetch_does_not_send_if_test_set(direqt, requests_mock):
    """Honors the test flag from the server

    Verify that when the Direqt server returns 'isTest', no message
    is sent via RBM.

    :param requests_mock.Mocker requests_mock
    :param direqt.DireqtClient direqt
    """
    rbm_message = {
        'contentMessage': {
            'text': 'Hello, world!'
        }
    }

    direqt_response = {
        'payload': json.dumps(rbm_message),
        'isTest': True
    }

    def verify_rbm_request(request):
        """:type request: requests.models.PreparedRequest"""
        assert False    # should not have been called!

    requests_mock.post(EXPECTED_FETCH_URL, json=direqt_response)  # direqt/fetch
    requests_mock.post(EXPECTED_AGENT_MESSAGE_URL, json={},
                       additional_matcher=verify_rbm_request)

    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert result
    assert requests_mock.call_count == 1    # just the direqt fetch, not the RBM


def test_fetch_media_upload(direqt, requests_mock):
    """Handles a media upload.

    When the fetch response includes a media file, we should upload it.

    :param requests_mock.Mocker requests_mock
    :param direqt.DireqtClient direqt
    """

    file_url = 'http://www.example.com/somefile.jpg'
    thumbnail_url = 'http://www.example.com/somefile-tn.jpg'
    content_description = 'This is a description.'

    expected_rbm_message = {
        'fileUrl': file_url,
        'thumbnailUrl': thumbnail_url,
        'contentDescription': content_description
    }

    # N.B. Currently, 'payload' is a string, while 'media' is JSON...
    direqt_response = {
        'media': [
            {'file_url': file_url, 'thumbnail_url': thumbnail_url, 'content_description': content_description},
        ]
    }

    def verify_rbm_request(request):
        """:type request: requests.models.PreparedRequest"""
        assert request.body == json.dumps(expected_rbm_message).encode('utf-8')
        return True

    requests_mock.post(EXPECTED_FETCH_URL, json=direqt_response)  # direqt/fetch
    requests_mock.post(EXPECTED_FILE_MESSAGE_URL, json=create_mock_rbm_response(expected_rbm_message),
                       additional_matcher=verify_rbm_request)

    rbm_called = False
    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 2


def test_fetch_provides_proper_sms_parameters(direqt_sms, requests_mock):
    """SDK provides expected default parameters fetch endpoint.
    :param direqt.DireqtClient direqt: default Direqt test client
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        body = parse_qs(request.body)

        assert body == {}
        assert qs['key'] == TEST_API_KEY
        assert qs['format'] == 'SMS'
        assert qs['adUnit'] == 'test-ad-unit'
        assert qs['subscriber'] == TEST_MSISDN_MD5
        assert 'targeting' not in qs

        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={}, additional_matcher=verify_request)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt_sms.ErrorCode.NO_AD_RETURNED


def test_fetch_uses_supplied_subscriber_id(direqt_sms, requests_mock):
    """SDK provides expected default parameters fetch endpoint.
    :param direqt.DireqtClient direqt: default Direqt test client
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        assert qs['subscriber'] == TEST_SUBSCRIBER_ID
        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={}, additional_matcher=verify_request)

    result = direqt_sms.fetch('test-ad-unit', subscriber_id=TEST_SUBSCRIBER_ID)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt_sms.ErrorCode.NO_AD_RETURNED


def test_fetch_uses_supplied_subscriber_id_when_msisdn_provided(direqt_sms, requests_mock):
    """SDK provides expected default parameters fetch endpoint.
    :param direqt.DireqtClient direqt: default Direqt test client
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        assert qs['subscriber'] == TEST_SUBSCRIBER_ID
        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={}, additional_matcher=verify_request)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN, subscriber_id=TEST_SUBSCRIBER_ID)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt_sms.ErrorCode.NO_AD_RETURNED


def test_fetch_returns_proper_sms_response(direqt_sms, requests_mock):
    """fetch() returns proper response object for SMS.
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        body = parse_qs(request.body)

        assert body == {}
        assert qs['key'] == TEST_API_KEY
        assert qs['format'] == 'SMS'
        assert qs['adUnit'] == 'test-ad-unit'
        assert 'targeting' not in qs

        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={'payload': 'This is test payload', 'messageId': 'test-message-id'}, additional_matcher=verify_request)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not False
    assert result['payload'] == 'This is test payload'
    assert result['message_id'] == 'test-message-id'


def test_fetch_returns_proper_sms_response_with_custom_properties(direqt_sms, requests_mock):
    """fetch() returns proper response object for SMS.
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """
    response_json = {
        'payload': 'This is test payload',
        'messageId': 'test-message-id',
        'properties': {
            'foo': 'foo-value',
            'bar': 'bar-value',
            'fff': 42
        }
    }

    requests_mock.post(EXPECTED_FETCH_URL, json=response_json)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert 'properties' in result
    properties = result['properties']
    assert properties['foo'] == 'foo-value'
    assert properties['bar'] == 'bar-value'
    assert properties['fff'] == 42


def test_fetch_sets_is_test_flag_to_false_by_default(direqt_sms, requests_mock):
    """fetch() sets 'is_test' property to false by default
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """
    response_json = {
        'payload': 'This is test payload',
        'messageId': 'test-message-id',
        'properties': {
            'foo': 'foo-value',
            'bar': 'bar-value',
            'fff': 42
        }
    }

    requests_mock.post(EXPECTED_FETCH_URL, json=response_json)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert 'is_test' in result
    assert not result['is_test']


def test_fetch_sets_is_test_flag_to_false_for_false_value(direqt_sms, requests_mock):
    """fetch() sets 'is_test' property to false by default
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """
    response_json = {
        'payload': 'This is test payload',
        'messageId': 'test-message-id',
        'properties': {
            'foo': 'foo-value',
            'bar': 'bar-value',
            'fff': 42
        },
        'isTest': False
    }

    requests_mock.post(EXPECTED_FETCH_URL, json=response_json)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert 'is_test' in result
    assert not result['is_test']


def test_fetch_sets_is_test_flag_to_true(direqt_sms, requests_mock):
    """fetch() sets 'is_test' property to false by default
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """
    response_json = {
        'payload': 'This is test payload',
        'messageId': 'test-message-id',
        'properties': {
            'foo': 'foo-value',
            'bar': 'bar-value',
            'fff': 42
        },
        'isTest': True
    }

    requests_mock.post(EXPECTED_FETCH_URL, json=response_json)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert 'is_test' in result
    assert result['is_test']


def test_fetch_does_not_leak_msisdn(direqt, requests_mock):
    """Msisdn supplied to fetch should never appear in a server request.
    :param direqt.DireqtClient direqt: default Direqt test client
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        body = parse_qs(request.body)

        assert 'targeting' not in qs
        for k in body:
            assert TEST_MSISDN not in body[k]

        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={}, additional_matcher=verify_request)

    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt.ErrorCode.OTHER


def test_fetch_invokes_custom_url_shortener(direqt_sms, requests_mock):
    """fetch() invokes custom shortener for SMS url, and requests longUrl.
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        assert qs['longUrl'] == 'true'
        return True

    requests_mock.post(EXPECTED_FETCH_URL, json={
        'payload': 'This is test payload http://www.example.com/long/url/here',
        'messageId': 'test-message-id'}, additional_matcher=verify_request)

    def custom_url_shortener(url):
        return 'https://ex.co/short/url'

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN, url_shortener=custom_url_shortener)

    assert requests_mock.call_count == 1
    assert result is not False
    assert result['payload'] == 'This is test payload https://ex.co/short/url'
    assert result['message_id'] == 'test-message-id'


def test_fetch_with_url_shortener_but_no_returned_link(direqt_sms, requests_mock):
    """fetch() behaves as expected when custom shortener specified and no link in returned payload.
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """
    requests_mock.post(EXPECTED_FETCH_URL, json={
        'payload': 'This payload has no link',
        'messageId': 'test-message-id'})

    def custom_url_shortener(url):
        return 'https://ex.co/short/url'

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN, url_shortener=custom_url_shortener)

    assert requests_mock.call_count == 1
    assert result is not False
    assert result['payload'] == 'This payload has no link'


def test_fetch_handles_204_response(direqt_sms, requests_mock):
    """handles 204 response when no ads match targeting data.
    :param direqt.DireqtClient direqt_sms: default Direqt test client configured for SMS
    """
    requests_mock.post(EXPECTED_FETCH_URL, json={}, status_code=204)

    result = direqt_sms.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt_sms.ErrorCode.NO_AD_RETURNED


def test_fetch_returns_retriable_error(direqt, requests_mock):
    """handles returns retriable_error for HTTP 50x errors.
    :param direqt.DireqtClient direqt: default Direqt test client
    """

    requests_mock.post(EXPECTED_FETCH_URL, json={}, status_code=502)

    result = direqt.fetch('test-ad-unit', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt.ErrorCode.RETRIABLE_ERROR


def test_fetch_handles_error_response(direqt, requests_mock):
    """handles error response.
    :param direqt.DireqtClient direqt: default Direqt test client
    """
    direqt_response = {
        'reasonCode': 1004,
        'reason': 'UnknownAdUnit',
        'description': 'The ad unit specified was invalid or unknown'
    }

    requests_mock.post(EXPECTED_FETCH_URL,json=direqt_response, status_code=422)

    result = direqt.fetch('nonexistent_ad', TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not None
    assert 'payload' not in result
    assert result['error']['status'] == direqt.ErrorCode.UNKNOWN_ADUNIT


def test_fetch_handles_multiple_payload(direqt_raw, requests_mock):
    """handles a multiple raw text response.

    Verify that when the Direqt server returns more than 1 item (an array),
    that it is handled correctly.

    :param requests_mock.Mocker requests_mock
    :param direqt.DireqtClient direqt
    """
    payload = [
        {
            'response': {
                'payload': {
                    'title': '1st Card'
                },
                'messageId': 'test-msg-id-1',
            }
        },
        {
            'response': {
                'payload': {
                    'title': '2nd Card'
                },
                'messageId': 'test-msg-id-2',
            }
        }
    ]

    def verify_request(request):
        """:type request: requests.models.PreparedRequest"""
        qs = parse_qs(request.url)
        body = parse_qs(request.body)

        assert body == {}
        assert qs['key'] == TEST_API_KEY
        assert qs['format'] == 'RAW'
        assert qs['count'] == '2'
        assert qs['adUnit'] == 'test-ad-unit'
        assert 'targeting' not in qs

        return True

    requests_mock.post(
        EXPECTED_FETCH_URL,
        json={
            'payload': payload,
            'messageId': 'test-message-id'},
        additional_matcher=verify_request
    )

    result = direqt_raw.fetch('test-ad-unit', count=2, msisdn=TEST_MSISDN)

    assert requests_mock.call_count == 1
    assert result is not False
    assert result['payload'] == payload
    assert result['message_id'] == 'test-message-id'