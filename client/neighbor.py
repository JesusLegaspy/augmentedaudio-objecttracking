import numpy as np
import scipy.spatial as spatial
import matplotlib.pyplot as plt
np.random.seed(2015)

from scipy import spatial
x, y = np.mgrid[0:5, 2:8]
tree = spatial.KDTree(list(zip(x.ravel(), y.ravel())))
tree.data

centers = [(1, 2), (3, 3), (4, 5)]
points = np.concatenate([pt+np.random.random((10, 2))*0.5 for pt in centers])
point_tree = spatial.cKDTree(points)

cmap = plt.get_cmap('copper')
colors = cmap(np.linspace(0, 1, len(centers)))
for center, group, color in zip(centers, point_tree.query_ball_point(centers, 0.5), colors):
   cluster = point_tree.data[group]
   x, y = cluster[:, 0], cluster[:, 1]
   plt.scatter(x, y, c=color, s=200)

plt.show()