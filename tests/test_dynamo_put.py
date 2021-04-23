import os
import sys
import unittest

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import boto_utils
import datetime
from constants import TABLE_NAME


# Note: May fail if boto_utils.migration() is not properly implemented
# Note: May take a long time as it deletes and recreates test table
class TestDynamoPut(unittest.TestCase):
    def setUp(self) -> None:
        self.dynamodb = boto_utils.dynamodb

        # Refresh test_table each test
        self.table = self.dynamodb.Table(TABLE_NAME)
        # boto_utils.migration(TABLE_NAME)
        # self.table.wait_until_exists()

        # dummy data
        self.original_url = "http://bored.com/"
        self.redirect_url = "1234567"
        self.expiration_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%s')
        self.user = "orangatan"

    def test_put_request(self):
        put_response = boto_utils.put(self.original_url, self.redirect_url, self.expiration_date, self.user, TABLE_NAME)
        print(put_response)
        self.assertEqual(put_response['ResponseMetadata']['HTTPStatusCode'], 200)
        check = self.table.get_item(Key={"redirect_url": self.redirect_url})

        self.assertEqual(check['Item']["original_url"], self.original_url)
        self.assertEqual(check['Item']["redirect_url"], self.redirect_url)
        self.assertEqual(check['Item']["expiration_date"], self.expiration_date)
        self.assertEqual(check['Item']["user"], self.user)

    def test_non_existing_table(self):
        put_response = boto_utils.put(self.original_url, self.redirect_url, self.expiration_date, self.user, "NOT_REAL_TABLE")
        self.assertEqual(put_response, False)

    def test_get_request(self):
        get_response = boto_utils.get("1234567")
        print(get_response)


if __name__ == "__main__":
    unittest.main()
