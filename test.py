#
# Makes sure I'm reading the JSON data correctly
#
##############################################################

import json, os, socket

HOSTNAME = socket.gethostname()
if HOSTNAME == 'ewucal_server' or HOSTNAME == 'calligraphy.ewuthesis.com':
    IMAGE_DIR = "~/CADAL-scripts/fetchimages/workslist/grabbedBooks/"
else:
    IMAGE_DIR = "/home/dave/workspace/pycharm/fetch/grabbedBooks/"

PATH = "~/"
def readfromjson() -> None:
    jsonfile = open("c-works.json", mode="r", encoding='utf-8')
    readfile = json.load(jsonfile)
    jsonfile.close()
    for r in readfile:
#       print(r['name'])
#       print(r['dynesty'])
        for w in r['works']:
#           print(w['work_id'])
#           print(w['text_block'])
            imgprefix = str(w['pages']['book_id'])
            for p in w['pages']['pages_id']:
                fileimg = IMAGE_DIR + imgprefix + "-" + str(p)
                if not os.path.isfile(fileimg):
                    fileimg = fileimg.split('.')[0] + ".tif"
                    if not os.path.isfile(fileimg):
                        fileimg = None
                print(fileimg)



readfromjson()
