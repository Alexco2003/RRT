from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt


img = Image.open('test_images/test.png')

fixed_size = (1800, 900)
img = img.resize(fixed_size)

img = ImageOps.grayscale(img)

np_img = np.array(img)


np_img = ~np_img
np_img[np_img > 0] = 1

plt.set_cmap('binary')
plt.imshow(np_img)
plt.show()

np.save('test_images/test.npy', np_img)