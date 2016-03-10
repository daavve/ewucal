#!/usr/bin/env python
#
# Got this from swampdragon/app_templates
#  Think this might run a redis server instan
#
######################################################################################

import os
import sys


from swampdragon.swampdragon_server import run_server

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ewucal.settings")

host_port = sys.argv[1] if len(sys.argv) > 1 else None

run_server(host_port=host_port)
