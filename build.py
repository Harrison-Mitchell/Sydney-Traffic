import urllib, shutil, json, os
from urllib.request import urlopen, urlretrieve
from PIL import Image, ImageFile
# this allows damaged images to still be processed, most of the
# CCTV cameras use an odd format so this is necessary
ImageFile.LOAD_TRUNCATED_IMAGES = True
os.mkdir("images")
num = 0

# load the latest JSON data in memory
url = 'http://data.livetraffic.com/cameras/traffic-cam.json'
jData = json.loads(urlopen(url).read())

# find all CCTV image URLs
for p in jData["features"]:
	camURL = p["properties"]["href"]
	# save each image numerically
	urllib.request.urlretrieve(camURL, "images/" + str(num) + ".jpg")
	num += 1

# create a new image, 352 and 288 are fixed width/height sizes
# and there are currently only 136 cameras, with no new ones
# added within 4 years, thus a 12x12 grid is sufficient
im = Image.new("RGB", (12 * 352, 10 * 288))
for y in range(12):
	for x in range(12):
		# add the image to the grid until we run out of images
		try:
			new = Image.open("images/" + str(x + y * 12) + ".jpg")
			im.paste(new, (x * 352, y * 288))
		except:
			pass
		
shutil.rmtree("images")
im.save("out.jpg")