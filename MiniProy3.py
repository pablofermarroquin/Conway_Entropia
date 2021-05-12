import pygame
import numpy as np
import time
import matplotlib.pyplot as plt 
import random as rnd

def DistanciaTaxi():
    dist=0
    m=0         #donde m es la masa total del sistema. Osea la cantidad de cuadros activos.
    for i in range(0,nX,1):
        for j in range(0,nY,1):
            if (status[i][j]>0.0):
                dist+=abs(i-xo)+abs(j-yo)
                m+=1
    #if(dist/m > Distancias[len(Distancias)-1]):
    Distancias.append(dist/m)
    Ms.append(m)
    
     
def Kinetic():
    for i in range(0,len(Distancias)-1,1):
        posF=Distancias[i+1]
        posI=Distancias[i]
        Energias.append(0.5*Ms[i]*(posF-posI)**2)
    
    for i in range(0,len(Energias)-1,1):
        EF=Energias[i+1]
        EI=Energias[i]
        Trabajos.append(EF-EI)
        
    fig2, ax2 = plt.subplots(1)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Trabajo (J)")
    plt.title("\nTrabajo vrs. Tiempo")
    ax2.plot(Trabajos)
        
def Graf_Dist():
    fig, ax = plt.subplots(1)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Distancia Taxi (m)")
    plt.title("\nDistancia Taxi vrs. Tiempo")    
    ax.plot(Distancias)
    plt.show()
    
def Calc_Entropia(variable, tipo):
    temp=[]
    for i in range(0,len(variable)-1,1):
        temp.append(variable[i+1]-variable[i])
    print("Entropía media "+ tipo+": "+str(np.mean(temp)))
    print("Desv. Estándar entropía "+ tipo+": "+str(np.std(temp)))
    


def StatusInicial():
    #status[0,0]=1
    status[(xo+1)%nX,(yo+0)%nY]=1 
    status[(xo+2)%nX,(yo+0)%nY]=1
    status[(xo+0)%nX,(yo+1)%nY]=1
    status[(xo+1)%nX,(yo+1)%nY]=1
    status[(xo+2)%nX,(yo+1)%nY]=1
    status[(xo+5)%nX,(yo+1)%nY]=1
    status[(xo+1)%nX,(yo+2)%nY]=1
    status[(xo+3)%nX,(yo+2)%nY]=1
    status[(xo+5)%nX,(yo+2)%nY]=1
    status[(xo+2)%nX,(yo+3)%nY]=1
    status[(xo+4)%nX,(yo+3)%nY]=1
    status[(xo+5)%nX,(yo+3)%nY]=1
    status[(xo+3)%nX,(yo+4)%nY]=1
    status[(xo+4)%nX,(yo+4)%nY]=1
    status[(xo+2)%nX,(yo+5)%nY]=1
    status[(xo+3)%nX,(yo+5)%nY]=1
    status[(xo+4)%nX,(yo+5)%nY]=1

WIDTH, HEIGHT = 800, 800
nX, nY = 60, 60
xSize = WIDTH/nX
ySize = HEIGHT/nY
rnd.seed(37)  #5, 35,  14, para distancia
# para trabajo 39 para 30x30      36 para 40x40       39 para 30x30
# 37 para 60x60 funciona super bien

Energias=[]
Trabajos=[]
Distancias=[]
#Distancias.append(3.25)

Ms=[]
#Ms.append(16)
contando=False
xo=  rnd.randint(0,int(nX)) #int(nX/2)
yo=  rnd.randint(0,int(nY)) #int(nY/2)

pygame.init() # Initialize PyGame

screen = pygame.display.set_mode([WIDTH,HEIGHT]) # Set size of screen

BG_COLOR = (10,10,10) # Define background color
LIVE_COLOR = (255,255,255)
DEAD_COLOR = (128,128,128)
# Celdas vivas = 1; Celdas muertas = 0
status = np.zeros((nX,nY)) # Intialize status of cells
StatusInicial()

pauseRun = True

running = True
while running:

    newStatus = np.copy(status) # Copy status

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pauseRun = not pauseRun
                contando=True
                

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            #newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newStatus[x,y] = not mouseClick[2]

    screen.fill(BG_COLOR) # Clean background

    for x in range(0,nX):
        for y in range(0,nY):


            if not pauseRun:

                # Numero de vecinos
                nNeigh = status[(x-1)%nX,(y-1)%nY] + status[(x)%nX,(y-1)%nY] + \
                        status[(x+1)%nX,(y-1)%nY] + status[(x-1)%nX,(y)%nY] + \
                        status[(x+1)%nX,(y)%nY] + status[(x-1)%nX,(y+1)%nY] + \
                         status[(x)%nX,(y+1)%nY] + status[(x+1)%nX,(y+1)%nY]

                # Rule 1: Una celula muerta con 3 vecinas revive
                if status[x,y] == 0 and nNeigh==3:
                    newStatus[x,y] = 1

                # Rule 2: Una celula viva con mas de 3 vecinos o menos de 2 muere
                elif status[x,y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newStatus[x,y] = 0


            poly = [(x*xSize,y*ySize),
                    ((x+1)*xSize,y*ySize),
                    ((x+1)*xSize,(y+1)*ySize),
                    (x*xSize,(y+1)*ySize)]

            if newStatus[x,y] == 1:
                pygame.draw.polygon(screen,LIVE_COLOR,poly,0)
            else:
                pygame.draw.polygon(screen,DEAD_COLOR,poly,1)

    status = np.copy(newStatus)
    time.sleep(0.1)
    pygame.display.flip()
    if contando:
        DistanciaTaxi()



pygame.quit()
Graf_Dist()
Kinetic()
Calc_Entropia(Distancias,"distancia taxi")
Calc_Entropia(Energias,"energía cinética")