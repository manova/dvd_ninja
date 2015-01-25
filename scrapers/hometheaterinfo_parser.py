from datetime import datetime
from pymongo import MongoClient
import csv


def extract_dvds():
    movies = MongoClient().dvds.movies
    file_name = 'dvd_csv.txt'
    keys = ['title', 'studio', 'released', 'status', 'sound', 'versions', 'price', 'rating', 'year', 'genre', 'aspect', 'upc', 'dvd_release_date', 'id', 'timestamp', 'updated']
    date_index = keys.index('dvd_release_date')
    with open(file_name, 'rb') as input_file:
        dvd_reader = csv.reader(input_file, delimiter='|')
        next(dvd_reader, None)
        for row in dvd_reader:
            row = [x.decode('iso-8859-1').encode('utf8') for x in row]
            try:
                row[date_index] = datetime.strptime(row[date_index].split(' ')[0], "%Y-%m-%d")
            except:
                continue
            entry = dict(zip(keys, row))
            movies.insert(entry)

extract_dvds()
