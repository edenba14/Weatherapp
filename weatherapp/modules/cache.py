import json
import os
from datetime import datetime, timedelta


file_dir = os.path.dirname(os.path.realpath(__file__))
main_path = os.path.join(file_dir, "cache")


def write_cache(location, data):
    """
    this function receives a location and data and enters it to the cache folder
    :param location:
    :param data:
    :return:
    """
    location = location.lower()
    if not os.path.exists(main_path):
        os.mkdir(main_path)
    cache_file = os.path.join(main_path, f'{location}.json')
    with open(cache_file, 'w') as f:
        json.dump(data, f)


def read_cache(location):
    """
    this function receives a location and returns the data of this location if it exist in the cache folder
    :param location:
    :return: data from cache or None
    """
    location = location.lower()
    if not os.path.exists(main_path):
        return None
    cache_file = os.path.join(main_path, f'{location}.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
            return data
    else:
        return None


def is_cache_expired(cache_file):
    """
    this function receives a path of a file and checks if it expires
    :param cache_file:
    :return:True or False
    """
    if os.path.exists(cache_file):
        modification_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        timed = modification_time + timedelta(minutes=0)
        now = datetime.now() + timedelta(seconds=0)
        if now - timed >= timedelta(hours=2):
            return True
    return False


def remove_expired_cache():
    """
    this function runs over the files in cache folder and removes all files that are expired
    :return:
    """
    if not os.path.exists(main_path):
        return False
    for filename in os.listdir(main_path):
        cache_file = os.path.join(main_path, filename)
        if os.path.isfile(cache_file):
            if is_cache_expired(cache_file):
                os.remove(cache_file)
