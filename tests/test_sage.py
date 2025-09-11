from tests import oracle


def test_sage():
    assert oracle.Sage.ok()
    assert oracle.Sage.hello_world() == "Hello to Client"
