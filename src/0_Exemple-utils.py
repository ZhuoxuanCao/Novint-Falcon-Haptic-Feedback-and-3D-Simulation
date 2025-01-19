from utils import *

a = [1,2,3,4]
a2 = a[::-1] # a dans le sens inverse
b = [5,4,3,2]
c = ['a','b','c','d']

############ LES VECTEURS 3D ################################""
V1 = Vecteur3d(1,0,0)
V2 = Vecteur3d(0,1,0)

V3 = V1 * V2 # V1 vectoriel V2
V5 = V1 ** V2 # V1 scalaire V2

V4 = V3+V1-V2 # Addition / Soustraction

print("V1*V2 = ",V3)
print("V1**V2 = ",V5)

print("V1-V2+V3=V4 = ",V4)

print ("la norme de V4 = ",V4.mod())

V4.normed() # on modifie V4 pour avoir son module = 1
print("V4 normalisé = ",V4)
print ("la norme de V4 après normalisation = ",V4.mod())

print("5 * V4 = ",5*V4) # multiplication scalaire

print ("V3 (X Y Z) = ", V3.x, V3.y, V3.z) # les composants d'un vecteur


############ TRACER DES COURBES ########################

# a vs indice en rouge, b vs indice en vert
figure("a(i) en rouge, b(i) en vert")
plot(a,'r',b,'g',marker="x")

# a vs b en bleu
figure("b(a) en bleu")
plot(a,b,'b')

# plot 3D


fig = figure("3D")
fig3D = fig.gca(projection='3d')
fig3D.scatter(a,a2,b,color='green',marker="o") 
fig3D.set_xlabel('a')
fig3D.set_ylabel('a2')
fig3D.set_zlabel('b')
#affiche
show()

####### SAUVEGARDE DES DONNÉES DANS UN FICHIER #################

#sauvegarde les listes dans un fichier "test.txt"
save('test.txt',a,b,c)

# POUR TRACER LE FICHIER DANS UN TERMINAL:
# gnuplot -persist -e "plot 'test.txt' using 1:2 with lines title 'X(t)' "
