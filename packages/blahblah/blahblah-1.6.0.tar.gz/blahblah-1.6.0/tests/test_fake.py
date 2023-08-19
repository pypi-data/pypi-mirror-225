from baby_steps import then, when
from district42 import schema

from blahblah import fake


def test_fake():
    with when:
        res = fake(schema.int)

    with then:
        isinstance(res, int)
