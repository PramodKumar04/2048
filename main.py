import pygame
import random
import math

pygame.init()

FPS = 60 #frame per second to set how fast it works
WIDTH,HEIGHT=600,600 # height and width of the square
ROWS,COLS=4,4
RECT_HEIGHT= HEIGHT//ROWS #defining the height of each row
RECT_WIDTH= WIDTH//COLS #defining the width of each col
#setting_up colors
OUTLINE_COLOR=(187,173,160) #grey
OUTLINE_THICKNESS =10
BG_COLOR=(205,192,180)
FONT_COLOR=(119,110,101)

FONT=pygame.font.SysFont("comicsans",60,bold=True)
#speed of movement of the tiles in the game
MOVE_VEL= 15

#to sET-UP the pygame window
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2048")#title of the window

class Tile:
    #defining colors each number tile
    COLORS=[
        (237,229,218),
        (238,225,201),
        (243,178,122),
        (246,150,101),
        (247,124,95),
        (247,95,59),
        (237,208,115),
        (237,204,99),
        (236,202,80)
    ]
    def __init__(self,value,row,col):
        self.value=value
        self.row=row
        self.col=col
        self.x=col*RECT_WIDTH
        self.y=row*RECT_HEIGHT
    
    def get_color(self):
        #for each power of 2 we need to set the color
        # so using the logarithm we get power which will be the index of color
        color_index=int(math.log2(self.value))-1
        color=self.COLORS[color_index]
        return color #returns the color based on the color_index

    
    def draw(self,window):
        color= self.get_color()#to get the color
        #drawing a tile at specified pos and size with required color
        pygame.draw.rect(window,color,(self.x,self.y,RECT_WIDTH,RECT_HEIGHT))
        #to get the number text
        
        text=FONT.render(str(self.value),1,FONT_COLOR)
        window.blit(text, 
    (self.x + RECT_WIDTH / 2 - text.get_width() / 2, 
     self.y + RECT_HEIGHT / 2 - text.get_height() / 2)
    )

    def set_pos(self,ceil=False):
        if ceil:
            self.row=math.ceil(self.y/RECT_HEIGHT)
            self.col=math.ceil(self.x/RECT_WIDTH)
        else:
            self.row=math.floor(self.y/RECT_HEIGHT)
            self.col=math.floor(self.x/RECT_WIDTH)
        
    
    def move(self,delta):
        self.x+=delta[0]
        self.y+=delta[1]


def draw_grid(window):
    #drawing horizontal row
    for row in range(1,ROWS):
        y=row*RECT_HEIGHT
        pygame.draw.line(window,OUTLINE_COLOR,(0,y),(WIDTH,y),OUTLINE_THICKNESS)
    #drawing the vertical line 
    for col in range(1,COLS):
        x=col*RECT_WIDTH
        pygame.draw.line(window,OUTLINE_COLOR,(x,0),(x,WIDTH),OUTLINE_THICKNESS)
    pygame.draw.rect(window,OUTLINE_COLOR,(0,0,WIDTH,HEIGHT),OUTLINE_THICKNESS)

def draw(window,tiles):
    window.fill(BG_COLOR)
    #drawing all the tiles before the grid appears
    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    pygame.display.update()

def get_random_pos(tiles):
    row =None
    col=None
    while True:
        row =random.randrange(0,ROWS)
        col=random.randrange(0,COLS)
        if(f"{row}{col}" not in tiles):
            break
    return row,col



#main logic for movement of tiles
def move_tiles(window,tiles,clock,direction):
    updated=True
    blocks=set()

    if direction == "left":
        #if we are moving to the left direction so sorting the dictionary according to column key
        sort_func=lambda x: x.col
        reverse =False #to sort in reverse or not
        delta=(-MOVE_VEL,0) #to specify the position by which the tile should move
        boundary_check =lambda tile: tile.col==0 #to check whether the tile is at left most
        #to get the before tile value
        get_next_tile= lambda tile: tiles.get(f"{tile.row}{tile.col-1}")
        #to merge the tiles or not 
        merge_check=lambda tile,next_tile:tile.x>next_tile.x+MOVE_VEL
        #if both the tiles are having same values or not
        move_check=(
            lambda tile,next_tile:tile.x>next_tile.x+RECT_WIDTH+MOVE_VEL
        )
        ceil=True


    elif direction=="right":
        #if we are moving to the right direction so sorting the dictionary according to column key
        sort_func=lambda x: x.col
        reverse =True #to sort in reverse or not
        delta=(MOVE_VEL,0) #to specify the position by which the tile should move
        boundary_check =lambda tile: tile.col==COLS-1 #to check whether the tile is at right most
        #to get the after tile value
        get_next_tile= lambda tile: tiles.get(f"{tile.row}{tile.col+1}")
        #to merge the tiles or not 
        merge_check=lambda tile,next_tile:tile.x<next_tile.x-MOVE_VEL
        #if both the tiles are having same values or not
        move_check=(
            lambda tile,next_tile:tile.x+RECT_WIDTH+MOVE_VEL < next_tile.x
        )
        ceil=False
    elif direction=="up":
        #if we are moving to the up direction so sorting the dictionary according to column key
        sort_func=lambda y: y.row
        reverse =False #to sort in reverse or not
        delta=(0,-MOVE_VEL) #to specify the position by which the tile should move
        boundary_check =lambda tile: tile.row==0 #to check whether the tile is at up most
        #to get the before tile value
        get_next_tile= lambda tile: tiles.get(f"{tile.row-1}{tile.col}")
        #to merge the tiles or not 
        merge_check=lambda tile,next_tile:tile.y>next_tile.y+MOVE_VEL
        #if both the tiles are having same values or not
        move_check=(
            lambda tile,next_tile:tile.y>next_tile.y+RECT_HEIGHT+MOVE_VEL
        )
        ceil=True
    elif direction=="down":
        #if we are moving to the down direction so sorting the dictionary according to column key
        sort_func=lambda y: y.row
        reverse =True #to sort in reverse or not
        delta=(0,MOVE_VEL) #to specify the position by which the tile should move
        boundary_check =lambda tile: tile.row==ROWS-1 #to check whether the tile is at down most
        #to get the before tile value
        get_next_tile= lambda tile: tiles.get(f"{tile.row+1}{tile.col}")
        #to merge the tiles or not 
        merge_check=lambda tile,next_tile:tile.y<next_tile.y-MOVE_VEL
        #if both the tiles are having same values or not
        move_check=(
            lambda tile,next_tile:tile.y+RECT_HEIGHT+MOVE_VEL<next_tile.y
        )
        ceil=False

    while updated:
        clock.tick(FPS)
        updated=False
        sorted_tiles=sorted(tiles.values(),key=sort_func,reverse=reverse)

        for i,tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            next_tile=get_next_tile(tile)
            #if no tile is present
            if not next_tile:
                tile.move(delta)
            #if both tiles are having the same value
            elif (tile.value== next_tile.value
                  and tile not in blocks and
                  next_tile not in blocks
            ):
                if merge_check(tile,next_tile):
                    tile.move(delta)
                else:
                    next_tile.value*=2 #updating the value
                    sorted_tiles.pop(i)# removing the previous tile
                    blocks.add(next_tile)#to prevent more than one merge
            elif move_check(tile,next_tile):
                tile.move(delta)
            else:
                continue
            tile.set_pos(ceil)
            updated=True
        update_tiles(window,tiles,sorted_tiles)
    return end_move(tiles)

#to check whether the game is ended
def end_move(tiles):
    if len(tiles)==16:
        return "lost"
    row,col=get_random_pos(tiles)
    tiles[f"{row}{col}"]=Tile(random.choice([2,4]),row,col)
    return "continue"

def update_tiles(window,tiles,sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"]=tile

#randomly generating the tile
def generate_tiles():
    tiles={}
    for _ in range(2):
        row,col=get_random_pos(tiles)
        tiles[f"{row}{col}"]=Tile(2,row,col)
    
    return tiles

def main(window):
    clock=pygame.time.Clock()
    run =True #flag to confirm to run the game or not
    tiles=generate_tiles()
    while run:
        clock.tick(FPS) #to run the game at specified fps

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    move_tiles(window,tiles,clock,"left")
                if event.key==pygame.K_RIGHT:
                    move_tiles(window,tiles,clock,"right")
                if event.key==pygame.K_UP:
                    move_tiles(window,tiles,clock,"up")
                if event.key==pygame.K_DOWN:
                    move_tiles(window,tiles,clock,"down")
        draw(window,tiles)
    pygame.quit()

if __name__== "__main__":
    main(WINDOW)

