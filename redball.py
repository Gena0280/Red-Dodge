import pygame
import random
import sys
import time
import math  

pygame.init()

WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquive les balles rouges !")


BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


PLAYER_RADIUS = 15
ENEMY_RADIUS = 15
BONUS_RADIUS = 10
PLAYER_SPEED = 8
NUM_ENEMIES = 14
NUM_BONUSES = 10
INVULNERABILITY_TIME = 2

font = pygame.font.SysFont(None, 36)



class Ball:
    def __init__(self, x, y, radius, color, speed_x=0, speed_y=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.speed_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.speed_y *= -1

    def collide_with(self, other):
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist < self.radius + other.radius


def draw_text_center(surface, text, size, color, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surface, rect)



def show_main_menu():
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("arialblack", 72)
    menu_font = pygame.font.SysFont("arial", 42)
    selected_color = (255, 215, 0)
    normal_color = WHITE

    options = [
        ("1 - Mode Solo (Bleu - ZQSD)", "solo"),
        ("2 - Mode 2 Joueurs (ZQSD + Flèches)", "multi"),
        ("3 - Mode Solo Pro (Difficile)", "solo_pro"),
        ("Echap - Quitter", "quit")
    ]
    selected_index = -1
    pulse = 0

    
    gradient = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        c = int(20 + 80 * (y / HEIGHT))
        pygame.draw.line(gradient, (c, c, c + 40), (0, y), (WIDTH, y))

    while True:
        clock.tick(60)
        screen.blit(gradient, (0, 0))

        
        pulse = (pulse + 2) % 360
        color_intensity = int(128 + 127 * abs(math.sin(pulse * 0.02)))
        title_color = (color_intensity, color_intensity, 255)

        title_surface = title_font.render("Esquive les Balles Rouges", True, title_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_surface, title_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_index = -1

        for i, (text, _) in enumerate(options):
            y = HEIGHT // 2.3 + i * 80
            text_surface = menu_font.render(text, True, normal_color)
            rect = text_surface.get_rect(center=(WIDTH // 2, y))

            if rect.collidepoint(mouse_x, mouse_y):
                text_surface = menu_font.render(text, True, selected_color)
                selected_index = i

            screen.blit(text_surface, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "solo"
                if event.key == pygame.K_2:
                    return "multi"
                if event.key == pygame.K_3:
                    return "solo_pro"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if selected_index != -1:
                    choice = options[selected_index][1]
                    if choice == "quit":
                        pygame.quit()
                        sys.exit()
                    else:
                        return choice



def main_game(mode):
    clock = pygame.time.Clock()

    player1 = Ball(WIDTH // 3, HEIGHT // 2, PLAYER_RADIUS, BLUE)
    player2 = Ball(WIDTH // 3 * 2, HEIGHT // 2, PLAYER_RADIUS, GREEN)

    enemies = []
    for _ in range(NUM_ENEMIES):
        x = random.randint(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS)
        y = random.randint(ENEMY_RADIUS, HEIGHT - ENEMY_RADIUS)
        speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        speed_y = random.choice([-3, -2, -1, 1, 2, 3])
        enemies.append(Ball(x, y, ENEMY_RADIUS, RED, speed_x, speed_y))

    bonuses = []
    for _ in range(NUM_BONUSES):
        x = random.randint(BONUS_RADIUS, WIDTH - BONUS_RADIUS)
        y = random.randint(BONUS_RADIUS, HEIGHT - BONUS_RADIUS)
        bonuses.append(Ball(x, y, BONUS_RADIUS, WHITE))

    score1 = 0
    score2 = 0
    running = True
    game_over = False
    win = False
    invulnerable = True
    invulnerability_start = time.time()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        if invulnerable and time.time() - invulnerability_start > INVULNERABILITY_TIME:
            invulnerable = False

        if not game_over and not win:
            keys = pygame.key.get_pressed()

            
            dx1, dy1 = 0, 0
            if keys[pygame.K_q]: dx1 -= 1
            if keys[pygame.K_d]: dx1 += 1
            if keys[pygame.K_z]: dy1 -= 1
            if keys[pygame.K_s]: dy1 += 1
            if dx1 != 0 and dy1 != 0:
                dx1 *= 0.7071
                dy1 *= 0.7071
            new_x1 = player1.x + dx1 * PLAYER_SPEED
            new_y1 = player1.y + dy1 * PLAYER_SPEED
            if PLAYER_RADIUS <= new_x1 <= WIDTH - PLAYER_RADIUS:
                player1.x = new_x1
            if PLAYER_RADIUS <= new_y1 <= HEIGHT - PLAYER_RADIUS:
                player1.y = new_y1

           
            if mode == "multi":
                dx2, dy2 = 0, 0
                if keys[pygame.K_LEFT]: dx2 -= 1
                if keys[pygame.K_RIGHT]: dx2 += 1
                if keys[pygame.K_UP]: dy2 -= 1
                if keys[pygame.K_DOWN]: dy2 += 1
                if dx2 != 0 and dy2 != 0:
                    dx2 *= 0.7071
                    dy2 *= 0.7071
                new_x2 = player2.x + dx2 * PLAYER_SPEED
                new_y2 = player2.y + dy2 * PLAYER_SPEED
                if PLAYER_RADIUS <= new_x2 <= WIDTH - PLAYER_RADIUS:
                    player2.x = new_x2
                if PLAYER_RADIUS <= new_y2 <= HEIGHT - PLAYER_RADIUS:
                    player2.y = new_y2

           
            for enemy in enemies:
                enemy.move()

            
            if not invulnerable:
                for enemy in enemies:
                    if player1.collide_with(enemy):
                        game_over = True
                        win = "Vert" if mode == "multi" else "Perdu"
                    if mode == "multi" and player2.collide_with(enemy):
                        game_over = True
                        win = "Bleu"
                if game_over:
                    break

            
            for bonus in bonuses:
                if player1.collide_with(bonus):
                    bonuses.remove(bonus)
                    score1 += 1
                    if mode in ["solo_pro", "multi"]:
                        for enemy in enemies:
                            enemy.radius += 1
                            enemy.speed_x *= 1.1
                            enemy.speed_y *= 1.1
                elif mode == "multi" and player2.collide_with(bonus):
                    bonuses.remove(bonus)
                    score2 += 1
                    for enemy in enemies:
                        enemy.radius += 1
                        enemy.speed_x *= 1.1
                        enemy.speed_y *= 1.1

            
            if len(bonuses) == 0:
                game_over = True
                if mode == "multi":
                    if score1 > score2:
                        win = "Bleu"
                    elif score2 > score1:
                        win = "Vert"
                    else:
                        win = "Match nul"
                else:
                    win = "Gagné"

        
        screen.fill(BLACK)
        player1.draw(screen)
        if mode == "multi":
            player2.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bonus in bonuses:
            bonus.draw(screen)

        score_text1 = font.render(f"Score Bleu: {score1}", True, BLUE)
        screen.blit(score_text1, (10, 10))
        if mode == "multi":
            score_text2 = font.render(f"Score Vert: {score2}", True, GREEN)
            screen.blit(score_text2, (WIDTH - score_text2.get_width() - 10, 10))

        if game_over:
            if win == "Bleu":
                draw_text_center(screen, "Le Bleu a gagné!", 48, BLUE, HEIGHT // 2)
            elif win == "Vert":
                draw_text_center(screen, "Le Vert a gagné!", 48, GREEN, HEIGHT // 2)
            elif win == "Gagné":
                draw_text_center(screen, "Bravo ! Tu as gagné !", 48, WHITE, HEIGHT // 2)
            elif win == "Perdu":
                draw_text_center(screen, "Tu as perdu !", 48, RED, HEIGHT // 2)
            else:
                draw_text_center(screen, "Match nul!", 48, WHITE, HEIGHT // 2)
            draw_text_center(screen, "Appuyez sur 'R' pour rejouer", 36, WHITE, HEIGHT // 1.5)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return

        pygame.display.flip()



if __name__ == "__main__":
    while True:
        mode = show_main_menu()
        main_game(mode)
