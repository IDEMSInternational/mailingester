from mailingester.extractors import Extractor


def test_can_extract_from_allowed_addresses():
    class MockEmail:
        def __init__(self, sender):
            self.sender = sender

    ex = Extractor(["sender_1@example.com", "sender_2@example.com"])

    assert ex.can_extract(MockEmail("sender_1@example.com"))
    assert ex.can_extract(MockEmail("Example sender <sender_2@example.com>"))
    assert not ex.can_extract(MockEmail("Not allowed <sender_3@example.com>"))
