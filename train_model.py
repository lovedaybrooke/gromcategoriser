from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

import sekrits
from training_data_redacted import *

app = ClarifaiApp(api_key=sekrits.clarifai_api_key)

all_images = []

for image_name in training_data.keys(): 
    image_url = "https://s3.eu-west-2.amazonaws.com/marketpicsttteeesssttt/{0}".format(image_name)
    concepts = [concept for concept in training_data[image_name] if concept in acceptable_concepts]
    not_concepts = [concept for concept in acceptable_concepts if concept not in training_data[image_name]]
    image = ClImage(url=image_url, concepts=concepts, not_concepts=not_concepts)
    all_images.append(image)

# API will only accept batches of 128 images
for pair in [[0, 127], [128, 256], [257, 384], [385, 512], [513, 640], [640,'']]:
    app.inputs.bulk_create_images(all_images[pair[0]:pair[1]])

model = app.models.create('witch_of_the_market', concepts=acceptable_concepts, concepts_mutually_exclusive=False)

def check_image(model, image_name):
    image_url = "https://s3.eu-west-2.amazonaws.com/marketpicsttteeesssttt/{0}".format(image_name)
    image = ClImage(url=image_url)
    response = model.predict([image])
    blargh = response["outputs"][0]["data"]["concepts"]
    print json.dumps(response, indent=2, sort_keys=True)
