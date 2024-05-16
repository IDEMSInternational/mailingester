from mailingester.extractors import strip_footer


def test_remove_footer_from_content():
    content = "Main content\n\n--footer--\nFooter content"
    assert strip_footer("--footer--", content) == "Main content\n\n"


def test_remove_nothing_if_footer_not_found():
    content = "Main content\n\n--footer--\nFooter content"
    assert strip_footer("--not-found--", content) == content
    assert strip_footer(None, content) == content
