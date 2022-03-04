#!/usr/bin/env python3

import csv
import os
import re
import tempfile
from argparse import ArgumentParser
from geocodio import GeocodioClient
from lib import Lib
from pprint import pprint

speed_regex = r'([0-9]{1,3})(?:\.([0-9]{1,2}))?([kmg])?(?:/?([0-9]{1,3})(?:\.([0-9]{1,2}))?([kmg])?)?'
default_columns = ['street', 'city', 'state', 'zip', 'ds', 'dsu', 'us', 'usu', 'aux']
required_columns = ['street', 'city', 'state', 'zip']

parser = ArgumentParser()

# General Arguments

parser.add_argument('-m', '--mode', required=True, type=str, help='Operating mode, either bd (broadband deployment)'
                                                                  + ' or bs (broadband subscription)')
parser.add_argument('-s', '--source', required=True, type=str, help='CSV input file to mutate data from')
parser.add_argument('-t', '--target', required=True, type=str, help='CSV output file to save mutated data to')
parser.add_argument('-D', '--delimiter', default=',', type=str, help='The delimiter to use for reading source CSV '
                                                                     + 'files. Defaults to the comma character.')
parser.add_argument('-q', '--quote', default='"', type=str, help='The quoting character to use when reading source '
                                                                 + 'CSV files. Defaults to the double quote character.')

# Broadband Deployment Mode Arguments

parser.add_argument('-c', '--consumer', required=False, type=str, help='If consumer broadband service is available '
                                                                       + 'then yes, no otherwise.')
parser.add_argument('-b', '--business', required=False, type=str, help='If business / government broadband service '
                                                                       + 'is available then yes, no otherwise.')
parser.add_argument('-d', '--downstream', required=False, type=str, help='Maximum consumer broadband downstream '
                                                                         + 'speed available in all census blocks '
                                                                         + '(Mbps)')
parser.add_argument('-u', '--upstream', required=False, type=str, help='Maximum consumer broadband upstream speed '
                                                                       + 'available in all census blocks (Mbps)')

# Broadband Subscription Mode Arguments

parser.add_argument('-k', '--apikey', default=None, type=str, help='Your Geocod.io API key')
parser.add_argument('-o', '--order', default=','.join(default_columns), type=str, help='The order of data '
                                                                                       + 'columns in the source'
                                                                                       + ' CSV file')
parser.add_argument('-S', '--skip', default=None, type=str, help='The number of rows to skip at the beginning of the '
                                                                 + 'source file')
parser.add_argument('-w', '--warn', default='no', type=str, help='Give a warning for rows missing required values')
parser.add_argument('-a', '--aux', default='no', type=str, help='Use auxiliary column for extracting plan speeds '
                                                                + 'instead of ds and us columns')
parser.add_argument('-r', '--regex', default=speed_regex, type=str, help='The regular expression to use for extracting'
                                                                         + 'the six segments of data from a blob of '
                                                                         + 'text.')

args = parser.parse_args()

if args.warn.lower() in ('yes', 'y', '1'):
    args.warn = True
elif args.warn.lower() in ('no', 'n', '0'):
    args.warn = False

if args.mode == 'bs' and ('apikey' not in args or args.apikey is None):
    Lib.api_key_warning()
    exit(0)

if args.mode == 'bd':

    if args.consumer is not None:

        consumer_service = True if str(args.consumer).lower() in ('yes', 'y', '1') else False
    else:
        consumer_service = Lib.bd_consumer_service()

    if args.business is not None:
        business_service = True if str(args.business).lower() in ('yes', 'y', '1') else False
    else:
        business_service = Lib.bd_business_service()

    if args.downstream is not None and len(str(args.downstream).strip()):
        downstream_bandwidth = float(args.downstream)
        if downstream_bandwidth < 1:
            downstream_bandwidth = Lib.bd_advertised_downstream('You must provide a downstream bandwidth of at least 1 '
                                                                + 'Mbps.')
    else:
        downstream_bandwidth = Lib.bd_advertised_downstream()

    if args.upstream is not None and len(str(args.upstream).strip()):
        upstream_bandwidth = float(args.upstream)
        if upstream_bandwidth < 1:
            upstream_bandwidth = Lib.bd_advertised_upstream('You must provide a downstream bandwidth of at least 1 '
                                                            + 'Mbps.')
    else:
        upstream_bandwidth = Lib.bd_advertised_upstream()

    rows = []

    with open(args.source, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=args.delimiter, quotechar=args.quote)
        for row in reader:
            row[0] = row[0].strip()
            row[1] = row[1].strip()
            row[2] = row[2].strip()
            row.append(int(consumer_service))
            row.append(str(int(downstream_bandwidth)))
            row.append(str(int(upstream_bandwidth)))
            row.append(int(business_service))
            rows.append(row)

    file = tempfile.mkstemp('.csv', 'as-fcc477-submission-tool-')
    target_path = os.path.realpath(args.target)
    tmp_path = file[1]

    Lib.bd_status_msg('Saving data to temporary file: ' + tmp_path)

    with open(tmp_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerows(rows)

    Lib.bd_status_msg('Moving temporary file to: ' + target_path)

    os.rename(tmp_path, target_path)

    Lib.bd_status_msg('All finished!', footer=True)

if args.mode == 'bs':
    Lib.bs_header()

    rows = []
    georows = {}

    Lib.bs_status_msg('Loading CSV data from source file...', True)

    with open(args.source, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=args.delimiter, quotechar=args.quote)
        rid = 1
        line_number = -1
        for line in reader:
            line_number += 1

            # Apply the "-s" or "--skip" argument to skip the given number of rows from the beginning of the file
            if args.skip is not None:
                skip = int(args.skip)
                if skip > 0 and (line_number + 1) <= skip:
                    continue

            row = {}

            c = 0
            missing = False
            for col in args.order.split(','):
                if col is not None and len(str(col).strip()) and col != 'none':
                    if not len(line[c].strip()):
                        missing = True
                    else:
                        row[col] = line[c]
                c += 1

            if missing and args.warn:
                Lib.bs_status_msg('One or more required column values are missing from line number '
                                  + str(line_number + 1), buffer=False)
            else:
                if args.aux and 'aux' in row:
                    # Extract the customer's plan speeds from the provided aux column
                    speeds = re.search(args.regex, row['aux'], re.IGNORECASE)

                    # Extract the downstream and upstream information from the value of the aux column
                    if speeds is not None:
                        dl = 0
                        ul = 0

                        if speeds.group(1) is not None:
                            dl += float(speeds.group(1))

                        if speeds.group(2) is not None:
                            dl += float(speeds.group(2)) / 10

                        if speeds.group(4) is not None:
                            ul += float(speeds.group(4))

                        if speeds.group(5) is not None:
                            ul += float(speeds.group(5)) / 10

                        if dl == 0:
                            dl = float(0.001)

                        if ul == 0:
                            ul = float(0.001)

                        row['ds'] = dl
                        row['dsu'] = str(speeds.group(3)).lower()
                        row['us'] = ul
                        row['usu'] = str(speeds.group(6)).lower()

                        if row['dsu'] not in ('k', 'm', 'g'):
                            row['dsu'] = 'm'

                        if row['usu'] not in ('k', 'm', 'g'):
                            row['usu'] = 'm'

                    else:
                        if args.warn:
                            Lib.bs_status_msg('Could not identify plan speeds for row number ' + str(line_number + 1)
                                              + '.', buffer=False)

                # Cache the row to a list
                rows.append(row)

                # Create a specifically formed record for the Geocod.io API if it has proper plan speeds
                if 'ds' in row and row['ds'] > 0 and 'us' in row and row['us'] > 0:
                    georows[str(rid)] = {
                        "street": row['street'],
                        "city": row['city'],
                        "state": row['state'],
                        "postal_code": row['zip'],
                        "country": "USA"
                    }
                    rid += 1
                elif args.warn:
                    Lib.bs_status_msg('Plan information is missing for line number ' + str(line_number + 1),
                                      buffer=False)

    if len(georows) > 10000:
        Lib.bs_status_msg('You are trying to process more than 10,000 records at once which is the current limit of the'
                          + ' Geocod.io API for batch requests.', footer=True)
    elif len(georows):
        api = GeocodioClient(args.apikey)
        counts = {}
        rid = 0

        Lib.bs_status_msg('Calling Geocod.io API for batch processing...')

        api_rows = api.batch_geocode(georows, fields=['census2020'])

        for rid, result in api_rows.items():
            rid = int(rid) - 1

            if len(result['results']):
                row = rows[rid]

                if 'fields' not in result['results'][0]:
                    if args.warn:
                        Lib.bs_status_msg('No matching location found for address of record number ' + (rid + 1),
                                          buffer=False)
                else:
                    census = result['results'][0]['fields']['census']['2020']
                    tract_code = census['county_fips'] + census['tract_code']
                    plan_id = Lib.bs_create_plan_id(row)

                    if tract_code not in counts:
                        counts[tract_code] = {}

                    if plan_id not in counts[tract_code]:
                        counts[tract_code][plan_id] = {
                            "subscribers": 0,
                            "dl_rate": row['ds'],
                            "dl_unit": row['dsu'],
                            "ul_rate": row['us'],
                            "ul_unit": row['usu'],
                        }

                    counts[tract_code][plan_id]['subscribers'] += 1

        csv_lines = 0
        file = tempfile.mkstemp('.csv', 'as-fcc477-submission-tool-')
        target_path = os.path.realpath(args.target)
        tmp_path = file[1]

        Lib.bs_status_msg('Saving data to temporary file: ' + tmp_path)

        with open(tmp_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')

            for tract_code, plans in counts.items():
                for plan_id, plan in plans.items():
                    subscribers = plan['subscribers']
                    if subscribers == 0:
                        continue
                    subscribers = str(subscribers)

                    if plan['dl_unit'] == 'k':
                        ds_mtp = 0.001
                    elif plan['dl_unit'] == 'm':
                        ds_mtp = 1
                    elif plan['dl_unit'] == 'g':
                        ds_mtp = 1000

                    if plan['ul_unit'] == 'k':
                        us_mtp = 0.001
                    elif plan['ul_unit'] == 'm':
                        us_mtp = 1
                    elif plan['ul_unit'] == 'g':
                        us_mtp = 1000

                    ds_rate = str(round(plan['dl_rate'] * ds_mtp, 3))
                    us_rate = str(round(plan['ul_rate'] * us_mtp, 3))

                    writer.writerow([tract_code, '70', ds_rate, us_rate, subscribers, subscribers])
                    csv_lines += 1

        if csv_lines:
            Lib.bs_status_msg('Moving temporary file to: ' + target_path)
            os.rename(tmp_path, target_path)
            Lib.bs_status_msg('All finished!', footer=True)
        else:
            Lib.bs_status_msg('There were no resulting rows to be written to the final CSV file!', footer=True)
    else:
        Lib.bs_status_msg('There were no extracted rows to be geocoded from the source CSV file!', footer=True)
