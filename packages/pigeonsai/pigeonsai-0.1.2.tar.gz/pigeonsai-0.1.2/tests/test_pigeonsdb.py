import unittest
from pigeonsai import PigeonsDB

class TestPigeonsDB(unittest.TestCase):

    def test_get_db_info(self):
        # Test the get_db_info method with valid input
        api_key = "psk-ed2eb1fd4ac64f0e8b61dfca2965cf55"
        db_name = "dbdone1054"
        s3_identifier, db_object = PigeonsDB.get_db_info(api_key, db_name)

        # Add assertions to check if the returned values are as expected
        self.assertIsNotNone(s3_identifier)
        self.assertIsNotNone(db_object)

    # Add more test functions for other methods and edge cases

if __name__ == "__main__":
    unittest.main()