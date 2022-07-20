import pygame
import random
import pytmx
import math
#Just preparation
SCREENWIDTH = 1600
SCREENHEIGHT =960

pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUESKY = (135,200,250)
GREEN = (0,255,0)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
GREENGRASS = (124,252,0)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Emporio")
armory = pygame.image.load("armory.png")
castle = pygame.image.load("castle.png")
farm = pygame.image.load('farm.png')
house = pygame.image.load('house.png')
lumber = pygame.image.load('lumber.png')
mine = pygame.image.load('mine.png')

goldimg = pygame.image.load("gold.png")
woodimg = pygame.image.load("wood.png")
stoneimg = pygame.image.load("stone.png")
foodimg = pygame.image.load("fruit.png")
manimg = pygame.image.load("user.png")
armorimg = pygame.image.load("armor.png")

armoryn = pygame.image.load("armorynote.png")
castlen = pygame.image.load("castlenote.png")
farmn = pygame.image.load('farmnote.png')
housen = pygame.image.load('housenote.png')
lumbern = pygame.image.load('lumbernote.png')
minen = pygame.image.load('minenote.png')

cross = pygame.image.load('blue_boxCross.png')
instruction = pygame.image.load('instruction.png')
gold = 500
wood = 200
stone = 200
food = 200
armor = 0
man = 50

background = pygame.image.load('3.png')
attributes = [gold,wood,stone,food,man,armor]


cas = pygame.image.load('cas.png')

life = 1 + armor


ADDDAY = pygame.USEREVENT +1
ADDENEMY = pygame.USEREVENT +2
pygame.time.set_timer(ADDENEMY,250)
pygame.time.set_timer(ADDDAY,6000)

x0 = 50
y0 = 450
x_change =0
y_change = 0
#Class for the SceneBase (All Scenes)
class SceneBase:
    def __init__(self):
        self.next = self
        self.x = 0
        self.y = 0
    def ProcessInputs(self,events,pressed_keys):
        pass
    def Update(self):
        pass
    def Render(self,screen):
        pass
    def SwitchToScene(self,next_scene):
        self.next = next_scene
    def Terminate(self):
        self.SwitchToScene(None)
    def cost(self):
        pass
    def numbers(self):
        pass
days = 1
#This is to calculate if building is allowed or not:
def allowed():
    if stone - 20 < 0:
        return False
    elif wood - 20 <0:
        return False
    elif food - 20 <0:
        return False
    elif gold - 20 <0:
        return False
    elif man - 10 <0:
        return False
    else:
        return True

#Main:
def main(FPS,current_scene):

    clock = pygame.time.Clock()
    active_scene = current_scene
    quitgame = False
    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        #Filtered game events
        filtered_events = []
        for event in pygame.event.get():
            #QUIT FILTERING
            if event.type == pygame.QUIT:
                quitgame = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quitgame = True
                if event.key == pygame.K_F4 and alt_pressed == True:
                    quitgame = True
            if quitgame == True:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
            #Day changing = every resource changes
            if event.type == ADDDAY:
                global days
                if isinstance(active_scene,Scene2):
                    days = days +1
                    active_scene.numbers()


        #RENDERR THE IMAGES

        active_scene.ProcessInputs(filtered_events,pressed_keys)
        active_scene.Render()
        #Process inputs and update the game
        active_scene.Update()


        active_scene = active_scene.next
        pygame.display.flip()
        clock.tick(FPS)



#CLASS FOR MENU
class Menu(SceneBase):
    def __init__(self,items):
        SceneBase.__init__(self)
        self.state = -1
        self.items = items
        self.font = pygame.font.Font("kenvector_future_thin.ttf",30)
        self.sprite_sheet =pygame.image.load('button.png').convert()
        self.buttons = self.create_button()
        self.rect_list = self.get_rect_list()
        self.soundindex = -1
        self.sound = pygame.mixer.Sound("switch2.ogg")
        self.sound2 = pygame.mixer.Sound("mouseclick1.ogg")
    #Cut an image and return it
    def get_image(self,x,y,width,height):
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
        # Return the image
        return image
        #return
    #Get the blue and yellow button out of the original image
    def create_button(self):
        buttondict = {}
        buttondict["blue"] = self.get_image(0,0,190,49)
        buttondict["yellow"] = self.get_image(190,0,190,49)
        return buttondict
    #Put the buttons in their rightful positions
    def get_button_position(self,index):
        pX = SCREENWIDTH //2 - 190 // 2
        #total height of all buttons
        th = len(self.items) * 49
        pY = (SCREENHEIGHT //2) - th //2 + index * (49+6)
        return pX, pY
    #Get the rect of the buttons
    def get_rect_list(self):
        rect_list = []
        for index, item in enumerate(self.items):
            pX,pY = self.get_button_position(index)
            #Create rect
            rect = pygame.Rect(pX,pY,190,49)
            #Add to the list
            rect_list.append(rect)
        return rect_list
    #Find the text positions
    def get_text_position(self,label,button_position):
        # calculate position of the text on the button
        width = label.get_width()
        height = label.get_height()

        x,y = button_position

        posX = x + (190//2) - (width//2)
        posY = y + (49//2) - (height//2)

        return posX,posY
    #Rect of background white surface
    def get_bg_rect(self):
        btn_width = 190 + 100 # add 100 px padding
        btn_height = 49 * len(self.items) + 100 # add 100 px padding

        x = SCREENWIDTH // 2 - btn_width // 2
        y = SCREENHEIGHT // 2 - btn_height // 2
        width = btn_width
        height = btn_height

        rect = pygame.Rect(x,y,width,height)

        return rect
        #Render the menu
    def Render(self):
        #Render background
        screen.fill(BLUESKY)
        rect = self.get_bg_rect()
        pygame.draw.rect(screen,WHITE,rect)
        pygame.draw.rect(screen,BLACK,rect,2)
        #Render the buttons and texts
        for index,item in enumerate(self.items):
            if self.state == index:
                button = self.buttons["yellow"]
            else:
                button = self.buttons["blue"]
            label = self.font.render(item,True,BLACK)

            button_position = self.get_button_position(index)
            text_position = self.get_text_position(label,button_position)

            screen.blit(button,button_position)
            screen.blit(label,text_position)

    #The index to find if the mouse collide with the buttons or not
    def collide_index(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i,rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i
        return index
        #Change the state so that it corresponds if it touches any buttons
    def Update(self):
        self.state = self.collide_index()
        if self.state != -1 and self.state != self.soundindex:
            self.sound.play()
        self.soundindex = self.state

    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            #if state == 0, START , wwhich means switch to scene 1
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 0:
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
            #if state == 1, OPTIONS, which means switch to SETTINGS
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(credit())
            #if state == 2, CREDITS, wwhich means switch to CREDITS
            #if state ==3, EXIT, TERMINATE
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state == 2:
                self.sound2.play()
                self.Terminate()
    def numbers(self):
        pass
menu = Menu(("Start","Credits","Exit"))


listed = []
#Create kinda the same as menu but with more rect colliding with mouse.
class Scene2(SceneBase):

    def __init__(self,items):
        SceneBase.__init__(self)
        self.state = -1
        self.items = items
        self.font = pygame.font.Font("kenvector_future_thin.ttf",30)
        self.sprite_sheet =pygame.image.load('button.png').convert()
        self.buttons = self.create_button()
        self.rect_list = self.get_rect_list()
        self.soundindex = -1
        self.sound = pygame.mixer.Sound("switch2.ogg")
        self.sound2 = pygame.mixer.Sound("mouseclick1.ogg")
        self.build_rect = self.get_build_rect()
        self.collide_build = -1
        self.font2 = pygame.font.Font("kenvector_future_thin.ttf",15)
        self.font3 = pygame.font.Font("kenvector_future_thin.ttf",60)
    def get_image(self,x,y,width,height):
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
        # Return the image
        return image
        #return
    def create_button(self):
        buttondict = {}
        buttondict["blue"] = self.get_image(0,0,190,49)
        buttondict["yellow"] = self.get_image(190,0,190,49)
        return buttondict
    def get_button_position(self,index):
        pX = SCREENWIDTH - 190 // 2 - 288//2
        #total height of all buttons
        th = len(self.items) * 49
        pY = (SCREENHEIGHT //2) - th //2 + index * (49+6)
        return pX, pY
    def get_rect_list(self):
        rect_list = []
        for index, item in enumerate(self.items):
            pX,pY = self.get_button_position(index)
            #Create rect
            rect = pygame.Rect(pX,pY,190,49)
            #Add to the list
            rect_list.append(rect)
        return rect_list
    #Find the text positions
    def get_text_position(self,label,button_position):
        # calculate position of the text on the button
        width = label.get_width()
        height = label.get_height()

        x,y = button_position

        posX = x + (190//2) - (width//2)
        posY = y + (49//2) - (height//2)

        return posX,posY
    def collide_index(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i,rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i
        return index
    def get_build_rect(self):
        rect_list = []
        rect1 = pygame.Rect(497,341,90,60)
        rect2 = pygame.Rect(752,341,90,60)
        rect3 = pygame.Rect(975,341,90,60)
        rect4 = pygame.Rect(368,530,90,60)
        rect5 = pygame.Rect(594,530,90,60)
        rect6 = pygame.Rect(847,530,90,60)
        rect7 = pygame.Rect(207,723,90,60)
        rect8 = pygame.Rect(431,723,90,60)
        rect9 = pygame.Rect(654,723,90,60)
        rect_list.append(rect1)
        rect_list.append(rect2)
        rect_list.append(rect3)
        rect_list.append(rect4)
        rect_list.append(rect5)
        rect_list.append(rect6)
        rect_list.append(rect7)
        rect_list.append(rect8)
        rect_list.append(rect9)
        return rect_list
    def collide_building(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i,rect in enumerate(self.build_rect):
            if rect.collidepoint(mouse_pos):
                index = i
        return index
    def Update(self):
        self.state = self.collide_index()
        if self.state != -1 and self.state != self.soundindex:
            self.sound.play()
        self.soundindex = self.state
        self.collide_build = self.collide_building()
        label1 = self.font.render(str(gold),True,BLACK)
        label2 = self.font.render(str(wood),True,BLACK)
        label3 = self.font.render(str(stone),True,BLACK)
        label4 = self.font.render(str(man),True,BLACK)
        label5 = self.font.render(str(food),True,BLACK)
        label6 = self.font.render(str(armor),True,BLACK)
        screen.blit(label1,(300,75))
        screen.blit(label2,(700,75))
        screen.blit(label3,(1100,75))
        screen.blit(label4,(300,150))
        screen.blit(label5,(700,150))
        screen.blit(label6,(1100,150))
        label7 = self.font3.render("DAY "+str(days),True,BLACK)
        screen.blit(label7,(1370,70))

        if self.collide_build ==0:
            screen.blit(instruction,(580,400))
        if self.collide_build ==1:
            screen.blit(instruction,(830,400))
        if self.collide_build ==2:
            screen.blit(instruction,(1020,400))
        if self.collide_build ==3:
            screen.blit(instruction,(433,580))
        if self.collide_build ==4:
            screen.blit(instruction,(680,580))
        if self.collide_build ==5:
            screen.blit(instruction,(920,580))
        if self.collide_build ==6:
            screen.blit(instruction,(280,770))
        if self.collide_build ==7:
            screen.blit(instruction,(460,770))
        if self.collide_build ==8:
            screen.blit(instruction,(700,770))
    def Render(self):

        hud = pygame.image.load('HUD.png')
        screen.blit(hud,(0,0))
        lal = pygame.image.load('Scene2.png')
        screen.blit(lal,(32,246))

        for index,item in enumerate(self.items):
            if self.state == index:
                button = self.buttons["yellow"]
            else:
                button = self.buttons["blue"]
            label = self.font.render(item,True,BLACK)

            button_position = self.get_button_position(index)
            text_position = self.get_text_position(label,button_position)

            screen.blit(button,button_position)
            screen.blit(label,text_position)
        for i in range(len(listed)):
            screen.blit(listed[i][0],(listed[i][1],listed[i][2]))
        screen.blit(goldimg,(200,70))
        screen.blit(woodimg,(600,70))
        screen.blit(stoneimg,(1000,70))
        screen.blit(manimg,(200,145))
        screen.blit(foodimg,(600,145))
        screen.blit(armorimg,(1000,145))
        #Calculate all the resources.
    def numbers(self):
        global gold
        global man
        global stone
        global wood
        global food
        global armor
        for index in range(len(listed)):
            if listed[index][0] == house and food-5>=0 and stone-5 >=0 and wood -5 >=0:
                food = food - 5
                stone = stone - 5
                wood = wood - 5
                gold = gold + 10
            elif listed[index][0] == mine and food-5>=0 and gold-5 >=0 and wood -5 >=0:
                food = food - 5
                wood = wood - 5
                gold = gold - 5
                stone = stone + 30
            elif listed[index][0] == lumber and food-5>=0 and stone-5 >=0 and gold -5 >=0:
                food = food - 5
                wood = wood + 30
                gold = gold - 5
                stone = stone - 5
            elif listed[index][0] == farm and food-5>=0 and stone-5 >=0 and wood -5 >=0:
                food = food + 30
                wood = wood - 5
                stone = stone - 5
                gold = gold - 5
            elif listed[index][0] == castle and food-5>=0 and stone-5 >=0 and wood -5 >=0:
                food = food - 5
                wood = wood - 5
                stone = stone -5
                gold = gold + 30
            elif listed[index][0] == armory and food-5>=0 and stone-5 >=0 and wood -5 >=0 and gold - 5 >= 0 and man-2 >= 0:
                man = man - 2
                armor = armor + 2
                food = food - 5
                stone = stone - 5
                gold = gold - 5
                wood = wood -5


        if gold < 0:
            gold = 0
        if stone < 0:
            stone = 0
        if wood <0:
            wood = 0
        if food <0:
            food = 0
        if man <0:
            man = 0
    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 0 and allowed():
                x =497-5
                y = 341-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 1 and allowed():
                x =752-5
                y = 341-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 2 and allowed():
                x =975-5
                y = 341-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 3 and allowed():
                x =368-5
                y = 530-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 4 and allowed():
                x =594-5
                y = 530-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 5 and allowed():
                x =847-5
                y = 530-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 6 and allowed():
                x =207-5
                y = 723-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 7 and allowed():
                x =431-5
                y = 723-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.collide_build == 8 and allowed():
                x =654-5
                y = 723-50
                self.SwitchToScene(Scene3(("HOUSE","FARM","LUMBER","MINE","ARMORY","CASTLE"),x,y))
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 0:
                self.SwitchToScene(howtoplay())
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(soon())
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 2:
                self.SwitchToScene(howtoplayed())
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 3:
                self.Terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and (self.state == 0 or self.collide_build == 8 or self.collide_build == 7 or self.collide_build == 6 or self.collide_build == 5 or self.collide_build == 4 or self.collide_build == 3 or self.collide_build == 2 or self.collide_build == 1 or self.collide_build == 0) and not allowed():
                self.SwitchToScene(noresource())
class Scene3(SceneBase):#Kinda like the menu, but more complicated.
    def __init__(self,items,x,y):
        SceneBase.__init__(self)
        self.state = -1
        self.items = items
        self.font = pygame.font.Font("kenvector_future_thin.ttf",30)
        self.sprite_sheet =pygame.image.load('button.png').convert()
        self.buttons = self.create_button()
        self.rect_list = self.get_rect_list()
        self.soundindex = -1
        self.sound = pygame.mixer.Sound("switch2.ogg")
        self.sound2 = pygame.mixer.Sound("mouseclick1.ogg")
        self.font2 = pygame.font.Font("kenvector_future_thin.ttf",100)
        self.x = x
        self.y =y
    def get_image(self,x,y,width,height):
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
        # Return the image
        return image
        #return
    def create_button(self):
        buttondict = {}
        buttondict["blue"] = self.get_image(0,0,190,49)
        buttondict["yellow"] = self.get_image(190,0,190,49)
        return buttondict
    def get_button_position(self,index):
        pX = SCREENWIDTH//2 - 190//2
        #total height of all buttons
        th = len(self.items) * 49
        pY = (SCREENHEIGHT //2) - th //2 + index * (49+6)
        return pX, pY
    def get_rect_list(self):
        rect_list = []
        for index, item in enumerate(self.items):
            pX,pY = self.get_button_position(index)
            #Create rect
            rect = pygame.Rect(pX,pY,190,49)
            #Add to the list
            rect_list.append(rect)
        return rect_list
    #Find the text positions
    def get_text_position(self,label,button_position):
        # calculate position of the text on the button
        width = label.get_width()
        height = label.get_height()

        x,y = button_position

        posX = x + (190//2) - (width//2)
        posY = y + (49//2) - (height//2)

        return posX,posY
    def get_text_position2(self,label,button_position):
        width = label.get_width()
        height = label.get_height()
        x = SCREENWIDTH // 2
        y = SCREENHEIGHT//2 -300
        posX = x - width //2
        posY = y - height //2

        return posX,posY
    def collide_index(self):
        index = -1
        rectro = pygame.Rect(1530,40,38,36)
        mouse_pos = pygame.mouse.get_pos()
        for i,rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i
        if rectro.collidepoint(mouse_pos):
            index = 6
        return index
    def Update(self):
        self.state = self.collide_index()
        if self.state != -1 and self.state != self.soundindex:
            self.sound.play()
        self.soundindex = self.state

        if self.state == 0:
            screen.blit(housen,(850,350))
        if self.state == 1:
            screen.blit(farmn,(850,405))
        if self.state == 2:
            screen.blit(lumbern,(850,460))
        if self.state == 3:
            screen.blit(minen,(850,515))
        if self.state == 4:
            screen.blit(armoryn,(850,570))
        if self.state == 5:
            screen.blit(castlen,(850,625))

    def Render(self):
        screen.fill(BLUESKY)
        rect = pygame.Rect(50,50,SCREENWIDTH-100,SCREENHEIGHT-100)
        pygame.draw.rect(screen,WHITE,rect)
        pygame.draw.rect(screen,BLACK,rect,2)
        for index,item in enumerate(self.items):
            if self.state == index:
                button = self.buttons["yellow"]
            else:
                button = self.buttons["blue"]
            label = self.font.render(item,True,BLACK)
            label2 = self.font2.render("BUILDINGS",True,BLACK)
            button_position = self.get_button_position(index)
            text_position = self.get_text_position(label,button_position)
            text_position2 = self.get_text_position2(label2, button_position)
            screen.blit(button,button_position)
            screen.blit(label,text_position)
        box = pygame.image.load("blue_boxCross.png")
        screen.blit(label2,text_position2)
        screen.blit(box,(1530,40))
    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 0:
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
                listed.append((house,self.x,self.y))
                self.cost()
                global man
                man = man + 50
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1 :
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
                listed.append((farm,self.x,self.y))
                self.cost()
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 2:
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
                listed.append((lumber,self.x,self.y))
                self.cost()
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 3:
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
                listed.append((mine,self.x,self.y))
                self.cost()
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 4 :
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
                listed.append((armory,self.x,self.y))
                self.cost()
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 5:
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
                listed.append((castle,self.x,self.y))
                self.cost()
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 6:
                self.sound2.play()
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
    def numbers(self):
        pass
    def cost(self):
        global gold
        global wood
        global stone
        global food
        global man
        stone = stone - 20
        wood = wood - 20
        food = food - 20
        gold = gold - 20
        man = man - 10
class whitebox(SceneBase):
    #This is for all the scenes with notes and instructions
    def __init__(self):
        SceneBase.__init__(self)
        self.state = -1
        self.font = pygame.font.Font("kenvector_future_thin.ttf",20)
        self.soundindex = -1
        self.sound = pygame.mixer.Sound("switch2.ogg")
        self.sound2 = pygame.mixer.Sound("mouseclick1.ogg")
        self.font2 = pygame.font.Font("kenvector_future_thin.ttf",60)
    def Render(self):
        screen.fill(BLUESKY)
        rect = pygame.Rect(150,150,1300,660)
        pygame.draw.rect(screen,WHITE,rect)
        pygame.draw.rect(screen,BLACK,rect,2)
    def collide_index(self):
        index = -1
        rectro = pygame.Rect(1430,135,38,36)
        mouse_pos = pygame.mouse.get_pos()
        if rectro.collidepoint(mouse_pos):
            index = 1
        return index
    def Update(self):
        self.state = self.collide_index()
        if self.state != -1 and self.state != self.soundindex:
            self.sound.play()
        self.soundindex = self.state
class credit(whitebox):
    def __init__(self):
        whitebox.__init__(self)
    def Render(self):
        whitebox.Render(self)
        label1 = self.font.render("Special thanks to kenney.nl for allowing me to use their assets (tilesets,UI pack, sound pack)",True,BLACK)
        label2 = self.font2.render("CREDITS",True,BLACK)
        label3 = self.font.render("Credits to creators on flaticon for the icons used in this game: Freepik, Nikita Golubev, Those Icons",True,BLACK)
        label4 = self.font.render("Credits to Tiled Map Editor for the creation of the maps",True,BLACK)
        label5 = self.font.render("Special thanks to pygame community for developing the framework used to make this game",True,BLACK)
        screen.blit(label2,(700,200))
        screen.blit(label1,(250,400))
        screen.blit(label3,(250,435))
        screen.blit(label4,(250,470))
        screen.blit(label5,(250,505))
        screen.blit(cross,(1430,135))
    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(Menu(("START","CREDITS","EXIT")))
class howtoplay(whitebox):
    def __init__(self):
        whitebox.__init__(self)
    def Render(self):
        whitebox.Render(self)
        label1 = self.font.render("You will be creating buildings in order to acquire resources to create soldiers to attack other kingdom",True,BLACK)
        label2 = self.font2.render("HOW TO PLAY",True,BLACK)
        label3 = self.font.render("Each building is specialized in creating one kind of resources, but also takes resources to sustain",True,BLACK)
        label4 = self.font.render("Each building also costs some resources to build",True,BLACK)
        label5 = self.font.render("Create enough soldiers to attack the other kingdom",True,BLACK)
        label6 = self.font.render("More soldiers means more health points.",True,BLACK)
        screen.blit(label2,(650,200))
        screen.blit(label1,(200,400))
        screen.blit(label3,(200,435))
        screen.blit(label4,(200,470))
        screen.blit(label5,(200,505))
        screen.blit(label6,(200,540))
        screen.blit(cross,(1430,135))
    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Exit")))
class noresource(whitebox):
    def __init__(self):
        whitebox.__init__(self)
    def Render(self):
        whitebox.Render(self)
        label1 = self.font2.render("NOT ENOUGH RESOURCES TO BUILD",True,BLACK)
        screen.blit(label1,(300,450))
        screen.blit(cross,(1430,135))
    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
class Combat(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.font = pygame.font.Font("kenvector_future_thin.ttf",30)
        self.life = armor + 1
        self.turret = 5
    def Render(self):
        screen.fill(BLACK)
        screen.blit(background,(0,0))
        screen.blit(cas,(1300,200))
        label1 = self.font.render("Your Life: "+str(self.life),True,BLACK)

        screen.blit(label1,(50,50))

        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)
        if pygame.sprite.spritecollideany(playered,enemies):
            self.life = self.life -1
        if self.life <= 0:
            self.SwitchToScene(gameover())
        if playered.rect.right == 1600:
            self.SwitchToScene(win())
    def ProcessInputs(self,events,pressed_keys):
        global life
        for event in events:
            if event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        playered.update(pressed_keys)
        enemies.update()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("crown.png").convert()
        self.surf.set_colorkey((255,255,255),pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
    #self.rect is the shape of the player itself. the outline, while surf is the surface drew
    def update(self,pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0,-15)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0,15)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-15,0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(15,0)
    #keep it on the screen:
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 960:
            self.rect.bottom = 960
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 1600:
            self.rect.right = 1600
playered = Player()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("stone.png").convert()
        self.surf.set_colorkey((255,255,255),pygame.RLEACCEL)
        self.rect = self.surf.get_rect(center= (random.randint(1620,1700), random.randint(0,960)))
        self.speed =random.randint(30,50)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(playered)
class gameover(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.font = pygame.font.Font("kenvector_future_thin.ttf",100)
    def Render(self):
        screen.fill(BLUESKY)
        label = self.font.render("GAME OVER", True, RED)
        screen.blit(label,(500,375))

class win(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.font=pygame.font.Font("kenvector_future_thin.ttf",100)
    def Render(self):
        screen.fill(BLUESKY)
        label = self.font.render("YOU WIN", True, RED)
        screen.blit(label,(600,375))
class soon(whitebox):
    def __init__(self):
        whitebox.__init__(self)
    def Render(self):
        whitebox.Render(self)
        label1 = self.font.render("This feature will be coming out soon.",True,BLACK)

        screen.blit(label1,(250,400))

        screen.blit(cross,(1430,135))
    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(Scene2(("Howtoplay","Explore","Invade","Quit")))
class howtoplayed(whitebox):
    def __init__(self):
        whitebox.__init__(self)
    def Render(self):
        whitebox.Render(self)
        label1 = self.font.render("You will be attacking.",True,BLACK)
        label2 = self.font2.render("HOW TO PLAY INVADING",True,BLACK)
        label3 = self.font.render("Dodge the stones coming at you",True,BLACK)
        label4 = self.font.render("The more soldiers you created in the previous scene, the more health points you have during this.",True,BLACK)
        label5 = self.font.render("Survive the wave of stones and move to right side of screen to win the game.",True,BLACK)

        screen.blit(label2,(400,200))
        screen.blit(label1,(200,400))
        screen.blit(label3,(200,435))
        screen.blit(label4,(200,470))
        screen.blit(label5,(200,505))
        screen.blit(cross,(1430,135))

    def ProcessInputs(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 1:
                self.SwitchToScene(Combat())
if __name__ == '__main__':
    main(60,menu)
