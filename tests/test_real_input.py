import numpy as np
import pytest
from matro import minimize


def test_complex_start_is_not_silently_projected_to_real_coordinates():
    calls = []
    with pytest.raises(ValueError, match='real vector'):
        minimize(lambda x: calls.append(x), np.array([1.+1.j, 2.+0.j]))
    assert not calls
