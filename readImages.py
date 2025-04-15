from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

for i in range(1, 12):
    # Read Image
    img = Image.open(f'test_images/test{i}.png')
    img = ImageOps.grayscale(img)

    np_img = np.array(img)
    np_img = ~np_img
    np_img[np_img > 0] = 1
    plt.set_cmap('binary')
    plt.imshow(np_img)

    # Save Image
    np.save(f'test_images/test{i}.npy', np_img)


