'''
Aquatic Attack

The Purpose of this program is to create a game in which two players will control a Seahorse and a Pufferfish as they duel eachother

Movement
The Pufferfish is controlled by the arrow keys and the Seahorse is controlled by the keys w,a,s and d.
The Pufferfish is faster than the Seahorse but the Seahorse has more manuverability and will need to use this to his advantage in order to win

Attacking
The Pufferfish deals damage to the Seahorse when they come in contact, due to its spikes, however the player can choose to press 0 (on the keypad) to send out its spikes and damage the Seahorse
The Pufferfish however will be deflated and spikeless for a few seconds unable to damage the Seahorse
The Seahorse deals damage by sending out bubbles in the direction he is facing (one at a time) with the space bar
The Seahorse cannot fire a bubble as long as another bubble is already existing, the bubble ability is considered on cooldown.
This means that missing a shot will result in a longer wait until another one can be fired

Powerup
There are several fish that will appear from the right side of the screen. If either player gets eats/touches one of these fish they will receive a damage boost of x2 for a limited duration
The duration of the damage boost will appear either on the top left (Seahorse) or the top right (Pufferfish)

Map
If a player goes off one side of the screen they will come out of the other one, this does not work vertically, if the player touches the top wall or the floor they will stop
The Pufferfish can use the pillar as protection from the Seahorses bubbles because they cannot pass through it

Game end
A round is finshed when one players health reaches 0, at which time the players can start a new round by pressing p or exit the program with Escape
The number of rounds (score) of each player is displayed at the top left and top right of the screen

Citation
Links for all images used not created by Adrian and Timothy will be provided in the comments above where they are loaded
No outside code sources were copied, all code was written by Timothy and Adrian

@Authors Adrian Pasqualini, Timothy Quijano
@Date 6/17/2016
@Course ICS3U1
'''

#Imports
import pygame, sys, os
from pygame.locals import *
import random
import time

#Initialize Pygame funcitons
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

#Assign constant color variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BEIGE = (255, 241, 103)

#Load All Images

#Pufferfish images
#http://forums.terraria.org/index.php?threads/sprites-ocean-expanded-dangerous-depths.5658/
pufferimage_bigright = pygame.image.load('assets/bigpufferfish_right.png')
pufferimage_bigleft = pygame.image.load('assets/bigpufferfish_left.png')
pufferimage_smallleft = pygame.image.load('assets/smallpufferfish_left.png')
pufferimage_smallright = pygame.image.load('assets/smallpufferfish_right.png')
pufferimage_bigright_save = pygame.image.load('assets/bigpufferfish_right.png')
pufferimage_bigleft_save = pygame.image.load('assets/bigpufferfish_left.png')


#Spike images, angle is named as time positions on clock (12 is up, 6 is down, etc.)
#http://worldartsme.com/orange-triangle-clipart.html#gal_post_26604_orange-triangle-clipart-1.jpg
spikeimage12 = pygame.image.load('assets/spike12.png')
spikeimage130 = pygame.image.load('assets/spike130.png')
spikeimage3 = pygame.image.load('assets/spike3.png')
spikeimage430 = pygame.image.load('assets/spike430.png')
spikeimage6 = pygame.image.load('assets/spike6.png')
spikeimage730 = pygame.image.load('assets/spike730.png')
spikeimage9 = pygame.image.load('assets/spike9.png')
spikeimage1030 = pygame.image.load('assets/spike1030.png')

#Seahorse images
#http://insaniquarium.wikia.com/wiki/Zorf
horseimage_right = pygame.image.load('assets/Zorf_the_Seahorse_right.png')
horseimage_left = pygame.image.load('assets/Zorf_the_Seahorse.png')

#Pillar image
#Created using http://www.piskelapp.com/
pillar = pygame.image.load('assets/pillar.png')


#Several powerup fish images
#http://www.dreamstime.com/royalty-free-stock-photo-cartoon-fishes-image14275195
red = pygame.image.load('assets/red_left.png')
blue = pygame.image.load('assets/blue_left.png')
green = pygame.image.load('assets/green_left.png')
orange = pygame.image.load('assets/orange_left.png')
pink = pygame.image.load('assets/pink_left.png')
red = pygame.image.load('assets/red_left.png')
yellow = pygame.image.load('assets/yellow_left.png')
purple = pygame.image.load('assets/purple_left.png')
brown = pygame.image.load('assets/brown_left.png')
bluepink = pygame.image.load('assets/blink_left.png')

#Several different seaweed/kelp images
#Created using http://www.piskelapp.com/
kelp1 = pygame.image.load('assets/kelp1.png')
kelp2 = pygame.image.load('assets/kelp2.png')
kelp3 = pygame.image.load('assets/kelp3.png')

#Coral image
#Created using http://www.piskelapp.com/
coral = pygame.image.load('assets/coral.png')

#Background Image
oceanback = pygame.image.load("assets/background.png")

#Create a list of fish images for the power up fish
fishlist = [red,blue,green,orange,pink,red,yellow,purple,brown,bluepink]




#Set initial player directions
horse_direction = "right"
puffer_direction = "left"

# Set display settings
width = 1440
height = 1440
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Aquatic Attack")

# Variables for moving 
move_right = False
move_left = False
move_up = False
move_down = False
move_right2 = False
move_left2 = False
move_up2 = False
move_down2 = False

#Set default values for variables 
on_cooldown = False
winner = None
matchdone = False

#Variables for the duration of the damage boost for both players
p_powertimer = 0
h_powertimer = 0

#Score for both players
puffer_score = 0
horse_score = 0


#Render several fonts with different sizes
basicsize_font = pygame.font.SysFont("Arial", 35)
instruction_font = pygame.font.SysFont("Arial", 36)
game_end_font = pygame.font.SysFont("Arial", 72)


#Display text for the bubble cooldown
cooldown_text = basicsize_font.render("On Cooldown",1,BLACK)

#Text telling players how to restart or exit the game
instructions = instruction_font.render("Press p to start a new round.                       Press Escape to exit the game.",1,BLACK)


#Declare classes


#Wall class
class Wall(pygame.sprite.Sprite):
    '''
    Create wall with varying x values ,y values, widths, and heights
    @Parameter x int
    @Parameter y int
    @Parameter width int
    @Parameter height int
    @Parameter self
    '''
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface([width,height])        
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
    
#Fish/Player class
class Fish(pygame.sprite.Sprite):
    '''
    Creates the player/fish setting their max and min speed, their damage, their health, and their location
    @Parameter x int
    @Parameter y int
    @Parameter maxspeed int
    @Parameter minspeed int
    @Parameter player int
    @Parameter health int
    @Parameter damage int
    @Parameter self
    '''
    def __init__(self,image,x,y,maxspeed,minspeed,health,player,damage):
        
        pygame.sprite.Sprite.__init__(self)
           
        self.image = image
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y        
        self.x_speed = 0
        self.y_speed = 0
        
        self.maxspeed = maxspeed
        self.minspeed = minspeed        
        self.player = player
        self.hitpoints = health
        self.damage = damage

    '''
    This draws the hitpoints bar underneath the player
    @Parameter self 
    '''
    def update(self):

        #If the player is the Pufferfish then the bar will be larger (ie has more health) and needs to be centered accordingly
        if self.player == 1:

            #Give it a white background
            pygame.draw.rect(screen,WHITE, [self.rect.x-15,self.rect.y+70,100,10],0)

            #If player is below 75 health make the health bar red
            if self.hitpoints<=75:
                    pygame.draw.rect(screen,RED, [self.rect.x-15,self.rect.y+70,self.hitpoints/2.5,10],0)

            #If player is below 150 health make the health bar yellow
            elif self.hitpoints <= 150:
                pygame.draw.rect(screen,YELLOW, [self.rect.x-15,self.rect.y+70,self.hitpoints/2.5,10],0)                           

            #If the player is above 150 health then make the helath bar Green
            else:
                pygame.draw.rect(screen,GREEN, [self.rect.x-15,self.rect.y+70,self.hitpoints/2.5,10],0)

            #Outline the health bar with a hollow black rectangle
            pygame.draw.rect(screen,BLACK, [self.rect.x-15,self.rect.y+70,100,10],1)

        #If the player is the Seahorse then the bar will be smalle (ie has less health) and needs to be centered accordingly
        elif self.player == 2:

            #Give it a white background
            pygame.draw.rect(screen,WHITE, [self.rect.x+5,self.rect.y+80,50,10],0)

            #If player is below 50 health make the health bar red
            if self.hitpoints <= 50:
                pygame.draw.rect(screen,RED, [self.rect.x+5,self.rect.y+80,self.hitpoints/2.5,10],0)

            #If player is below 85 health make the health bar yellow
            elif self.hitpoints <= 85:
                pygame.draw.rect(screen,YELLOW, [self.rect.x+5,self.rect.y+80,self.hitpoints/2.5,10],0)        

            #If the player is above 85 health then make the health bar Green
            else:
                pygame.draw.rect(screen,GREEN, [self.rect.x+5,self.rect.y+80,self.hitpoints/2.5,10],0)

            #Outline the health bar with a hollow black rectangle
            pygame.draw.rect(screen,BLACK, [self.rect.x+5,self.rect.y+80,50,10],1)


#Class for the various spikes
class Spike(pygame.sprite.Sprite):

    '''
    Define the spikes image and Direction
    @Parameter self
    '''
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = spikeimage12
        self.rect = self.image.get_rect()

        self.direction = " "

    '''
    Based on the direction, determine how the spike will move
    @Parameter self
    '''
    def update(self):

        #If spike is facing up, move spike up
        if self.direction == "12":
            self.rect.y -= 30

        #If spike is facing up and right, move spike up and right
        if self.direction == "130":
            self.rect.x += 30
            self.rect.y -= 30

        #If spike is facing right, move spike left
        if self.direction == "3":
            self.rect.x += 30

        #If spike is facing down and right, move spike down and right
        if self.direction == "430":
            self.rect.x += 30
            self.rect.y += 30

        #If spike is facing down, move spike down
        if self.direction == "6":
            self.rect.y += 30

        #If spike is facing down and left, move spike down and left
        if self.direction == "730":
            self.rect.x -= 30
            self.rect.y += 30

        #If spike is facing left, move spike left
        if self.direction == "9":
            self.rect.x -= 30

        #If spike is facing up and left, move spike up and left
        if self.direction == "1030":
            self.rect.x -= 30
            self.rect.y -= 30 


#Bubble Class
class Bubble(pygame.sprite.Sprite):

    '''
    Defines bubble image and direction
    @Parameter direction  string
    @Parameter self
    '''
    def __init__(self,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/bubble.png')
        self.rect = self.image.get_rect()
        self.direction = direction

    '''
    Determines how the bubble will move based on its direction
    @Parameter self
    '''
    def update(self):

        #If the seahorse was moving right when the bubble is shot, move the bubble right
        if self.direction=="right":         
            self.rect.x += 40                                    

        #If the seahorse was moving left when the bubble is shot, move the bubble left       
        if self.direction=="left":
            self.rect.x -= 40


#Powerup Class
class Powerup(pygame.sprite.Sprite):

    '''
    Define the fish image this power up will be, and its location
    @Parameter self
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=fishlist[random.randrange(0,9)]
        
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = random.randrange(0,height-250)

    '''
    The powerup fish will move left across the screen
    @Parameter self
    '''
    def update(self):
        self.rect.x -= 7.5



#Pillar sprite class, the pillar sprite cannot be made from the image itself due to the base of the pillar making the hitbox too wide and inaccurate
class Pillar(pygame.sprite.Sprite):

    '''
    Define the pillar sprites width, height, and location
    @Parameter x int
    @Parameter y int
    @Parameter self
    '''
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([65,300])        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

'''
Draw 3 corals across the screen
@Parameter coral.png  image
'''
def coraldraw(coral):
    #Offset each coral by 450 pixels
    for x_offset in range(0,1350,450):
        screen.blit(coral,(x_offset,height-350))



'''
Draw the background, including the coral, the sand, the pillar, and the seaweed/kelp
@Parameter coral.png  image (png)
@Parameter height     int
@Parameter BEIGE      list
'''
def background_draw(coral,height,BEIGE):
    coraldraw(coral)
    pygame.draw.rect(screen, BEIGE, (0, height-150, 1440, 150),0)
    screen.blit(kelp1, (25, height-260))
    screen.blit(kelp2, (1200, height-260))
    screen.blit(kelp3, (800, height-260))       
    screen.blit(pillar,(350,height-398))   
    
    
    
'''
Draw the score text, the power bar for each player, the power bar title, and the "on cooldown" text
'''
def game_displays():
    #If the bubble ability is on cooldown and the player tries to fire it then display text indicating to them that the ability is unavailable
    if on_cooldown==True:
        screen.blit(cooldown_text, (horse.rect.x-70, horse.rect.y+95))

    #Power bar timer for both players
    pygame.draw.rect(screen,WHITE, [50,20,300,25],0)
    pygame.draw.rect(screen,WHITE, [1100,20,300,25],0)
    pygame.draw.rect(screen,BLACK, [50,20,300,25],1)
    pygame.draw.rect(screen,BLACK, [1100,20,300,25],1)
    pygame.draw.rect(screen,(255,165,0), [1100,20,p_powertimer,25],0)  
    pygame.draw.rect(screen,(255,165,0), [50,20,h_powertimer,25],0)

    #Title above both power bar timers
    screen.blit(text[1],(1075,50))
    screen.blit(text[2],(40,50))

    #Score for both players
    screen.blit(text[3],(800,15))
    screen.blit(text[4],(360,15))




#Take Screenshot of the current game state
def take_screenshot(screen):
    time_taken = time.asctime(time.localtime(time.time()))
    time_taken = time_taken.replace(" ", "_")
    time_taken = time_taken.replace(":", ".")
    save_file = "screenshots/" + time_taken + ".png"
    pygame.image.save(screen, save_file)
    print("Screenshot Taken")



#Create Object instances
puffer = Fish(pufferimage_bigleft,900,600,20,-20,250,1,1.5)
horse = Fish(horseimage_right,400,600,15,-15,125,2,25)
bubble=Bubble(horse_direction)
wall_left = Wall(-130,0,40,height)
wall_right = Wall(width+147,0,40,height)
wall_up = Wall(0,-5,width,5)
wall_down = Wall(0,height-150,width,5)
damageboost = Powerup()
pillar_sprite = Pillar(420,height-398)

#Create sprite groups
walls = pygame.sprite.Group()
player1 = pygame.sprite.GroupSingle()
player2 = pygame.sprite.GroupSingle()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bubble_list = pygame.sprite.Group()
spike_list = pygame.sprite.Group() 
pillar_group = pygame.sprite.GroupSingle()

#Add instances to groups
player1.add(puffer)
player2.add(horse)
powerups.add(damageboost)
walls.add(wall_left,wall_right,wall_down,wall_up,pillar_sprite)
all_sprites.add(puffer,horse,damageboost)
pillar_group.add(pillar_sprite)




# <<-----------Main Loop------------>>

#Set variable to use to check when to exit the main loop
done = False 
while not done:

    # Process all events 
    for event in pygame.event.get():

        #End game if window is closed
        if event.type == pygame.QUIT: 
            done = True

        #Process all keys pressed down events     
        if event.type == pygame.KEYDOWN:

            #End game if Escape is pressed
            if event.key == pygame.K_ESCAPE:
                done=True

                
            #Take screenshot if f is pressed
            if event.key == pygame.K_t:
                    take_screenshot(screen)
                    
            #If p is pressed reset the game, both players are reverted to their initial states
            if event.key == pygame.K_p:
                player1.remove(puffer)
                player2.remove(horse)
                all_sprites.remove(puffer,horse)
                puffer = Fish(pufferimage_bigleft,900,600,20,-20,250,1,1.5)
                horse = Fish(horseimage_right,400,600,15,-15,125,2,25)
                player1.add(puffer)
                player2.add(horse)
                all_sprites.add(puffer,horse)
                p_powertimer = 0
                h_powertimer = 0
                horse_direction="right"
                puffer_direction="left"
                smallpuffer_timer = 0

                #Allow key controls to work again because a new match has started
                matchdone = False

        #Only allow the players to control the characters if the match isnt done
        if matchdone == False:

            #Process all keys pressed down events  
            if event.type == pygame.KEYDOWN:


                # Player 1's controls

                #If the player presses the up arrow key, recognize that he is moving up (Through making the variable True)
                if event.key == pygame.K_UP:
                    move_up=True

                #If the player presses the down arrow key, recognize that he is moving down (Through making the variable True)    
                if event.key == pygame.K_DOWN:
                    move_down = True

                #If the player presses the right arrow key, recognize that he is moving right (Through making the variable True, and another direction variable to determine which image to display (left or right))
                if event.key == pygame.K_RIGHT:
                    move_right = True
                    puffer_direction = "right"

                #If the player presses the left arrow key, recognize that he is moving left (Through making the variable True and another direction variable to determine which image to display (left or right))
                if event.key == pygame.K_LEFT:                     
                    move_left = True
                    puffer_direction = "left"
                    

                # Player 2's controls

                #If the player presses w, recognize that he is moving up (Through making the variable True)
                if event.key == pygame.K_w:
                    move_up2 = True

                #If the player presses s, recognize that he is moving down (Through making the variable True)
                if event.key == pygame.K_s:
                    move_down2 = True

                #If the player presses d, recognize that he is moving right (Through making the variable True and another direction variable to determine which image to display
                #and which direction the bubble travels(left or right))
                if event.key == pygame.K_d:
                    move_right2 = True                 
                    horse_direction = "right"

                #If the player presses a, recognize that he is moving left (Through making the variable True and another direction variable to determine which image to display
                #and which direction the bubble travels(left or right))
                if event.key == pygame.K_a:                     
                    move_left2 = True
                    horse_direction = "left"

                #If the Seahorse player presses the space bar fire a bubble
                if event.key == pygame.K_SPACE:
                    

                    #Ensures that Seahorse can only shoot one bubble at a time
                    if len(bubble_list) == 0:

                        #If the Seahorse is moving right, the bubble will travel right
                        if horse_direction == "right":
                            bubble = Bubble("right")

                            #Spawn bubble at the right spot on the Seahorse's nose
                            bubble.rect.x = horse.rect.x+55

                        #If the Seahorse is moving left, the bubble will travel left   
                        elif horse_direction == "left":
                            bubble = Bubble("left")

                            #Spawn bubble at the right spot on the Seahorse's nose
                            bubble.rect.x = horse.rect.x-10

                        #Spawn bubble at the right spot on the Seahorse's nose
                        bubble.rect.y = horse.rect.y+20
                        bubble_list.add(bubble)
                        
                    #If there is already a bubble on the screen then this ability is "on cooldown" and appropriate text will display to show this    
                    else:                                      
                        on_cooldown=True

                #If a player presses the keypad 0 then 8 spikes will fire from  the puffer fish
                if event.key == pygame.K_0:

                    #If the Pufferfish is still small/deflated then they cannot use this ability
                    if pufferimage_bigright != pufferimage_smallright:

                        #Ability only available if no other spikes are exitsing
                        if len(spike_list) == 0:

                            #Create 8 different spikes with different directions
                            
                            spike12 = Spike()
                            spike12.direction = "12" 
                            spike12.image = spikeimage12
                            #Spawn the spike in the correct location
                            spike12.rect.x = puffer.rect.x + 30
                            spike12.rect.y = puffer.rect.y - 35

                            spike130 = Spike()
                            spike130.direction = "130" 
                            spike130.image = spikeimage130
                            #Spawn the spike in the correct location
                            spike130.rect.x = puffer.rect.x + 35
                            spike130.rect.y = puffer.rect.y - 14

                            spike3 = Spike()
                            spike3.direction = "3" 
                            spike3.image = spikeimage3
                            #Spawn the spike in the correct location
                            spike3.rect.x = puffer.rect.x + 30
                            spike3.rect.y = puffer.rect.y + 10

                            spike430 = Spike()
                            spike430.direction = "430" 
                            spike430.image = spikeimage430
                            #Spawn the spike in the correct location
                            spike430.rect.x = puffer.rect.x + 25
                            spike430.rect.y = puffer.rect.y + 25

                            spike6 = Spike()
                            spike6.direction = "6" 
                            spike6.image = spikeimage6
                            #Spawn the spike in the correct location
                            spike6.rect.x = puffer.rect.x + 25
                            spike6.rect.y = puffer.rect.y + 25

                            spike730 = Spike()
                            spike730.direction = "730" 
                            spike730.image = spikeimage730
                            #Spawn the spike in the correct location
                            spike730.rect.x = puffer.rect.x + 15
                            spike730.rect.y = puffer.rect.y + 15

                            spike9 = Spike()
                            spike9.direction = "9" 
                            spike9.image = spikeimage9
                            #Spawn the spike in the correct location
                            spike9.rect.x = puffer.rect.x + 15
                            spike9.rect.y = puffer.rect.y + 20

                            spike1030 = Spike()
                            spike1030.direction = "1030" 
                            spike1030.image = spikeimage1030
                            #Spawn the spike in the correct location
                            spike1030.rect.x = puffer.rect.x + 15
                            spike1030.rect.y = puffer.rect.y + 15

                        #Add all the spikes to a sprite group
                        spike_list.add(spike12,spike130,spike3,spike430,spike6,spike730,spike9,spike1030)

                        #Create a timer variable for how long the pufferfish will be small/deflated
                        smallpuffer_timer = 200
                

                        

            #Process all keys pressed up events     
            if event.type == pygame.KEYUP:


                #Player 1's controls

                #If the right arrow key is released, recognized that the player is no longer moving right 
                if event.key == pygame.K_RIGHT:                
                    move_right = False

                    #Slow down the player to simulate movement in water
                    puffer.x_speed = puffer.x_speed/1.2

                #If the left arrow key is released, recognized that the player is no longer moving left   
                if event.key == pygame.K_LEFT:
                    move_left = False

                    #Slow down the player to simulate movement in water
                    puffer.x_speed = puffer.x_speed/1.2

                #If the up arrow key is released, recognized that the player is no longer moving up 
                if event.key == pygame.K_UP:
                    move_up=False

                    #Slow down the player to simulate movement in water
                    puffer.y_speed = puffer.y_speed/1.2

                #If the down arrow key is released, recognized that the player is no longer moving down 
                if event.key == pygame.K_DOWN:
                    move_down = False

                    #Slow down the player to simulate movement in water
                    puffer.y_speed = puffer.y_speed/1.2


                # Player 2's controls

                #If the d key is released, recognize that the player is no longer moving right 
                if event.key == pygame.K_d:                
                    move_right2 = False

                    #Slow down the player to simulate movement in water
                    horse.x_speed = horse.x_speed/1.2

                #If the a key is released, recognize that the player is no longer moving left  
                if event.key == pygame.K_a:
                    move_left2=False

                    #Slow down the player to simulate movement in water
                    horse.x_speed = horse.x_speed/1.2

                #If the w key is released, recognize that the player is no longer moving up   
                if event.key == pygame.K_w:
                    move_up2 = False

                    #Slow down the player to simulate movement in water
                    horse.y_speed = horse.y_speed/1.2

                #If the s key is released, recognize that the player is no longer moving down    
                if event.key == pygame.K_s:
                    move_down2 = False

                    #Slow down the player to simulate movement in water
                    horse.y_speed = horse.y_speed/1.2

                #If the space bar is released, stop displaying the "cooldown" text   
                if event.key == pygame.K_SPACE:
                    on_cooldown = False
    
#Movement Effects for Player 1

    #If no movement keys are being pressed slow the player to an eventual stop
    if move_right == False and move_left == False:        
        puffer.x_speed = puffer.x_speed/1.1      

    #If no movement keys are being pressed slow the player to an eventual stop
    if move_up == False and move_down == False:
        puffer.y_speed=puffer.y_speed/1.1

    #Reduces x speed by a hard value for quicker stops, solves a bug where players would drift forever
    if puffer.x_speed < 0:
        puffer.x_speed += 0.025
        
    #Reduces y speed by a hard value for quicker stops, solves a bug where players would drift forever
    if puffer.y_speed < 0:
        puffer.y_speed += 0.025
        
    #Move the players x and y values based on the x and y accelerations
    puffer.rect.x += puffer.x_speed
    puffer.rect.y += puffer.y_speed

    
    
    #If the players x acceleration is greater than the max speed, set it to the max speed
    if puffer.x_speed > puffer.maxspeed: 
        puffer.x_speed = puffer.maxspeed

    #If the players x acceleration is less than the minimum speed, set it to the minimum speed    
    if puffer.x_speed < puffer.minspeed: 
        puffer.x_speed = puffer.minspeed

    #If the players y acceleration is greater than the max speed, set it to the max speed   
    if puffer.y_speed > puffer.maxspeed: 
        puffer.y_speed = puffer.maxspeed

    #If the players y acceleration is less than the minimum speed, set it to the minimum speed   
    if puffer.y_speed < puffer.minspeed: 
        puffer.y_speed = puffer.minspeed

    #If player is moving right, increase the x acceleration    
    if move_right == True:           
        puffer.x_speed += 1    

    #If player is moving left, decrease the x acceleration 
    if move_left == True:                      
        puffer.x_speed -= 1
        
    #If player is moving up, decrease the y acceleration
    if move_up == True:
        puffer.y_speed -= 1    

    #If player is moving down, increase the y acceleration 
    if move_down == True:
        puffer.y_speed += 1


#Movement Effects for Player 2    
    
    #If no movement keys are being pressed slow the player to an eventual stop
    if move_right2 == False and move_left2 == False:
        horse.x_speed = horse.x_speed/1.1

    #If no movement keys are being pressed slow the player to an eventual stop
    if move_up2 == False and move_down2 == False:
        horse.y_speed=horse.y_speed/1.1

    #Reduces speed by a hard value for quicker stops, solves a bug where players would drift forever
    if horse.x_speed < 0:
        horse.x_speed += 0.025
    if horse.y_speed < 0:        
        horse.y_speed += 0.025
    
    #Move the players x and y values based on the x and y accelerations
    horse.rect.x += horse.x_speed        
    horse.rect.y += horse.y_speed    
    
    #If the players x acceleration is greater than the max speed, set it to the max speed
    if horse.x_speed > horse.maxspeed: 
        horse.x_speed = horse.maxspeed 

    #If the players x acceleration is less than the minimum speed, set it to the minimum speed
    if horse.x_speed < horse.minspeed: 
        horse.x_speed = horse.minspeed 

    #If the players y acceleration is greater than the max speed, set it to the max speed
    if horse.y_speed > horse.maxspeed: 
        horse.y_speed = horse.maxspeed
    
    #If the players y acceleration is less than the minimum speed, set it to the minimum speed
    if horse.y_speed < horse.minspeed: 
        horse.y_speed = horse.minspeed
        
    #If player is moving right, increase the x acceleration  
    if move_right2 == True:           
        horse.x_speed += 2   

    #If player is moving left, decrease the x acceleration
    if move_left2 == True:                      
        horse.x_speed -= 2    

    #If player is moving up, decrease the y acceleration
    if move_up2 == True:
        horse.y_speed -= 2    

    #If player is moving down, increase the y acceleration 
    if move_down2 == True:
        horse.y_speed += 2



    #If the Seahorse is moving right, display the Seahorse facing right
    if horse_direction == "right":
        horse.image = horseimage_right

    #If the Seahorse is moving left, display the Seahorse facing left
    elif horse_direction == "left":
        horse.image = horseimage_left

    #If the puffer is moving right, display the puffer facing right
    if puffer_direction == "right":
        puffer.image = pufferimage_bigright

    #If the puffer is moving left, display the puffer facing left
    elif puffer_direction == "left":
        puffer.image = pufferimage_bigleft 
    
   
#Collision Detection

    
    #Detect collisions between the Pufferfish and the bubble    
    bubble_collide_list = pygame.sprite.spritecollideany(puffer, bubble_list)

    #If there is a collision, deal the appropriate damage to the Pufferfish and remove the bubble from all sprite groups   
    if bubble_collide_list != None:            
        puffer.hitpoints -= horse.damage
        bubble.kill()

    #Only check for collisions if spikes have been created
    if len(spike_list)!= 0:

        #Detect collisions between the Seahorse and the spikes
        spike_collide_list = pygame.sprite.spritecollideany(horse, spike_list)

        #If the spike moving upwards hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike12:
            horse.hitpoints -= 20
            spike12.kill()

        #If the spike moving upwards and right hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike130:            
            horse.hitpoints -= 20
            spike130.kill()            

        #If the spike moving right hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike3:            
            horse.hitpoints -= 20
            spike430.kill()

        #If the spike moving downwards and right hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike430:            
            horse.hitpoints -= 20
            spike12.kill()

        #If the spike moving downwards hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike6:            
            horse.hitpoints -= 20
            spike6.kill()

        #If the spike moving downwards and left hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike730:            
            horse.hitpoints -= 20
            spike730.kill()

        #If the spike moving left hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike9:            
            horse.hitpoints -= 20
            spike9.kill()

        #If the spike moving upwards and left hits the seahorse, remove the spike from all groups and deal the appropriate damage 
        if spike_collide_list == spike1030:            
            horse.hitpoints -= 20
            spike1030.kill()

        #While the timer is greater than 0 the pufferfish is small 
        if smallpuffer_timer >= 0:

            pufferimage_bigright = pufferimage_smallright
            pufferimage_bigleft = pufferimage_smallleft

            #Count down (reduce the value) of the timer
            smallpuffer_timer -= 2

            #Pufferfish cannot deal any damage while small
            puffer.damage = 0

        #If the timer isn't greater than 0 then the Pufferfish reverts to normal
        else:
            pufferimage_bigright = pufferimage_bigright_save
            pufferimage_bigleft = pufferimage_bigleft_save
            puffer.damage = 1.5

            #All the spikes are removed from the spike group
            for spike in spike_list:
                spike_list.remove(spike)
            


    #Collision detection for the Pufferfish and all the walls
    wall_collide_list1 = pygame.sprite.spritecollideany(wall_left,player1)
    wall_collide_list2 = pygame.sprite.spritecollideany(wall_right,player1)
    wall_collide_list3 = pygame.sprite.spritecollideany(wall_down,player1)
    wall_collide_list4 = pygame.sprite.spritecollideany(wall_up,player1)

    #Collision detection for the Seahorse and all the walls
    wall_collide_list5 = pygame.sprite.spritecollideany(wall_left,player2)
    wall_collide_list6 = pygame.sprite.spritecollideany(wall_right,player2)
    wall_collide_list7 = pygame.sprite.spritecollideany(wall_down,player2)
    wall_collide_list8 = pygame.sprite.spritecollideany(wall_up,player2)
    
    #Collision detection for the bubble and all the walls
    wall_collide_list_bubble = pygame.sprite.spritecollideany(bubble,walls)

    #Collision detection for the Pufferfish and the seahorse
    player_collide_list = pygame.sprite.spritecollideany(puffer,player2)

    #Collision detection for the Powerup with both players and the walls
    powerup_puffercollide_list = pygame.sprite.spritecollideany(damageboost,player1)
    powerup_horsecollide_list = pygame.sprite.spritecollideany(damageboost,player2)
    wall_powerup_collide_list = pygame.sprite.spritecollideany(wall_left,powerups)
    
    
    #If the Pufferfish collides with the left wall, move it to the opposite side of the screen           
    if wall_collide_list1 == puffer:
        puffer.rect.x = width

    #If the Pufferfish collides with the right wall, move it to the opposite side of the screen 
    if wall_collide_list2 == puffer:
        puffer.rect.x = -109

    #If the Pufferfish collides with the bottom wall, stop it there
    if wall_collide_list3 == puffer:
        puffer.rect.y = height-212
        puffer.y_speed = 0  


    #If the Pufferfish collides with the top wall, stop it there
    if wall_collide_list4 == puffer:
        puffer.rect.y = 0
        puffer.y_speed = 0    

    #If the Seahorse collides with the left wall, move it to the opposite side of the screen   
    if wall_collide_list5 == horse:
        horse.rect.x = width

    #If the Seahorse collides with the right wall, move it to the opposite side of the screen
    if wall_collide_list6 == horse:
        horse.rect.x = -89

    #If the Seahorse collides with the bottom wall, stop it there
    if wall_collide_list7 == horse:
        horse.rect.y = height-150-75
        horse.y_speed = 0 

    #If the Seahorse collides with the top wall, stop it there
    if wall_collide_list8 == horse:
        horse.rect.y = 0
        horse.y_speed = 0

    #If the powerup fish collides with the Pufferfish, reset its location to past the right side of the screen at a random y value with a different image, and set the timer for the damage boost
    if powerup_puffercollide_list == puffer:
        damageboost.rect.x = width+1500
        damageboost.rect.y = random.randrange(0,height-250)
        p_powertimer = 300
        damageboost.image = fishlist[random.randrange(0,9)]
        
    #If the powerup fish collides with the Seahorse, reset its location to past the right side of the screen at a random y value with a different image, and set the timer for the damage boost
    if powerup_horsecollide_list == horse:
        damageboost.rect.x = width+1500
        damageboost.rect.y = random.randrange(0,height-250)
        h_powertimer = 300
        damageboost.image = fishlist[random.randrange(0,9)]

    #If the powerup fish collides with the left wall, reset its location to past the right side of the screen at a random y value with a different image
    if wall_powerup_collide_list != None:
        damageboost.rect.x = width+1500
        damageboost.rect.y = random.randrange(0,height-250)
        damageboost.image = fishlist[random.randrange(0,9)]

    #If the bubble collides with the wall remove it from all groups  
    if wall_collide_list_bubble != None:
        bubble.kill()

    #This statements ensures that if the Pufferfish dies ontop of the seahorse it will not continue to deal damage to it after the match has ended
    if matchdone==False:
    
        #If the Pufferfish is colliding with the Seahorse then the seahorse takes damage
        if player_collide_list != None:
            horse.hitpoints -= puffer.damage
        
    #If the timer for the damageboost has not ended then double the damage the player deals
    if p_powertimer > 0:
        puffer.damage = 3
        #Make the timer count down
        p_powertimer -= 1.5
        
    #If the timer is finished revert the players damage to normal
    else:
        puffer.damage = 1.5
        
    #If the timer for the damageboost has not ended then double the damage the player deals
    if h_powertimer > 0:        
        horse.damage = 50
        #Make the timer count down
        h_powertimer -= 1.5
        
    #If the timer is finished revert the players damage to normal
    else:
        horse.damage = 25


    
        


#Game end Mechanics 

    #Checks if Pufferfish has ran out of HP
    if puffer.hitpoints <= 0:        
        winner = "SeaHorse!"
        puffer.hitpoints = 0

        #This if statements ensures that the score is only changed once instead of it happening continuously with the main program loop
        if matchdone == False:
            horse_score += 1

        #Enter the "Match Finished" state
        matchdone = True

    #Checks if Seahorse has ran out of HP
    if horse.hitpoints <= 0:
        winner = "Pufferfish!"
        horse.hitpoints = 0

        #This if statements ensures that the score is only changed once instead of it happening continuously with the main program loop
        if matchdone == False:
            puffer_score += 1

        #Enter the "Match Finished" state
        matchdone = True



    #Create/Update all needed texts, e.g. Game over, The score, and the winner 
    game_end_text = game_end_font.render("Game Over! The Winner is "+str(winner),1,BLACK)
    power_puffer = basicsize_font.render("Pufferfish Damage x2",1,BLACK)
    power_horse = basicsize_font.render("Seahorse Damage x2",1,BLACK)
    puffer_score_text = basicsize_font.render("Pufferfish Score: "+str(puffer_score),1,BLACK)
    horse_score_text = basicsize_font.render("Seahorse Score: "+str(horse_score),1,BLACK)
    #Create list for the updated texts
    text=[game_end_text,power_puffer,power_horse,puffer_score_text,horse_score_text]


    screen.fill((3,183,255))
    screen.blit(oceanback,(0, 0))

    #Draw Background
    background_draw(coral,height,BEIGE)

    #Draw and update sprite groups
    spike_list.draw(screen)
    spike_list.update()
    
    all_sprites.update()
    all_sprites.draw(screen)
    
    bubble_list.draw(screen)
    bubble_list.update()

            
    
    #If the match is over display the neccessary results and instruction text as well as stop all players from moving
    if matchdone == True:
        screen.blit(text[0], (100,200))
        screen.blit(instructions, (150,400))

        puffer.y_speed = 0
        puffer.x_speed = 0
        horse.x_speed = 0
        horse.y_speed = 0
        move_right = False
        move_left = False
        move_up = False
        move_down = False
        move_right2 = False
        move_left2 = False
        move_up2 = False
        move_down2 = False

    #Display the score, damageboost timer bar, and all necessary game text or picture displays
    game_displays()

    #Update the screen with everything that has been drawn
    pygame.display.flip()



    #Set the tick rate
    clock.tick(20)
#Exit the program    
pygame.quit()


