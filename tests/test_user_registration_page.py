import pytest
from assertpy import assert_that
from utils.config_reader import ConfigReader
from utils.csv_reader import csv_reader
import uuid


def get_random_email():
    """Generates a random email address for testing purposes."""
    return f"tester{uuid.uuid4().hex[:8]}@gmail.com"

@pytest.mark.user_registration
@pytest.mark.usefixtures('setup_registration_page')
class TestUserRegistrationPage:

    @pytest.mark.parametrize(
        'first_name, last_name, telephone, password, subscribe', csv_reader(ConfigReader.get_config('test_data').get('user_registration')))
    def test_user_new_registration(self, first_name, last_name, telephone, password, subscribe):
        assert_that(self.registration_page.register_user(first_name, last_name, get_random_email(), telephone, password, subscribe)).is_true()