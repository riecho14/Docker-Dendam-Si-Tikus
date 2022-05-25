from abc import ABC, abstractmethod
import pygame
import random
import os
import json

FPS = 60
WIDTH = 500
HEIGHT = 600

BLACK = (0,0,0)
TEXT = (32,32,32)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW =(255,255,0)

#Set up awal dan pembuatan gamed
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img = pygame.image.load("head.png")
pygame.display.set_icon(img)
pygame.display.set_caption("Dendam si Tikus")
clock = pygame.time.Clock()

#Pemuatan gambar
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
mouse_img1 = pygame.image.load(os.path.join("img","mouse1.png")).convert_alpha()
mouse_img2 = pygame.image.load(os.path.join("img","mouse2.png")).convert_alpha()
mouse_mini_img1 = pygame.transform.scale(mouse_img1,(14,34))
mouse_mini_img1.set_colorkey(BLACK)
mouse_mini_img2 = pygame.transform.scale(mouse_img2,(14,34))
mouse_mini_img2.set_colorkey(BLACK)
poison_img = pygame.image.load(os.path.join("img","poison.png")).convert_alpha()
cat_imgs = []
for i in range(7): 
    cat_imgs.append(pygame.image.load(os.path.join("img",f"cat{i}.png")).convert_alpha())
expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["mouse"] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img,(30,30)))
    mouse_expl_img = pygame.image.load(os.path.join("img",f"mouse_expl{i}.png")).convert()
    mouse_expl_img.set_colorkey(BLACK)
    expl_anim["mouse"].append(mouse_expl_img)
power_imgs = {}
power_imgs["shield"] = pygame.image.load(os.path.join("img","shield.png")).convert_alpha()   
power_imgs["gun"] = pygame.image.load(os.path.join("img","gun.png")).convert_alpha() 

#Pemuatan suara
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.3)

font_name = os.path.join("font.otf") 

score = 0

def character_selection():
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    draw_text(screen,"Pilih Karakter Kamu",30,WIDTH/2,HEIGHT/10)

    #Posisi gambar mouse1
    x1 = 65
    y1 = 150
    player_img1 = pygame.image.load(os.path.join("img","mouse1_select.png")).convert_alpha()
    screen.blit(player_img1, (x1,y1))
    draw_text(screen, "Mouse 1", 24, WIDTH/4.5, HEIGHT*0.65)
    draw_text(screen,"HP : 100",18,WIDTH/4.5,HEIGHT*0.70)
    draw_text(screen,"LIVES : 3",18,WIDTH/4.5,HEIGHT*0.75)

    #Posisi gambar mouse2
    x2 = 320
    y2 = 150
    player_img2 = pygame.image.load(os.path.join("img","mouse2_select.png")).convert_alpha()
    screen.blit(player_img2, (x2,y2))
    draw_text(screen, "Mouse 2", 24, WIDTH/1.3, HEIGHT*0.65)
    draw_text(screen,"HP : 150",18,WIDTH/1.3,HEIGHT*0.70)
    draw_text(screen,"LIVES : 2",18,WIDTH/1.3,HEIGHT*0.75)

    pygame.display.flip()
    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set posisi x, y pemilihan karakter
                x1, y1 = event.pos
                if player_img1.get_rect().collidepoint(x1-65, y1-150):
                    players = "1"
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set posisi x, y pemilihan karakter
                x2, y2 = event.pos
                if player_img2.get_rect().collidepoint(x2-320, y2-150):
                    players = "2"
                    running = False
    return(players)

def lose():
    with open('Data/topScore.json') as dat:
        data = json.load(dat)
    topScore = data['TopScore']

    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    draw_text(screen,"Game Over!",60,WIDTH/2,HEIGHT/4)
    draw_text(screen,"Nilai Tertinggi: " + str(topScore),15,WIDTH/2,HEIGHT/4+70)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_q:
                    waiting = False
                    pygame.quit()

def draw_text(surf, text ,size ,x ,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True, TEXT)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def new_cat():
    r = cat()
    all_sprites.add(r)
    cats.add(r)

def draw_score(surf, text ,size ,x ,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def draw_header():
    BG_LENGTH = 1000
    BG_HEIGHT = 50
    fill_rect = pygame.Rect(0,0,BG_LENGTH,BG_HEIGHT)
    pygame.draw.rect(screen,TEXT,fill_rect)

def draw_health1(surf,hp,x,y): 
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100 
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH 
    outline_rect =pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT )
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_health2(surf,hp,x,y): 
    if hp < 0:
        hp = 0
    BAR_LENGTH = 150 
    BAR_HEIGHT = 10
    fill = (hp/150)*BAR_LENGTH 
    outline_rect =pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT )
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,lives, img, x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)

def draw_init():
    
    with open('Data/topScore.json') as dat:
        data = json.load(dat)
    topScore = data['TopScore']

    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    draw_text(screen,"Dendam Si Tikus",40,WIDTH/2,HEIGHT/4)
    draw_text(screen,"Nilai Tertinggi: " + str(topScore),15,WIDTH/2,HEIGHT/3)
    draw_text(screen,'Tekan ARROW KEY atau A D untuk bergerak',13,WIDTH/2,HEIGHT/2)
    draw_text(screen, 'Tekan SPASI atau LEFT MOUSE BUTTON untuk menembak', 13, WIDTH/2, HEIGHT/1.87)
    draw_text(screen,"Tekan apa saja untuk memulai permainan",15,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def pause():
    paused = True

    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    draw_text(screen, "Pause", 35, WIDTH/2, HEIGHT/3)
    draw_text(screen, "Tekan C Untuk Resume", 20, WIDTH/2, HEIGHT/3+70)
    draw_text(screen, "Tekan Q untuk keluar", 20, WIDTH/2, HEIGHT/3+97)
    pygame.display.update()

    clock.tick(FPS)
    while paused:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    lose()


def uploadScore():
    with open('Data/topScore.json') as dat:
        data = json.load(dat)
    topScore = data['TopScore']

    if(score > topScore):
        x = {
            "TopScore": score
        }
        a_file = open("Data/topScore.json", "r")
        json_object = json.load(a_file)
        json_object["TopScore"] = score

        timpah = open("Data/topScore.json", "w")
        json.dump(json_object, timpah)

#class utama
class Mouse(pygame.sprite.Sprite, ABC):
    def __init__(self):
        # set sprite mouse
        pygame.sprite.Sprite.__init__(self)
        self.speedx = 8
        self.gun = 1
        self.gun_time = 0

    #polimorphism
    # dijalankan per frame update
    def update(self):
        # variabel untuk menentukan timing
        now = pygame.time.get_ticks()
        
        # timing tembakan
        if self.gun > 1 and now  - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now 

        # respawn mouse ketika hiiden dan beri delay untuk respawn
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # baca inputan keyboard
        Key_pressed = pygame.key.get_pressed()

        # ketika klik d atau panah kanan pada keyboard rect.x akan ditambah dan mouse akan ke arah kanan,
        # ketika klik a atau panah kiri mouse akan bergerak sebaliknya
        if Key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if Key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx 
        if Key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if Key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx 
        
        # ini untuk membatasi pergerakan agar tidak melewati layar,
        # ketika rect mouse melewati lebar layar rect kanan akan di set sesuai lebar
        # dan rect kiri di set 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):

        # validasi agar mouse tidak bisa menembak ketika mati
        if not(self.hidden):

            # banyaknya tembakan
            if self.gun == 1:
                poison = Poison(self.rect.centerx, self.rect.top)
                all_sprites.add(poison)  
                poisons.add(poison)
                shoot_sound.play()
            elif self.gun >=2: 
                poison1 = Poison(self.rect.left, self.rect.centery)
                poison2 = Poison(self.rect.right, self.rect.centery)
                all_sprites.add(poison1)  
                all_sprites.add(poison2) 
                poisons.add(poison1)
                poisons.add(poison2)
                shoot_sound.play() 

    # set ketika mouse mati
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    # upgrade tembakan, abstract method
    @abstractmethod
    def gun_up(self):
        pass

#mewarisi class utama Mouse
class Mouse1(Mouse):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mouse_img1, (31,73))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() 
        self.radius = 20
        
        # set property2 posisi darah dll pada mouse di game
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.__health = 100 
        self.__lives = 3
        self.hidden = False
        self.hide_time = 0 
        self.gun = 1
        self.gun_time = 0

    #abstract method
    def gun_up(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

#mewarisi class utama Mouse
class Mouse2(Mouse):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mouse_img2, (31,73))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() 
        self.radius = 20
        
        # set property2 posisi darah dll pada mouse di game
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.__health = 150 
        self.__lives = 2
        self.hidden = False
        self.hide_time = 0 
        self.gun = 1
        self.gun_time = 0

    #abstract method
    def gun_up(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class cat(pygame.sprite.Sprite):
    def __init__(self):
        # set sprite kucing
        pygame.sprite.Sprite.__init__(self) 
        self.image_ori = random.choice(cat_imgs)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)     
        
        # set radius putaran random kucing di awal
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,7)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-1,5) 

    # set radius putaran random kucing di update
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    #polimorphism
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx 

        # set posisi kucing + validasi
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            
            # Set kecepatan speed y setiap score bertambah
            kecepatanDinamis = int(score / 100)
            if kecepatanDinamis >= 23:
                kecepatanDinamis = 23
            elif kecepatanDinamis < 4:
                kecepatanDinamis = 4

            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(kecepatanDinamis - 3, kecepatanDinamis)
            self.speedx = random.randrange(-3,3)

            print(kecepatanDinamis)

class Poison(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self) 
            self.image = poison_img
            self.rect = self.image.get_rect()
            self.rect.centerx = x 
            self.rect.bottom = y
            self.speedy = -10

        #polimorphism
        def update(self):
            self.rect.y += self.speedy

            # ketika objek keluar dari layar pantau, hilangkan objeknya
            if self.rect.bottom < 0: 
                self.kill() 

class Explosion(pygame.sprite.Sprite):
    
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self) 
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    #polimorphism
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill() 
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
        def __init__(self,center):
            pygame.sprite.Sprite.__init__(self) 
            self.type = random.choice(["shield","gun"])
            self.image = power_imgs[self.type]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center 
            self.speedy = 3 

        #polimorphism
        def update(self):
            self.rect.y += self.speedy

            # ketika objek keluar dari layar pantau, hilangkan objeknya
            if self.rect.top > HEIGHT: 
                self.kill() 

# Group untuk menampung semua objek yang ada di game
all_sprites = pygame.sprite.Group()
cats = pygame.sprite.Group()
poisons = pygame.sprite.Group()
powers = pygame.sprite.Group()

for i in range(8):
    new_cat()
pygame.mixer.music.play(-1)

# looping pada game
show_init = True
character_select = True
running = True
losing = True

while running:
    if show_init:
        draw_init()
        show_init = False

    if character_select:
        players = character_selection()
        if players == "1":
            mouse = Mouse1()
        elif players == "2":
            mouse = Mouse2()
        character_select = False
    all_sprites.add(mouse)

    screen.fill(BLACK)

    if players == "1":
        clock.tick(FPS)    
        for event in pygame.event.get():
            Key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse.shoot()
            elif Key_pressed[pygame.K_SPACE]:
                mouse.shoot()
            elif Key_pressed[pygame.K_p]:
                pause()

        all_sprites.update()
        hits = pygame.sprite.groupcollide(cats,poisons,True,True)

        for hit in hits:
            random.choice(expl_sounds).play()
            score += hit.radius 
            expl = Explosion(hit.rect.center,"lg")
            all_sprites.add(expl)
            if random.random() > 0.85:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
            new_cat()

        hits = pygame.sprite.spritecollide(mouse,cats, True,pygame.sprite.collide_circle)

        for hit in hits:
            new_cat()
            mouse._Mouse1__health -= hit.radius
            expl = Explosion(hit.rect.center,"sm")
            all_sprites.add(expl)
            if mouse._Mouse1__health <=0:
                death_expl = Explosion(mouse.rect.center,'mouse')
                all_sprites.add(death_expl)
                die_sound.play() 
                mouse._Mouse1__lives -= 1
                mouse._Mouse1__health = 100
                mouse.hide()

        hits = pygame.sprite.spritecollide(mouse,powers,True)

        for hit in hits:
            if hit.type == "shield":
                mouse._Mouse1__health += 20
                if mouse._Mouse1__health > 100:
                    mouse._Mouse1__health = 100
                shield_sound.play()

            elif hit.type == "gun":
                mouse.gun_up()        
                gun_sound.play()

        if mouse._Mouse1__lives == 0:
            running = False

        screen.fill(BLACK) 
        screen.blit(background_img,(0,0))  
        all_sprites.draw(screen)
        draw_header()
        draw_score(screen,str(score),19,WIDTH/2, 10)
        draw_health1(screen,mouse._Mouse1__health,10,10)
        draw_lives(screen,mouse._Mouse1__lives,mouse_mini_img1,WIDTH - 100, 15)
        pygame.display.update()

    elif players == "2":
        clock.tick(FPS)    
        for event in pygame.event.get():
            Key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse.shoot()
            elif Key_pressed[pygame.K_SPACE]:
                mouse.shoot()
            elif Key_pressed[pygame.K_p]:
                pause()

        all_sprites.update()
        hits = pygame.sprite.groupcollide(cats,poisons,True,True)

        for hit in hits:
            random.choice(expl_sounds).play()
            score += hit.radius 
            expl = Explosion(hit.rect.center,"lg")
            all_sprites.add(expl)
            if random.random() > 0.85:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
            new_cat()

        hits = pygame.sprite.spritecollide(mouse,cats, True,pygame.sprite.collide_circle)

        for hit in hits:
            new_cat()
            mouse._Mouse2__health -= hit.radius
            expl = Explosion(hit.rect.center,"sm")
            all_sprites.add(expl)
            if mouse._Mouse2__health <=0:
                death_expl = Explosion(mouse.rect.center,'mouse')
                all_sprites.add(death_expl)
                die_sound.play() 
                mouse._Mouse2__lives -= 1
                mouse._Mouse2__health = 100
                mouse.hide()

        hits = pygame.sprite.spritecollide(mouse,powers,True)

        for hit in hits:
            if hit.type == "shield":
                mouse._Mouse2__health += 20
                if mouse._Mouse2__health > 150:
                    mouse._Mouse2__health = 150
                shield_sound.play()

            elif hit.type == "gun":
                mouse.gun_up()        
                gun_sound.play()

        if mouse._Mouse2__lives == 0:
            running = False

        screen.fill(BLACK) 
        screen.blit(background_img,(0,0))  
        all_sprites.draw(screen)
        draw_header()
        draw_score(screen,str(score),19,WIDTH/2, 10)
        draw_health2(screen,mouse._Mouse2__health,10,10)
        draw_lives(screen,mouse._Mouse2__lives,mouse_mini_img2,WIDTH - 100, 15)
        pygame.display.update()

if losing:
    uploadScore()
    lose()
    losing = False

pygame.quit()