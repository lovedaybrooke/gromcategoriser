import csv
import sys

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import psycopg2
import requests

import sekrits
import training_data_redacted

def database_set_up():
    conn = psycopg2.connect(host="localhost", database="images_analysed",
        user=sekrits.psql_username, password=sekrits.psql_password)
    return conn

def create_queries(version, image_url, tag_dict):
    queries = []
    image_name = image_url[58:]
    image_info = image_name.split('__')
    hash = image_info[1]
    date = image_info[0]
    username = image_info[2][:-4]
    for tag, strength in tag_dict:
        values = "'" + "', '".join([hash, image_url, username, date]) + "'"
        values += ", " + str(version) + ", '" + tag + "', " + str(round(strength, 4))
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

def Clarifai_set_up():
    app = ClarifaiApp(api_key=sekrits.clarifai_api_key)
    model = app.models.create('market_pic_categoriser',
        concepts=training_data_redacted.acceptable_concepts, 
        concepts_mutually_exclusive=False)
    return model

def categorise_image(model, image_url):
    image = ClImage(url=image_url)
    response = model.predict([image])
    concepts = response['outputs'][0]['data']['concepts']
    return {concept['name']: concept['value'] for concept in concepts}

def process_all_images(csv, version):
    conn = database_set_up()
    sys.stdout.write("Database set up")    

    model = Clarifai_set_up()
    sys.stdout.write("Clarifai set up")

    input_file = open('all_non_training_data.csv', 'r')
    csv_reader = csv.reader(input_file)
    error_file = open('errors.csv', 'w')
    csv_writer = csv.writer(error_file)

    total = sum(1 for line in open('all_non_training_data.csv'))
    i = 0
    sys.stdout.write("Starting to process {0} images".format(total))

    for line in csv_reader:
        image_url = 'https://s3.eu-west-2.amazonaws.com/marketpicsttteeesssttt/' + line[0]
        try:
            tags = categorise_image(model, image_url)
            add_image(version, image_url, tags)
            i += 1
            sys.stdout.write("\rFinished row {0} of {1}".format(
            i, total))
            sys.stdout.flush()

if __name__ == "__main__":
    if sys.argv[1][-3:] == 'csv':
        if sys.argv[2] == int:
            process_all_images(sys.argv[1], sys.argv[2])
