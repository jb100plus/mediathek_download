#!/usr/bin/env python3

"""script to download videos from the mediathek of german public broadcasting,
   which are delivered in segments 
   use the network analysis of your browser to discover the source url
"""

import os.path
import sys
import urllib.request
import re

if len(sys.argv) != 3:
    print('usage mediathek_download.py source_url destination_file')
    print('the source must contain a segment number')
    exit(1)

source = sys.argv[1]
p = re.compile('(segment\d+)',re.IGNORECASE)
source, count = p.subn('segment{}', source)
if count == 0:
    print('no segment item found')
    exit(1)
print(source)

destination_filename = sys.argv[2]
if os.path.isfile(destination_filename):
    print('file {0} exists, aborting.'.format(destination_filename))
    exit(1)

hasgotdata = False
destination = None
for i in range(1, 9999):
    try:
        nurl = source.format(i)
        videoreqest = urllib.request.urlopen(nurl)
        segmentdata = videoreqest.read()
        if destination is None:
            destination = open(destination_filename, 'wb')
        destination.write(segmentdata)
        hasgotdata = True
        print('.', end='')
        sys.stdout.flush()
    except urllib.error.HTTPError as he:
        if hasgotdata:
            destination.close()
            print('')
            print('done')
            break
        else:
            print(str(he))
            exit(1)

exit(0)
