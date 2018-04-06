from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

import sekrits
from training_data_redacted_v3 import *


app = ClarifaiApp(api_key=sekrits.clarifai_api_key)

all_images = []

for image_name in training_data_v5.keys(): 
    image_url = "https://s3.eu-west-2.amazonaws.com/marketpicsttteeesssttt/{0}".format(image_name)
    concepts = [concept for concept in training_data_v5[image_name] if concept in acceptable_concepts]
    not_concepts = [concept for concept in acceptable_concepts if concept not in training_data_v5[image_name]]
    image = ClImage(url=image_url, concepts=concepts, not_concepts=not_concepts)
    all_images.append(image)

app.inputs.bulk_create_images(all_images)

model = app.models.get('witch_of_the_market')
model.train()
