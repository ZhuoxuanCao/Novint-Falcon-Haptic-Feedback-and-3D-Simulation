from utils import *


fig = figure("Exemple 3D")
fig3D = fig.gca(projection='3d')

x =[1,2,3,4,5,6,7,8,9,10]
y =[5,6,2,3,13,4,1,2,4,8]
z =[2,3,3,3,5,7,9,11,9,10]



fig3D.scatter(x, y, z, c='r', marker='o')

fig3D.set_xlabel('X Label')
fig3D.set_ylabel('Y Label')
fig3D.set_zlabel('Z Label')

show()
