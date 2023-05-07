import unittest
from SiteSentry import *
import os

class TestMyModule(unittest.TestCase):

    def test_download_csv_from_google_sheets(self):
        # Replace with your test data


        service_account_json_path= "data/service_account.json"

        service_account_json_path = "data/service_account.json"
        spreadsheet_id = "1blbxEA0_jgBgc_UPxf65xcboSxF3WrNyrhcDvxl8Xys"
        worksheet_name = "Sheet1"
        filename =  "test.csv"

        # Call the function
        download_csv_from_google_sheets(service_account_json_path, spreadsheet_id, worksheet_name, filename)

        # Assert that the file was created
        self.assertTrue(os.path.isfile(filename))

    def test_check_certificate_expiry(self):
        # Replace with your test data
        list_file = "data/test_data.csv"
        warn_days = 30

        # Call the function
        check_certificate_expiry(list_file, warn_days)

        # Assert that the function does not raise any errors

    def test_diff_files(self):
        # Replace with your test data
        file1 = "test1.csv"
        file2 = "test2.csv"

        # Create test files
        with open(file1, 'w') as f:
            f.write("Test line 1\nTest line 2\n")

        with open(file2, 'w') as f:
            f.write("Test line 1\nTest line 3\n")

        # Call the function
        diff_log = diff_files(file1, file2)

        # Assert that the function returns the expected output
        expected_output = ['Difference found on line 2:',
                           f'{file1}: Test line 2',
                           f'{file2}: Test line 3']
        self.assertEqual(diff_log, expected_output)

        # Remove test files
        os.remove(file1)
        os.remove(file2)

if __name__ == '__main__':
    unittest.main()
