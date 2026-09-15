import pygame
import time 
import json
pygame.init()
pygame.font.init()

gamesize = 800
border = 100
if 0==1:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Crystal Diffuser")
    screen_width = screen.get_width()
    screen_hight = screen.get_height()
if 1==1:
    screen_hight = gamesize
    screen_width = screen_hight*1.25
    screen = pygame.display.set_mode((screen_width, screen_hight))
    pygame.display.set_caption("Crystal Diffuser")
    clock = pygame.time.Clock()
sizex = (screen_width-border*2*1.25)/10
sizey = (screen_hight-border*2)/8
color1 = (50,50,50)
color2 = (70,70,70)
fillcolor = (100,100,100)
pieces = []
sc = (1,0,0)
my_font = pygame.font.Font("Minecraftia.ttf", 30)
def getcolor(item):
    match item:
        case (0,0,0):
            color = (255,255,255)
        case (1,0,0):
            color = (255,0,0)
        case (0,1,0):
            color = (255,255,0)
        case (0,0,1):
            color = (0,0,255)
        case (1,1,0):
            color = (255,128,0)
        case (0,1,1):
            color = (0,255,0)
        case (1,0,1):
            color = (255,0,255)
        case (1,1,1):
            color = (0,0,0)
    return color
def drawsquare(x,y):
        rectangle = pygame.Rect((x*sizex+border*1.25),(y*sizey+border),(sizex),(sizey))
        if int(y)%2 == 1:
            if int(x)%2 == 1 :
                squarecolor = color1
            else:
                squarecolor = color2
        else:
            if int(x)%2 == 1 :
                squarecolor = color2
            else:
                squarecolor = color1
        pygame.draw.rect(screen,(squarecolor), rectangle)
        if cords.get((x,y)) != "void":
            currentcell = cords.get((x,y))
            drawtriangle(getcolor(currentcell[1]),currentcell[0],x,y)
def drawgrid():
    for x in range(10):
        for y in range (8):
            drawsquare(x,y)
def drawtriangle(tricolor, rotation, x, y):
    x = x*sizex+border*1.25
    y = y*sizey+border
    match rotation:
        case 1:
            pygame.draw.polygon(screen,tricolor,( (x+1,y), (x+sizex-1,y) ,(x+sizex-1, y+sizey-1) ))
        case 2:
            pygame.draw.polygon(screen,tricolor,( (x,y), (x+sizex-1,y) ,(x, y+sizey-1) ))
        case 3:
            pygame.draw.polygon(screen,tricolor,( (x,y+1), (x+sizex-1,y+sizey-1) ,(x, y+sizey-1) ))
        case 4:
            pygame.draw.polygon(screen,tricolor,( (x+sizex-1,y+sizey-1), (x+sizex-1,y) ,(x, y+sizey-1) ))
        case 5:
            rectangle=pygame.Rect((x),(y),(sizex),(sizey))
            pygame.draw.rect(screen,(tricolor), rectangle)
def drawshape(shape,x,y):
    shapecolor = shape[0]
    for piece in shape[1:]:
        drawtriangle((getcolor(shapecolor)),piece[0],piece[1]+x,piece[2]+y)
        cords[str(piece[1]+x)+","+str(piece[2]+y)] = (piece[0],shapecolor)
def rotateshape(shape,rotation):
    rotation = rotation-(int(rotation/4))
    
    if rotation > 0:
        positive = 1
    else:
        positive = -1 
    outshape = [shape[0]]
    for piece in shape[1:]:
        for i in range(rotation):
            piece = [piece[0], piece[2]*positive*-1, piece[1]*positive]
            if piece[0] != 9:
                piece[0] += positive*-1
                if piece[0] > 4:
                    piece[0] -= 4
                if piece[0] < 1:
                    piece[0] += 4
        outshape.append(piece)
    return outshape
def checkmousecolision(corner1x, corner1y, corner2x, corner2y):
    if mousex > corner1x and mousey > corner1y and mousex < corner2x and mousey < corner2y:
        return True
    else:
        return False
def drawtext(text,x,y,color):
    text_surface = my_font.render(text, False, color)
    screen.blit(text_surface, (x,y))

cords = {}
for x in range (10):
    for y in range (8):
        cords[(x,y)] = "void"
export_width, export_hight = my_font.size("export")
screen.fill(fillcolor)
running = True

if 1==0:
    tshape = [(0,1,0),(1,-1,0),(1,0,1),(9,0,0)]
    testdict = {}
    testdict["data"] = []
    testdict["data"].append(tshape)
    testdict["data"].append([(1,0,0),(9,0,0),(3,1,0),(1,-1,0)])
    dumpsed_data = json.dumps(testdict)
    with open("shapes.json", "w") as f:
        json.dump(testdict, f, indent=3)
    with open("shapes.json", "r") as f:
        sfile = json.load(f)["data"]


def export(shape):
    with open("shapes.json", "r") as f:
        sfile = json.load(f)

    sfile["data"].append(shape)

    with open("shapes.json", "w") as f:
        json.dump(sfile, f, indent=3)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mousex, mousey = pygame.mouse.get_pos()
                mx = round(((mousex-border*1.25)/sizex)-0.5)
                my = round(((mousey-border)/sizey)-0.5)
                if mx < 0 or mx > 9 or my < 0 or my > 7:
                    mx = "out"
                    my = "side"
                if isinstance(my, int):
                    cell = cords.get((mx,my))

                    #a cords cell SHOULD look like (rotation,(r,y,b))
                    #a shape cell SHOULD look like (rotation,x,y)
                    if cell == "void": 
                        #creates the cell
                        cords[(mx,my)] = (1,sc)
                        if len(pieces) == 0:
                            origin_point = (mx,my)
                            pieces.append((1,0,0))
                        else:
                            pieces.append((1,mx-origin_point[0],my-origin_point[1]))

                    if cell != "void":
                        index = pieces.index((cell[0],mx-origin_point[0],my-origin_point[1]))


                        #rotates the cell
                        cell = (cell[0]+1,cell[1])
                        cell = (cell[0]-(int(cell[0]/6))*6, cell[1])
                        #adds the cell to cords and shape
                        if cell[0] == 0:
                            cords[(mx,my)] = "void"
                            pieces.pop(index)
                        else:
                            cords[(mx,my)] = cell
                            pieces[index] = (cell[0],mx-origin_point[0],my-origin_point[1])
            if checkmousecolision(20,0,export_width,export_hight):
                #with open("shape.txt","a") as f:
                    #f.write("\n"+((str(pieces)).replace("5","9").replace(" ","")))
                


                print(pieces)

                output = pieces.copy()
                for i in range(len(output)-1):
                    print(i, output[i])
                    if output[i][0] == 5:
                    
                        output[i] = (9,output[i][1],output[i][2])

                output.insert(0,sc)

                export(output)


    drawgrid()
    drawtext("export",20,0,(128,128,128))
    pygame.display.update()
                        
pygame.quit()