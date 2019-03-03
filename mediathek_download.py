#!/usr/bin/env python3

"""script to download videos from the mediathek of german public broadcasting,
   which are delivered in segments 
   use the network analysis of your browser to discover the source url
"""

import os.path
import sys
import urllib.request

if len(sys.argv) != 3:
    print('usage mediathek_download.py source_url destination_file')
    print('the source must contain a placeholder for the segment number (curly braces)')
    print('e.g. https://mediathek/segment{}_123_av.ts')
    exit(0)

source = sys.argv[1]
destination_filename = sys.argv[2]

if os.path.isfile(destination_filename):
    print('file {0} exists, aborting.'.format(destination_filename))
    exit(1)

destination = None
for i in range(1, 2000):
    try:
        nurl = source.format(i)
        videoreqest = urllib.request.urlopen(nurl)
        segmentdata = videoreqest.read()
        if destination is None:
            destination = open(destination_filename, 'wb')
        destination.write(segmentdata)
        print('.', end='')
        sys.stdout.flush()
    except urllib.error.HTTPError as he:
        print(str(he))
        exit(1)
destination.close()

print('done')
exit(0)
