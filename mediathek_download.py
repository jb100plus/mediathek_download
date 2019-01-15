#!/usr/bin/env python

"""script to download videos from the mediathek of german public broadcasting,
   which are delivered in segments 
   use the network analysis of your browser to discover the source url
"""


import urllib.request
import sys
import os.path
import progressbar


if len(sys.argv) != 3:
    print('usage mediathek_download.py source_url destination_file')
    print('the source must contain a placeholder for the segment number (curly braces)')
    print('e.g. https://mediathek/segment{}_123_av.ts')
    exit(0)

source = sys.argv[1]
destination_filename = sys.argv[2]

if os.path.isfile(destination_filename):
    print('file {0} exists, aborting.'.format(destination_filename))
    exit(0)

bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength).start()
destination = open(destination_filename, 'wb')

for i in range(1, 2000):
    try:
        nurl = source.format(i)
        videoreqest = urllib.request.urlopen(nurl)
        segmentdata = videoreqest.read()
        destination.write(segmentdata)
        bar.update(i)
    except urllib.error.HTTPError as he:
        bar.finish(end=os.linesep + 'download done' + os.linesep)
        break

destination.close()

