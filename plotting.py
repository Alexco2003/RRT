import numpy as np
import matplotlib.pyplot as plt

for i in range(1, 12):
    #Read Image
    grid = np.load(f'test_images/test{i}.npy')
    print(grid)
    print(grid.shape)
    plt.imshow(grid, cmap = "binary")
    plt.tight_layout()
    plt.show()