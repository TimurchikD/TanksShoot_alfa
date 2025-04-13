from pygame import *
from random import randint
from time import time as timer
 
mixer.init()
mixer.music.load('zvukt.mp3')
mixer.music.play()
fire_sound = mixer.Sound('tv.ogg')
vzr_sound = mixer.Sound('babah.ogg')
 
font.init()
font1 = font.Font(None, 80)
win = font1.render('ХАХХАХАХАХАХААХХАХА', True, (255, 255, 255))
win2 = font1.render('КАПЕЦ ОНИ ЛОХИ!!', True, (255, 255, 255))
lose = font1.render('ДА КАК ТАК ТО ***?!!!!', True, (180, 0, 0))
font2 = font.Font(None, 36)
 
img_back = "fonb.jpg"
img_enemy = "E100.png"
img_hero = "KV2.png"
img_bullet = "BK.png"
img_ast = "Leopard.png"
img_Pz = "JE100.png"
 
score = 0
goal = 500
lost = 0
max_lost = 5
life = 5   
num_fire = 0
rel_time = False
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
 
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys  = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global life
        if self.rect.y > win_height:
            self.rect.x = randint(70, win_width - 70)
            self.rect.y = 0
            lost = lost + 1
            life = life - 1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
 
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('БОЙ')
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 30)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy,randint(80, win_width - 80), -40, 85, 100, randint(2, 3))
    monsters.add(monster)
 
asteroids = sprite.Group()
for i in range(1, 5):
    asteroid = Enemy(img_ast,randint(80, win_width - 80), -40, 60, 80, randint(1, 2))
    asteroids.add(asteroid)

je100s = sprite.Group()
for i in range(1, 5):
    je100 = Enemy(img_ast,randint(80, win_width - 80), -40, 95, 100, randint(1, 2))
    je100s.add(je100)

bullets = sprite.Group()
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 15 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                
                if num_fire >= 15 and rel_time == False:
                    last_time = timer()
                    rel_time = True
 
    if not finish:
        window.blit(background,(0, 0))  
 
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render('Пропущенно: ' + str(lost), 1,  (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        text_life = font2.render('Жизни:' + str(life), 1,  (255, 255, 255))
        window.blit(text_life, (10, 80))
 
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        je100s.update()
 
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        je100s.draw(window)
 
        if rel_time == True:
            now_time = timer()
 
            if now_time - last_time < 3:
                reload = font2.render('ПЕРЕЗАРЯДКА!!!!', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
 
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            vzr_sound.play()            
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 85, 100, randint(2, 3))
            monsters.add(monster)
            
 
        collides1 = sprite.groupcollide(bullets, asteroids, True, True)
        for c in collides1:
            score = score + 1
            
            asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 60, 80, randint(1, 2))
            asteroids.add(asteroid)

        collides2 = sprite.groupcollide(bullets, je100s, True, True)
        for c in collides2:
            score = score + 1
            
            je100 = Enemy(img_Pz, randint(80, win_width - 80), -40, 95, 100, randint(1, 2))
            je100s.add(je100)
 
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life -= 1
            lost+=1
        
        if sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            life-=1
            lost+=1

        if sprite.spritecollide(ship, je100s, False):
            sprite.spritecollide(ship, je100s, True)
            life-=1
            lost+=1
 
 
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (120, 200))
 
        if score >= goal:
            finish = True
            window.blit(win, (120, 200))
            window.blit(win2, (120, 200))
 
        display.update()
 
    time.delay(50)