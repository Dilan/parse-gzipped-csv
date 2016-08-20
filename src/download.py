# CLI that takes one parameter which is an URL to a gzipped CSV file stored on a remote server.
# Program should then output to standard out the following with new line separators
# - total count of all users
# - number of users with a device resolution of 640x960
# - total spend of all users in dollars
# - user_id of the first user who joined

# assumption 1: CSV might be huge => read by 1Kb chunks

import csv
import sys
import urllib2
import datetime
import zlib
import traceback

def isoparse(s):
    try:
        return datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]),
                        int(s[11:13]), int(s[14:16]), int(s[17:19]))
    except:
        return None

def is_int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Report():
    users_amount = 0
    resolution_640_960 = 0
    spend_amount = 0
    first_joined_user_id = None
    first_joined_user_date = None

def analyse_csv_row(row, headers, report):
    data = {}
    for idx, value in enumerate(row):
        data[headers[idx]] = str(value)

    if 'user_id' in data and data['user_id']:
        report.users_amount +=1

    if ('device_width' in data) and ('device_height' in data) \
            and data['device_width'].strip() == '640' \
            and data['device_height'].strip() == '960':
        report.resolution_640_960 += 1

    if ('spend' in data) and (is_int_number(data['spend'].strip())):
        report.spend_amount += int(data['spend'])

    if ('date_joined' in data) and (isoparse(data['date_joined'])):
        date_joined = isoparse(data['date_joined'])

        has_to_update = True
        if report.first_joined_user_date and report.first_joined_user_date < date_joined:
            has_to_update = False

        if has_to_update:
            report.first_joined_user_id = data['user_id']
            report.first_joined_user_date = date_joined

    return report

def read_url(url, report):
    response = urllib2.urlopen(urllib2.Request(url))

    # default
    headers = None
    unfinished_line = ''

    d = zlib.decompressobj(zlib.MAX_WBITS|32)
    while True:
        # read stream by 1Kb
        gz_data = response.read(1024)
        if not gz_data: break

        data = d.decompress(gz_data)
        # text -> array
        lines = data.splitlines(True)

        # merge completed lines to CSV rows
        rows = []
        for line in lines:
            if len(unfinished_line):
                line = unfinished_line + line
                unfinished_line = ''

            if line.endswith('\n'):
                line = line.strip()
                rows.append(line);
            else:
                unfinished_line = line

        for row in csv.reader(rows):
            # 1st row must be column names
            if headers is None:
                headers = row
                continue
            # skip empty rows
            if len(row) == 0:
                continue
            # ... the rest rows
            analyse_csv_row(row, headers, report)

    return report

def main(url):
    try:
        report = read_url(url,Report())

        print report.users_amount # - total count of all users
        print report.resolution_640_960 # - number of users with a device resolution of 640x960
        print report.spend_amount # - total spend of all users in dollars
        print report.first_joined_user_id # - user_id of the first user who joined

    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url

    except urllib2.URLError, e:
        print "URL Error:", e.reason, url

    except Exception as e:
        print "Unexpected Error:", e
        print traceback.format_exc()

# CLI
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Error: please provide URL as a first argument.'
        sys.exit()

    main(sys.argv[1])
