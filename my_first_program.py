# On peut importer des modules dans notre script de Python avec:
# import nom_de_module
# Ensuite, on peut aussi changer le nom de ce module quand ce nom est trop long
import numpy as np
# Avec la ligne au dessus, chaque fois qu'on veut utiliser numpy, on doit écrire seulement "np"
import matplotlib.pyplot as plt

############################## Étape 1 ##############################

# Consigne: Créer une fonction qui reçoit 2 nombres, et elle donne le
# résultat de la somme des deux chiffres.
def main(number_1, number_2):
    return number_1 + number_2

############################## Étape 2 ##############################

# Consigne: Créer une fonction qui demande à l'utilisateur de rentrer un chiffre.
# cette fonction recoit un texte, elle l'affiche, et elle vous
# donne le chiffre que l'utilisateur a rentré
def obtenir_nombre(texte_a_afficher):
    # On peut ajouter des commentaires aux fonctions. Ce type de commentaires
    # commence et termine avec " ''' " (trois guillemets simples)
    '''
    This function shows the string stored in z, and it
    asks the user to enter a number. The result is
    returned at the end of this function.

    Args:
        texte_a_afficher: Text to be shown to the user

    Returns:
            The entered number
    '''
    # This line asks the user to enter a number
    b = input(texte_a_afficher)
    return b

# On utilise la fonction "obtenir_nombre"
valeur = obtenir_nombre("Donnez moi un nombre: ")
print("La valeur rentree est: {}".format(valeur))

############################## Fin étape 2 ##############################

############################## Étape 3 ##############################
# Toutes les fois qu'on veut, on peut créer des fonctions qui ne font rien, mais
#  les valeurs d'entrée et de sortie sont correctes. Par exemple, on ne sait
# pas comment filtrer une image, mais on sait que pour filtrer une image, on a besoin
# de l'image et du kernel. De plus, ce type de fonction devrait nous donner l'image
# filtrée. Donc, on peut créer une fonction comme cela:

def filtrer_image(img, kernel):
    return img

# Et, nous la laissons comme ça jusqu'à ce qu'on trouve le moyen de filtrer une image.
############################## Fin étape 3 ##############################


############################## Étape 4 ##############################
# Consigne: Ouvrir une image
filepath = "endroit dans notre disque de l'image qu'on veut utiliser"
img = cv2.imread(filepath)

# Si OpenCV ne peut pas ouvrir l'image car il ne la trouve pas, il va poser dans
# la variable "img" le type de variable "rien", qui est "None". Donc, on verifie
# si c'est le cas. Si l'image est vide, on ne fait rien.
if not img is None:
    print("There was an error opening this image")
    exit(-1)

# On regarde la taille de l'image avec la propiété "shape"
print("La taille de l'image est.... {}".format(img.shape))
# On regarde le contenu du pixel (0,0)
pixel = img[0,0]
# Si l'image est en couleur, la prochaine ligne va stocker la valeur de la
# quantité de bleu dans le pixel (0,0). Si l'image est de niveau de gris, cette ligne
# va faire un échec, et le programme va terminer.
bleu = pixel[0]
# Si on a reussi à lire le pixel, on montre cette valeur.
print("La valeur du pixel (0,0) est: {}".format(pixel))

############################## Fin étape 4 ##############################

############################## Étape 5 ##############################
# Consigne: Ouvrir une image, et montrer les trois canaux.
filepath = "endroit dans notre disque de l'image qu'on veut utiliser"
img = cv2.imread(filepath)

# Même code qu'avant
if not img is None:
    print("There was an error opening this image")
    exit(-1)

# OpenCV ouvre l'image dans le système BVR, et pas dans le système RVB, donc
# le canal img[:,:,2] correspond à l'image de rouge seulement.

winname = 'Canal de rouge'
cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
cv2.imshow(winname, img[:,:,2])
cv2.waitKey()
cv2.destroyAllWindows()

# Consigne: Faire la même chose pour les deux autres canaux.
# Question: L'image montrée comme ça est au niveau de gris. Pourquoi ?

############################## Fin étape 5 ##############################


############################## Étape 6 ##############################
# Consigne: Ouvrir une image, et montrer les trois canaux, avec la teinte qui
# correspond à chaque canal: Par exemple, l'image de rouge doit être rouge, et pas
# en niveau de gris.
filepath = "endroit dans notre disque de l'image qu'on veut utiliser"
img = cv2.imread(filepath)

# Même code qu'avant
if not img is None:
    print("There was an error opening this image")
    exit(-1)

# OpenCV ouvre l'image dans le système BVR, et pas dans le système RVB, donc
# le canal img[:,:,2] correspond à l'image de rouge seulement.
img_rouge = np.zeros(img.shape, dtype=np.uint8)
img_rouge[:,:,2] = img[:,:,2]

winname = 'Canal de rouge'
cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
cv2.imshow(winname, img_rouge)
cv2.waitKey()
cv2.destroyAllWindows()

# Consigne: Faire la même chose pour les deux autres canaux.

############################## Fin étape 6 ##############################

############################## Étape 7 ##############################
# Consigne: Créer une "class" appellée "Point", à qui on donne deux coordonnées, X et Y
# pendant sa contruction, et avec lequel on peut calculer la distance euclidienne
# jusqu'à un autre point en donnant les coordonnées X et Y du deuxième point seulement

### Début de la class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, x2, y2):
        return np.sqrt((self.x - x2)**2 + (self.y - y2)**2)

    def dist_to_point(self, p2):
        x2 = p2.x
        y2 = p2.y
        return self.dist(x2, y2)

    def get_coords(self):
        return (self.x, self.y)
### Fin de la class

# Exemple d'utilisation de la class
p1 = Point(5,5)
p2 = Point(10,1)
print("La distance entre {} et {} est égale à: {}".format(p1.get_coords(), p2.get_coords(), p1.dist_to_point(p2)))

############################## Fin étape 7 ##############################