import csv
import sys

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import psycopg2
import requests

import sekrits
import hand_categorised_data


def database_set_up():
    conn = psycopg2.connect(host="localhost", database="images_analysed",
    user=sekrits.psql_username, password=sekrits.psql_password)
    return conn

def create_queries(version, image_url, tag_list):
    queries = []
    image_name = image_url[58:]
    image_info = image_name.split('__')
    hash = image_info[1]
    date = image_info[0]
    username = image_info[2][:-4]
    for tag in tag_list:
        values = "'" + "', '".join([hash, image_url, username, date]) + "'"
        values += ", 0, '" + tag + "', 1" 
        query = "INSERT INTO image_analysis (hash, url, username, date, version, tag, strength) VALUES (" + values + ");"
        queries.append(query)
    return queries

def add_to_db(conn, queries):
    for query in queries:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

def add_image(version, image_url, tag_list):
    queries = create_queries(version, image_url, tag_list)
    conn = database_set_up()
    add_to_db(conn, queries)

def process_all_images(version):
    conn = database_set_up()
    print("database_set_up")
    
    total = 743
    i = 0
    
    for image, tags in hand_categorised_data.tag_data.iteritems():
        image_url = 'https://s3.eu-west-2.amazonaws.com/marketpicsttteeesssttt/' + image
        add_image(version, image_url, tags)
        i += 1
        sys.stdout.write("\rFinished row {0} of {1}".format(
            i, total))
        sys.stdout.flush()

process_all_images(0)
