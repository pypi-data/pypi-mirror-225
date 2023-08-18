"""Test fixtures shared by all tests."""

import sys
from pathlib import Path
import pytest
from faker import Faker
import locale
from finesse.env import warn

# Add the test root directory to the path so test scripts can import the testutil
# package directly.
sys.path.append(str(Path(__file__).parent))


# Register test utilities package assertion error rewriting.
pytest.register_assert_rewrite(
    "testutils.cli", "testutils.diff", "testutils.fuzzing", "testutils.text"
)


# Set up a repeatable Faker seed.
FAKER_SEED = 314159
Faker.seed(FAKER_SEED)


def pytest_addoption(parser):
    import hypothesis

    # Add an option to change the Hypothesis max_examples setting via the `pytest` CLI.
    parser.addoption(
        "--hypothesis-max-examples",
        action="store",
        default=None,
        help="set the Hypothesis max_examples setting",
    )
    # Add an option to change the Hypothesis suppress_health_check setting via the `pytest` CLI.
    parser.addoption(
        "--hypothesis-suppress-health-check",
        action="store",
        # Work around failing fuzzing healthchecks:
        # "It looks like your strategy is filtering out a lot of data."
        # TODO: figure out why it is producing too much and then reset to None here.
        default=(hypothesis.HealthCheck.filter_too_much,),
        # default=None,
        help="set the Hypothesis suppress_health_check setting as list of int",
    )


def pytest_configure(config):
    import hypothesis

    # Set Hypothesis max_examples and suppress_health_check  using what, if
    # anything, was specified in the call to the `pytest` CLI.
    hypothesis_max_examples = config.getoption("--hypothesis-max-examples")
    hypothesis_suppress_health_check = config.getoption(
        "--hypothesis-suppress-health-check"
    )

    if hypothesis_max_examples is not None:
        max_examples = int(hypothesis_max_examples)
    else:
        max_examples = hypothesis.settings.default.max_examples

    if hypothesis_suppress_health_check is not None:
        # cmdline arg is string, default could be directly list of HealthCheck
        if isinstance(hypothesis_suppress_health_check, str):
            suppress_health_check = (
                hypothesis.HealthCheck(int(i))
                for i in hypothesis_suppress_health_check.split(",")
            )
        else:
            suppress_health_check = hypothesis_suppress_health_check
    else:
        suppress_health_check = hypothesis.settings.default.suppress_health_check

    hypothesis.settings.register_profile(
        "hypothesis-overridden",
        max_examples=max_examples,
        suppress_health_check=suppress_health_check,
    )
    hypothesis.settings.load_profile("hypothesis-overridden")

    # store the numeric locale for reversion if a test unexpectedly changes it
    pytest.expected_locale = locale.getlocale(locale.LC_NUMERIC)


def pytest_runtest_teardown(item, nextitem):
    # check if the numeric locale has changed
    curr_locale = locale.getlocale(locale.LC_NUMERIC)

    if curr_locale != pytest.expected_locale:
        warn(
            f"locale unexpectedly changed from {pytest.expected_locale} to {curr_locale}",
            RuntimeWarning,
        )

        # numeric locale has changed, revert it back
        locale.setlocale(locale.LC_NUMERIC, pytest.expected_locale)


@pytest.fixture(autouse=True)
def test_setup_and_teardown():
    # Set up global state before, and clean up after, each test.
    from finesse.config import autoconfigure
    from finesse.datastore import invalidate

    # Reset to default configuration.
    autoconfigure()

    # Run the test.
    yield

    # Delete the global cache.
    invalidate()
