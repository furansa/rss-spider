import pytest

import rss_spider


def test_do_log_with_empty_message_raises_error():
    """
    Test if raises exception on empty message
    """
    expected_output = "Argument 'message' cannot be empty"

    none_message = str()

    with pytest.raises(TypeError) as e1:
        assert rss_spider.do_log(none_message)

    assert expected_output in str(e1)

    empty_message = ""

    with pytest.raises(TypeError) as e2:
        assert rss_spider.do_log(empty_message)

    assert expected_output in str(e2)


def test_do_log_with_wrong_message_type():
    """
    Test if raises exception on non string message
    """
    expected_output = "Argument 'message' must be of type string"
    input_message = 123456

    with pytest.raises(TypeError) as t:
        assert rss_spider.do_log(input_message)

    assert expected_output in str(t)


@pytest.mark.skip("WIP")
def test_fetch_feeds_with_socket_timeout():
    """
    Test if raises exception on socket timeout
    """
    assert False
