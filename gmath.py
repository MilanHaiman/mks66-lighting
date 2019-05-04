import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambientlight, light, areflect, dreflect, sreflect ):
  A=limit_color(calculate_ambient(ambientlight, areflect))
  D=limit_color(calculate_diffuse(light,dreflect,normal))
  S=limit_color(calculate_specular(light,sreflect,view,normal))
  I=[int(A[i]+D[i]+S[i]) for i in range(3)]
  return limit_color(I)

def calculate_ambient(ambientlight, areflect):
  return [ambientlight[i]*areflect[i] for i in range(3)]

def calculate_diffuse(light, dreflect, normal):
  L=light[0]
  I_L=light[1]
  normalize(L)
  normalize(normal)
  return [I_L[i]*dreflect[i]*dot_product(L,normal) for i in range(3)]

def calculate_specular(light, sreflect, view, normal):
  L=light[0]
  I_L=light[1]
  normalize(L)
  normalize(normal)
  normalize(view)
  R = [2*dot_product(normal,L)*normal[i]-L[i] for i in range(3)]
  return [I_L[i]*sreflect[i]*dot_product(R,view)**SPECULAR_EXP for i in range(3)]

def limit_color(color):
  return [clamp(color[i],0,255) for i in range(3)]

def clamp(x,m,M):
  if x<m:
    x=m
  if x>M:
    x=M
  return x

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
