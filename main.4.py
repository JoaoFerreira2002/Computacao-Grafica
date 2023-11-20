from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import time
import math

class RGB:
    def __init__(self, red, green, blue, alpha):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

class Sphere:
    def __init__(self, radius, slices=150, stacks=150):
        self.radius = radius
        self.slices = slices
        self.stacks = stacks

    def new(self, position, color: RGB):
        ambient_color = [0.2, 0.2, 0.2, 1.0]
        specular_color = [0.1, 0.1, 0.1, 1]
        shininess = 10.0

        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_color)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [color.red, color.green, color.blue, 1.0])
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        glutSolidSphere(self.radius, self.slices, self.stacks)
        glPopMatrix()
            

elements = [1, 3, 4, 2]
n = len(elements)
swap_i = 0
swap_j = 0
swap_percentage = 0.0
verde = RGB(0.0, 1.0, 0.5, 1.0)

# Camera parameters
cameraRadius = 10.0
cameraAngle = 0.0
cameraSpeed = 360.0 / 45.0  # 1 full rotation every 15 seconds

# Rotation speed increment/decrement
speedIncrement = 1.0

# Camera angle increment/decrement
angleIncrement = 10.0

# So pra manter um tamanho correto dos objetos
def define_raios(lista):
    raios = []
    tamanho_base = 0.6
    minimun = min(lista)
    maximun = max(lista)
    for i in range(len(lista)):
        normalize = (lista[i] - minimun) / (maximun - minimun)
        if lista[i] == minimun:
            size = 0.3 + (tamanho_base * normalize)
        if lista[i] == maximun:
            size = 0.1 + (tamanho_base * normalize)
        else:
            size = 0.2 + (tamanho_base * normalize)
        raios.append(size)

    return raios

def create_spheres():
    return [Sphere(r) for r in define_raios(elements)]
    
# spheres = create_spheres()
def draw_sphere(spheres, element, position, is_comparing=False, cor=RGB(1, 1, 1, 1)):
    # global spheres
    if is_comparing:
        cor = RGB(0.9, 0, 0, 0)

    spheres[element].new(position, cor)

def draw_text(position, text):
    glPushMatrix()
    glTranslatef(position[0], 0, 1)

    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(-0.05, -0.05)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    glPopMatrix()

def draw_elements(isDone=False):
    for i, elemento in enumerate(elements):
        comparing = i == swap_i or i == swap_j
        if isDone:
            position = (i * 1.4 - 3, 2, 0)
            spheres = create_spheres()
            draw_sphere(spheres, i, position, False, verde)
        else:
            position = (i * 1.4 - 3, 0.5, 0)
            spheres = create_spheres()
            draw_sphere(spheres, i, position, comparing)
        draw_text(position, str(elemento))

def draw_room():
    # Draw the floor, walls, and roof
    grid_size = 15
    
    # Floor
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-grid_size, -3 / 3, -grid_size)
    glVertex3f(grid_size, -3 / 3, -grid_size)
    glVertex3f(grid_size, -3 / 3, grid_size)
    glVertex3f(-grid_size, -3 / 3, grid_size)
    glEnd()
    
    # Roof
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-grid_size, grid_size, -grid_size)
    glVertex3f(grid_size, grid_size, -grid_size)
    glVertex3f(grid_size, grid_size, grid_size)
    glVertex3f(-grid_size, grid_size, grid_size)
    glEnd()

    # Walls
    glColor3f(1, 1, 1)
    # Left Wall
    glBegin(GL_QUADS)
    glVertex3f(-grid_size, -3 / 3, -grid_size)
    glVertex3f(-grid_size, grid_size, -grid_size)
    glVertex3f(-grid_size, grid_size, grid_size)
    glVertex3f(-grid_size, -3 / 3, grid_size)
    glEnd()
    
    # Right Wall
    glBegin(GL_QUADS)
    glVertex3f(grid_size, -3 / 3, -grid_size)
    glVertex3f(grid_size, grid_size, -grid_size)
    glVertex3f(grid_size, grid_size, grid_size)
    glVertex3f(grid_size, -3 / 3, grid_size)
    glEnd()
    
    # Back Wall
    glBegin(GL_QUADS)
    glVertex3f(-grid_size, -3 / 3, -grid_size)
    glVertex3f(grid_size, -3 / 3, -grid_size)
    glVertex3f(grid_size, grid_size, -grid_size)
    glVertex3f(-grid_size, grid_size, -grid_size)
    glEnd()

def draw_scene():
    draw_room()
    draw_elements()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.09, 0.09, 0.09, 0.6)
    glEnable(GL_DEPTH_TEST)

    # Set light source position
    # light_position = [14, 10.0, 3, 1.0] # x, y, z => x distancia horizontal, y altura, z frente (positivo) e atras (negativo)
    light_position = [14, 15.0, 15, 1.0] # x, y, z => x distancia horizontal, y altura, z frente (positivo) e atras (negativo)
    lightZeroColor = [0.6, 0.6, 0.6, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE);
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Set up the camera position
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    cameraX = cameraRadius * math.sin(cameraAngle * math.pi / 180.0)
    cameraZ = cameraRadius * math.cos(cameraAngle * math.pi / 180.0)
    gluLookAt(cameraX, 3.0, cameraZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    draw_scene()
    glutSwapBuffers()

def bubble_sort():
    global swap_i, swap_j, swap_percentage
    sorted = False

    while not sorted:
        sorted = True

        for j in range(0, n - 1):
            swap_i, swap_j = j, j + 1

            for percentage in range(100):
                swap_percentage = percentage / 100.0
                glutPostRedisplay()  # Request a redraw
                glutMainLoopEvent()  # Allow the main loop to process events
                time.sleep(0.01)

            if elements[j] > elements[j + 1]:
                elements[j], elements[j + 1] = elements[j + 1], elements[j]
                sorted = False

                # Animate the transition
                for frame in range(100):
                    swap_percentage = frame / 100.0
                    glutPostRedisplay()
                    glutMainLoopEvent()
                    time.sleep(0.01)
    draw_elements(True)
    glutSwapBuffers()
    time.sleep(0.01)                
    glutIdleFunc(None)

def reshapeWindow(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w) / float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        3, 3, 10, # (x, y ,z) posição da camera no espaço
        -1, 0, -1,  # ponto focal da camera
        0, 1, 0   # controla altura no eixo escolhido (y no caso)
    )  # Ajusta a posição da câmera

def timerFunc(value):
    # Update the camera angle
    global cameraAngle
    cameraAngle += cameraSpeed * 0.01  # 0.01 seconds elapsed

    # Redraw the scene
    glutPostRedisplay()

    # Set the timer for the next update
    glutTimerFunc(10, timerFunc, 0)  # 10 milliseconds interval

def specialKeyHandler(key, x, y):
    global cameraRadius, cameraAngle
    if key == GLUT_KEY_UP:
        cameraRadius -= 0.1
        if cameraRadius < 0.1:
            cameraRadius = 0.1
    elif key == GLUT_KEY_DOWN:
        cameraRadius += 0.1
    elif key == GLUT_KEY_LEFT:
        cameraAngle += angleIncrement
    elif key == GLUT_KEY_RIGHT:
        cameraAngle -= angleIncrement

    # Redraw the scene
    glutPostRedisplay()

def keyboardHandler(key, x, y):
    global cameraSpeed
    if key == b'+':
        cameraSpeed += speedIncrement
    elif key == b'-':
        cameraSpeed -= speedIncrement

    # Redraw the scene
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Bubble Sort 3D")
    glutDisplayFunc(display)
    glutReshapeFunc(reshapeWindow)
    glutSpecialFunc(specialKeyHandler)
    glutKeyboardFunc(keyboardHandler)
    glutIdleFunc(bubble_sort)
    glutTimerFunc(10, timerFunc, 0)

    # Set up the initial camera position
    gluLookAt(
        0.0, 3.0, cameraRadius,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )

    glutMainLoop()

if __name__ == "__main__":
    main()