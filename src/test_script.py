from semantic_search import Search
from image import Image

img_object = Image()
img_object.upload('random.jpg', 'random_image')

print(img_object.download('random_image'))