import pytest

from executors.version_constraints import satisfies


def test_range_constraints():
    assert satisfies("2.0.15", ">=2.0,<3.0")
    assert not satisfies("3.0.0", ">=2.0,<3.0")


def test_exact_and_not_equal_constraints():
    assert satisfies("2.0.15", "==2.0.15")
    assert not satisfies("2.0.15", "!=2.0.15")


def test_unknown_version_does_not_satisfy_constraint():
    assert not satisfies("UNKNOWN", ">=2.0")


def test_invalid_constraint_is_rejected():
    with pytest.raises(ValueError):
        satisfies("2.0.15", "~=2.0")
