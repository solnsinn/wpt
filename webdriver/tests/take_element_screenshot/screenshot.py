import pytest

from tests.support.asserts import assert_error, assert_success
from tests.support.image import png_dimensions
from . import element_dimensions


def take_element_screenshot(session, element_id):
    return session.transport.send(
        "GET",
        "session/{session_id}/element/{element_id}/screenshot".format(
            session_id=session.session_id,
            element_id=element_id,
        )
    )


def test_no_top_browsing_context(session, closed_window):
    response = take_element_screenshot(session, "foo")
    assert_error(response, "no such window")


def test_no_browsing_context(session, closed_frame, inline):
    session.url = inline("<input>")
    element = session.find.css("input", all=False)

    response = take_element_screenshot(session, element.id)
    screenshot = assert_success(response)

    assert png_dimensions(screenshot) == element_dimensions(session, element)


@pytest.mark.parametrize("as_frame", [False, True], ids=["top_context", "child_context"])
def test_stale_element_reference(session, stale_element, as_frame):
    element = stale_element("<input>", "input", as_frame=as_frame)

    result = take_element_screenshot(session, element.id)
    assert_error(result, "stale element reference")


def test_format_and_dimensions(session, inline):
    session.url = inline("<input>")
    element = session.find.css("input", all=False)

    response = take_element_screenshot(session, element.id)
    screenshot = assert_success(response)

    assert png_dimensions(screenshot) == element_dimensions(session, element)
