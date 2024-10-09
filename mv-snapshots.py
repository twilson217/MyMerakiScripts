import meraki
import os
import requests
import time
from datetime import datetime, timezone, timedelta
import shutil

API_KEY = os.getenv('MERAKI_DASHBOARD_API_KEY')
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

manual_loop = True
serial = 'Q4EE-CJ3B-Q7QN'
filename = 1

def snapshot():
    now = datetime.now(timezone.utc)
    delta = timedelta(seconds=60)
    shifted_time = now - delta
    formatted_time = shifted_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(formatted_time)
    snap = dashboard.camera.generateDeviceCameraSnapshot(serial, timestamp=formatted_time, fullframe="false")
    url = snap['url']
    print(url)
    time.sleep(2)
    local_file = open(f'./snapshots/{filename}.jpg', 'wb')
    resp = requests.get(snap['url'], stream=True)
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    local_file.close()

while manual_loop:
    snapshot()
    filename += 1
    time.sleep(30)
