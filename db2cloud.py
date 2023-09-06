
# import os
# from dotenv import load_dotenv

# load_dotenv(dotenv_path='.env')
#
# connection = mariadb.connect(
#     host=os.getenv('DB_HOST'),
#     user=os.getenv('DB_USER'),
#     password=os.getenv('DB_PASSWORD'),
#     database=os.getenv('DB_NAME')
# )
import mariadb

from datetime import datetime, timedelta
from webdav3.client import Client

options = {
    "webdav_hostname": "https://cloud.kerk-loh.de/remote.php/dav/files/USERNAME/",
    "webdav_login": "USERNAME",
    "webdav_password": "###",
}
client = Client(options)

connection = mariadb.connect(
    host='localhost',
    user='###',
    password='###',
    database='###'
)
last_week = datetime.now() - timedelta(days=7)
yearweek = f"{last_week.year}{last_week.isocalendar().week}"
cursor = connection.cursor()

for electricity_meter in ("Solar", "Haus"):
    cursor.execute(f"SELECT reading, current_power , time FROM meter_readings "
                   f"WHERE electricity_meter_name ='{electricity_meter}' and YEARWEEK(time, 3) = YEARWEEK(DATE_SUB(NOW(), INTERVAL 7 DAY), 3) "
                   f"INTO OUTFILE '/tmp/{yearweek}{electricity_meter}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n';")
    client.upload_sync(remote_path=f"/Stromzaehler/{yearweek}{electricity_meter}.csv", local_path=f"/tmp/{yearweek}{electricity_meter}.csv")
