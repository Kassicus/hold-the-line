import pygame
import random
import math

pygame.mixer.pre_init(44100, 16, 1, 512)
pygame.init()

delta_time = 0

sounds = {
    "gun 1": pygame.mixer.Sound("assets/sounds/gunshot_1.wav"),
    "gun 2": pygame.mixer.Sound("assets/sounds/gunshot_2.wav"),
    "gun 3": pygame.mixer.Sound("assets/sounds/rifle_1.wav"),
    "gun 4": pygame.mixer.Sound("assets/sounds/rifle_2.wav")
}

def playSound(sound):
    pygame.mixer.Sound.set_volume(sounds[sound], 0.5)
    pygame.mixer.Sound.play(sounds[sound])
    pygame.mixer.Sound.fadeout(sounds[sound], 750)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, sx: int, sy: int, tx: int, ty: int):
        super().__init__()

        self.pos = pygame.math.Vector2(sx, sy)
        self.target_pos = pygame.math.Vector2(tx, ty)
        self.velocity = pygame.math.Vector2()
        self.speed = 750
        self.damage = 1
        self.lifetime = 8000

        self.image = pygame.Surface([3, 3])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.velocity.x, self.velocity.y = self.get_vectors()[0], self.get_vectors()[1]

    def update(self):
        self.pos += self.velocity * delta_time
        self.rect.center = self.pos

        self.lifetime -= 1

        if self.lifetime < 0:
            self.kill()

    def get_vectors(self) -> list:
        distance = [self.target_pos.x - self.pos.x, self.target_pos.y - self.pos.y]
        normal = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / normal, distance[1] / normal]
        vectors = [direction[0] * self.speed, direction[1] * self.speed]

        return vectors
    
    def destroy(self):
        self.kill()

class MachineGunner(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.pos = pygame.math.Vector2(x, y)

        self.target = None
        self.accuracy = 80
        self.shot_max_cooldown = 5
        self.shot_cooldown = random.randint(0, self.shot_max_cooldown)

        self.magazine_capacity = 250
        self.rounds_remaining = self.magazine_capacity
        self.reloading = False
        self.reload_max_timer = 800
        self.reload_timer = self.reload_max_timer

        self.image = pygame.Surface([20, 30])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, enemies: pygame.sprite.Group):
        if self.target == None:
            if len(enemies.sprites()) > 0:
                # closest
                self.target = min([z for z in enemies], key=lambda e: self.pos.distance_to(e.pos))    

        if self.target is not None:
            if self.reloading == False:
                self.shot_cooldown -= 1
            else:
                self.reload_timer -= 1
                if self.reload_timer <= 0:
                    self.reloading = False
                    self.reload_timer = self.reload_max_timer
                    self.rounds_remaining = self.magazine_capacity

            if self.target.alive():
                if self.shot_cooldown < 0:
                    self.shoot()
                    self.shot_cooldown = self.shot_max_cooldown
            else:
                self.target = None

    def shoot(self):
        b = Bullet(
            self.pos.x,
            self.pos.y,
            random.randint(int(self.target.pos.x) - self.accuracy, int(self.target.pos.x) + self.accuracy),
            random.randint(int(self.target.pos.y) - self.accuracy, int(self.target.pos.y) + self.accuracy)
            )
        
        game.friends_projectiles.add(b)

        playSound(random.choice(("gun 1", "gun 2")))

        self.rounds_remaining -= 1

        if self.rounds_remaining <= 0:
            self.reloading = True

class AutoRifleman(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.pos = pygame.math.Vector2(x, y)

        self.target = None
        self.accuracy = 50
        self.shot_max_cooldown = 30
        self.shot_cooldown = random.randint(0, self.shot_max_cooldown)

        self.magazine_capacity = 30
        self.rounds_remaining = self.magazine_capacity
        self.reloading = False
        self.reload_max_timer = 500
        self.reload_timer = self.reload_max_timer

        self.image = pygame.Surface([20, 30])
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, enemies: pygame.sprite.Group):
        if self.target == None:
            if len(enemies.sprites()) > 0:
                # closest
                self.target = min([z for z in enemies], key=lambda e: self.pos.distance_to(e.pos))    

        if self.target is not None:
            if self.reloading == False:
                self.shot_cooldown -= 1
            else:
                self.reload_timer -= 1
                if self.reload_timer <= 0:
                    self.reloading = False
                    self.reload_timer = self.reload_max_timer
                    self.rounds_remaining = self.magazine_capacity

            if self.target.alive():
                if self.shot_cooldown < 0:
                    self.shoot()
                    self.shot_cooldown = random.randint(10, self.shot_max_cooldown)
            else:
                self.target = None

    def shoot(self):
        b = Bullet(
            self.pos.x,
            self.pos.y,
            random.randint(int(self.target.pos.x) - self.accuracy, int(self.target.pos.x) + self.accuracy),
            random.randint(int(self.target.pos.y) - self.accuracy, int(self.target.pos.y) + self.accuracy)
            )
        
        game.friends_projectiles.add(b)

        playSound(random.choice(("gun 1", "gun 2")))

        self.rounds_remaining -= 1

        if self.rounds_remaining <= 0:
            self.reloading = True

class Rifleman(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.pos = pygame.math.Vector2(x, y)

        self.target = None
        self.accuracy = 20
        self.shot_max_cooldown = 100
        self.shot_cooldown = random.randint(0, self.shot_max_cooldown)

        self.magazine_capacity = 10
        self.rounds_remaining = self.magazine_capacity
        self.reloading = False
        self.reload_max_timer = 350
        self.reload_timer = self.reload_max_timer

        self.image = pygame.Surface([20, 30])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, enemies: pygame.sprite.Group):
        if self.target == None:
            if len(enemies.sprites()) > 0:
                # closest
                self.target = min([z for z in enemies], key=lambda e: self.pos.distance_to(e.pos))    

        if self.target is not None:
            if self.reloading == False:
                self.shot_cooldown -= 1
            else:
                self.reload_timer -= 1
                if self.reload_timer <= 0:
                    self.reloading = False
                    self.reload_timer = self.reload_max_timer
                    self.rounds_remaining = self.magazine_capacity

            if self.target.alive():
                if self.shot_cooldown < 0:
                    self.shoot()
                    self.shot_cooldown = random.randint(15, self.shot_max_cooldown)
            else:
                self.target = None

    def shoot(self):
        b = Bullet(
            self.pos.x,
            self.pos.y,
            random.randint(int(self.target.pos.x) - self.accuracy, int(self.target.pos.x) + self.accuracy),
            random.randint(int(self.target.pos.y) - self.accuracy, int(self.target.pos.y) + self.accuracy)
            )
        
        game.friends_projectiles.add(b)

        playSound(random.choice(("gun 3", "gun 4")))

        self.rounds_remaining -= 1

        if self.rounds_remaining <= 0:
            self.reloading = True

class Musketman(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, side: str):
        super().__init__()

        self.pos = pygame.math.Vector2(x, y)

        self.side = side
        self.health = 3

        self.target = None
        self.accuracy = random.randint(60, 120)
        self.shot_max_cooldown = 50
        self.shot_cooldown = random.randint(0, self.shot_max_cooldown)

        self.magazine_capacity = 2
        self.rounds_remaining = self.magazine_capacity
        self.reloading = False
        self.reload_max_timer = 350
        self.reload_timer = self.reload_max_timer

        self.image = pygame.Surface([20, 30])
        if self.side == "friend":
            self.image.fill((0, 0, 255))
        elif self.side == "enemy":
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, bug_fix: pygame.sprite.Group):
        if self.target == None:
            if self.side == "friend":
                enemies = game.enemies
            elif self.side == "enemy":
                enemies = game.friends

            if len(enemies.sprites()) > 0:
                # closest
                self.target = min([z for z in enemies], key=lambda e: self.pos.distance_to(e.pos))    

        if self.target is not None:
            if self.reloading == False:
                self.shot_cooldown -= 1
            else:
                self.reload_timer -= 1
                if self.reload_timer <= 0:
                    self.reloading = False
                    self.reload_timer = self.reload_max_timer
                    self.rounds_remaining = self.magazine_capacity

            if self.target.alive():
                if self.shot_cooldown < 0:
                    self.shoot()
                    self.shot_cooldown = random.randint(0, self.shot_max_cooldown)
            else:
                self.target = None

        if self.health <= 0:
            self.kill()

    def shoot(self):
        b = Bullet(
            self.pos.x,
            self.pos.y,
            random.randint(int(self.target.pos.x) - self.accuracy, int(self.target.pos.x) + self.accuracy),
            random.randint(int(self.target.pos.y) - self.accuracy, int(self.target.pos.y) + self.accuracy)
            )
        
        if self.side == "friend":
            game.friends_projectiles.add(b)
        elif self.side == "enemy":
            game.enemies_projectiles.add(b)

        playSound(random.choice(("gun 1", "gun 2", "gun 3", "gun 4")))

        self.rounds_remaining -= 1

        if self.rounds_remaining <= 0:
            self.reloading = True

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = pygame.math.Vector2(random.randint(1200, 1500), random.randint(0, 900))
        self.velocity = pygame.math.Vector2()
        self.speed = random.randint(30, 80)

        self.health = 4

        self.image = pygame.Surface([20, 30])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.velocity.x = -self.speed
        self.pos += self.velocity * delta_time
        self.rect.center = self.pos

        if self.health <= 0:
            self.kill()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([1200, 900])
        pygame.display.set_caption("Hold or something?")

        self.running = True
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()

        self.frame_limit = 120

        self.fight = False

        self.friends = pygame.sprite.Group()
        self.friends_projectiles = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemies_projectiles = pygame.sprite.Group()

        self.font = pygame.font.SysFont("Courier", 16)
        self.fps = self.font.render(str(int(self.clock.get_fps())), True, (0, 255, 0))
        self.fight_text = self.font.render("False", True, (255, 255, 255))

    def spawn_wave(self, count: int):
        for x in range(count):
            x = Zombie()
            self.zombies.add(x)

    def collide_projectiles(self):
        for z in self.zombies:
            for p in self.friends_projectiles:
                if z.rect.colliderect(p.rect):
                    z.health -= p.damage
                    p.destroy()

        for e in self.enemies:
            for p in self.friends_projectiles:
                if e.rect.colliderect(p.rect):
                    e.health -= p.damage
                    p.destroy()

        for f in self.friends:
            for p in self.enemies_projectiles:
                if f.rect.colliderect(p.rect):
                    f.health -= p.damage
                    p.destroy()

    def toggle_fight(self):
        if self.fight:
            self.fight = False
            self.fight_text = self.font.render("False", True, (255, 255, 255))
        else:
            self.fight = True
            self.fight_text = self.font.render("True", True, (255, 255, 255))

    def start(self):
        while self.running:
            self.event_loop()
            self.draw()
            self.update()

    def event_loop(self):
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    x, y = pygame.mouse.get_pos()
                    r = Rifleman(x, y)
                    self.friends.add(r)

                if event.key == pygame.K_m:
                    x, y = pygame.mouse.get_pos()
                    m = MachineGunner(x, y)
                    self.friends.add(m)

                if event.key == pygame.K_a:
                    x, y = pygame.mouse.get_pos()
                    a = AutoRifleman(x, y)
                    self.friends.add(a)

                if event.key == pygame.K_g:
                    x, y = pygame.mouse.get_pos()
                    g = Musketman(x, y, "friend")
                    self.friends.add(g)

                if event.key == pygame.K_b:
                    x, y = pygame.mouse.get_pos()
                    b = Musketman(x, y, "enemy")
                    self.enemies.add(b)

                if event.key == pygame.K_c:
                    for f in self.friends:
                        f.kill()
                    for e in self.enemies:
                        e.kill()

                if event.key == pygame.K_SPACE:
                    self.toggle_fight()

                if event.key == pygame.K_1:
                    self.spawn_wave(10)
                
                if event.key == pygame.K_2:
                    self.spawn_wave(20)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.friends.draw(self.screen)
        self.friends_projectiles.draw(self.screen)
        self.zombies.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemies_projectiles.draw(self.screen)

        self.screen.blit(self.fps, (10, 10))
        self.screen.blit(self.fight_text, (1200 / 2 - self.fight_text.get_width() / 2, 10))

    def update(self):
        global delta_time

        self.fps = self.font.render(str(int(self.clock.get_fps())), True, (0, 255, 0))

        if self.fight:
            self.collide_projectiles()

            self.friends.update(self.zombies)
            self.friends_projectiles.update()
            self.zombies.update()
            self.enemies.update(self.zombies)
            self.enemies_projectiles.update()

        pygame.display.update()
        delta_time = self.clock.tick(self.frame_limit) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()