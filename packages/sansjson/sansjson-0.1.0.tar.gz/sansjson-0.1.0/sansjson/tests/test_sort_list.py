
import pytest
from sansjson.utils import Hasher

o = Hasher()


# TODO: fix objects
@pytest.mark.parametrize(
    'a, b',
    [
        # Homogenous
        (
            [3, 5, 4, 2],
            [2, 3, 4, 5]
        ),
        # Non-Homogenous
        (
            [None, 'a', 2, None],
            [None, None, 2, 'a']
        ),
        # Non-Homogenous Array 2
        (
            ['z', 1, 'a', 2, 'y', 3, 'c', 4],
            [1, 2, 3, 4, 'a', 'c', 'y', 'z']
        ),
        # Non-Homogenous 3
        (
            [None, 'z', 2, None, True, False, 1, 'a'],
            [None, None, False, True, 1, 2, 'a', 'z']
        )
    ]
)
def test_sortable_homogenous(a, b, compare):
    assert compare
