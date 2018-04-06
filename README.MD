1. hand categorise some images, and put this data into training_data_redacted.py in the format shown
2. create the model and do some initial training ```python train_model.py```
3. you can now ask the model to categorise new images using the check_image() function
4. make a database, and a table with the following columns: hash (str), url (str), username (str), date (str), version (int), tag (str), strength (float)
5. put all the urls of images that weren't in the training data (ie, the ones you want to categorise) in a csv
6. choose a version number, eg 2
7. Run this to categorise all images in the csv and put them in the DB ```python database_putter.py 'non_training_images.csv' 2```