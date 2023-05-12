#Reskinned space version of airplane python tutorial game.


import pygame
import random



from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

width = 800
height = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/shipresized.png").convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
            #Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height
            
    #create an enemy object 
    #the surface I draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/missile.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )
        self.speed = random.randint(5, 20)
        
        
        #move sprite based on speed
        #remove sprite when it passes the left edge of window
    def update(self):
        self.rect.move_ip(-self.speed, 0 )
        if self.rect.right < 0 :
            self.kill()
            
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/meteor.png")
        self.surf.set_colorkey((0,0,0), RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )        
        
    def update(self):
        self.rect.move_ip(-10, 0 )
        if self.rect.right < 0 :
            self.kill()
                
                
#Setup for sounds
pygame.mixer.init()
        
pygame.init()

#Setup clock for a decent game speed
clock = pygame.time.Clock()

#Background music
pygame.mixer.music.load("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/space.mp3")
#Add music license
pygame.mixer.music.play(loops=-1)

#move sounds
move_up_sound = pygame.mixer.Sound("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/mixkit-spaceship-large-drone-2742.wav")
move_down_sound = pygame.mixer.Sound("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/mixkit-spaceship-large-drone-2742.wav")
collision_sound = pygame.mixer.Sound("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/Collision.ogg")

#Set entire screen
screen = pygame.display.set_mode((width,height))

#create a custom event for adding a new enemy then add event to event queue where main loop is running
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,  250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

#create the enemy sprite as variable and add to a group.
#add sprite groups to all sprites.
#add player as seperate entity to sprite group

#enemies are collision detection
#all_sprite is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)



running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
            
        #Add a new enemy
        elif event.type == ADDENEMY:
            #Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        #Add a new cloud
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    enemies.update()
    clouds.update()
    
    bg = pygame.image.load("C:/Users/donav/OneDrive/Documents/Scripts/pygame_basics/spacegame/space.png").convert()
    
    screen.blit(bg, (0,0))    
    #screen.fill((135,206,250))
    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
        
        #Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        #If so, then remove the player and stop the loop
        player.kill()
        
        #Stop an moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
                
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        
        running = False

    pygame.display.flip()           
    
    #Ensure program maintains a rate of 30 frames per second
    clock.tick(30) 
            
    