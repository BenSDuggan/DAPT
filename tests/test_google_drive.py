"""
Test the Box class in `dapt.storage.google_drive`
"""

import pytest

from tests.base import Storage_test_base

@pytest.mark.test_login
class TestGoogleDrive(Storage_test_base):
    
    def preflight(self):
        """
        Testing items that should be ran before tests are ran.  This method returns a new
        class method for the test.

        Returns:
            The class instance which will be used for the unit test.
        """

        pass

    def postflight(self):
        """
        Clean up after tests are ran.
        """

        pass



