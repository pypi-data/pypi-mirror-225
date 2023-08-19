import pathlib
import datetime
from . import logging
import os

def cache_file_exists(cache_file, cache_minutes):    
    if os.path.exists(cache_file):
        #https://stackoverflow.com/questions/237079/how-to-get-file-creation-and-modification-date-times
        m_dt = datetime.datetime.fromtimestamp(pathlib.Path(cache_file).stat().st_mtime, tz=datetime.timezone.utc) + datetime.timedelta(hours=9)
        logging.debug(m_dt)
        logging.debug(type(m_dt))
    
        #https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
        now_dt = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
        cache_minutes_dt = now_dt - datetime.timedelta(minutes=5)
        logging.debug(cache_minutes_dt)
        logging.debug(type(cache_minutes_dt))

        if m_dt > cache_minutes_dt: #캐시에서 가져오기
            return True
        else: #새로 가져오기
            return False
    return False 

if __name__ == "__main__":
    level = logging.DEBUG
    #level = logging.INFO
    #level = logging.ERROR
    logging.basic_config(level)
    
    print(cache_file_exists("cache.json", 10))
