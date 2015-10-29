import os
import sys

from swampdragon.swampdragon_server import run_server

os.environ.setdefault('DJANGO_SETTINGS_MODULE','OnlineDating.settings')

print(sys.argv)

run_server(sys.argv[1])