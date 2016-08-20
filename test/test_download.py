import os
import urllib2
import unittest
from src.download import Report
from src.download import read_url
from src.download import analyse_csv_row

class SwrveCsvTest(unittest.TestCase):

    def test_analyse_local_gziped_csv(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        csvpath = os.path.join(dir_path, 'csv', 'test.csv.gz')

        report = read_url('file://' + csvpath, Report())

        self.assertEqual(report.users_amount, 100)
        self.assertEqual(report.resolution_640_960, 28)
        self.assertEqual(report.spend_amount, 51621)
        self.assertEqual(report.first_joined_user_id, 'a888a1c57cf6af2ffee687bfdd7dc4c5')

    def test_specified_row(self):

        headers = ['user_id','date_joined','spend','milliseconds_played','device_height','device_width']
        row = [
            'user00001',
            '2015-11-25T01:29:14+00:00',
            '820',
            '57698',
            '1136',
            '640'
        ]
        report = analyse_csv_row(row, headers, Report())

        self.assertEqual(report.users_amount, 1)
        self.assertEqual(report.resolution_640_960, 0)
        self.assertEqual(report.spend_amount, 820)
        self.assertEqual(report.first_joined_user_id, 'user00001')

    def test_specified_row_with_wrong_spent_format(self):
        report = analyse_csv_row(
            ['[850]'],
            ['spend'],
            Report()
        )
        self.assertEqual(report.users_amount, 0)
        self.assertEqual(report.spend_amount, 0)

    def test_specified_row_with_non_isoformat_for_date_joined_field(self):
        report = analyse_csv_row(
            ['17 August 2016 12:00:09'], # non iso format
            ['date_joined'],
            Report()
        )
        self.assertEqual(report.first_joined_user_id, None)

    def test_analyse_remote_gziped_csv(self):
        report = read_url(
            'https://s3.amazonaws.com/dept-dev-swrve/full_stack_programming_test/test_data.csv.gz',
            Report()
        )

        self.assertEqual(report.users_amount, 100)
        self.assertEqual(report.resolution_640_960, 28)
        self.assertEqual(report.spend_amount, 51621)
        self.assertEqual(report.first_joined_user_id, 'a888a1c57cf6af2ffee687bfdd7dc4c5')

    def test_for_403_error(self):
        try:
            read_url(
                'https://s3.amazonaws.com/dept-dev-swrve/full_stack_programming_test/NONEXIST_DATA.CSV.GZ',
                Report()
            )
        except urllib2.HTTPError, e:
            self.assertEqual(e.code, 403)

if __name__ == '__main__':
    unittest.main()