from tinydb import TinyDB, Query
from datetime import datetime


filetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
db = TinyDB('/home/pi/Desktop'+ filetime +'.json')

def insertJson(i_json):
    db.insert(i_json)