from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('test_images/test3.png')
img = ImageOps.grayscale(img)

np_img = np.array(img)
np_img = ~np_img  # invert B&W
np_img[np_img > 0] = 1
plt.set_cmap('binary')
plt.imshow(np_img)

# Save Image
np.save('test_images/test3.npy', np_img)

#Read Image
grid = np.load('test_images/test3.npy')
print(grid)
print(grid.shape)
plt.imshow(grid, cmap = "binary")
plt.tight_layout()
plt.show()
