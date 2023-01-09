import pytest
import numpy as np


@pytest.fixture()
def image():
    return (np.random.rand(4000, 4000, 3) * 255).astype(np.ubyte)
