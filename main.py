import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Python Game")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
#SPACESHIP = pygame.transform.scale(pygame.image.load("player.png"), (PLAYER_WIDTH , PLAYER_HEIGHT))

PLAYER_VEL = 5
STAR_WIDTH, STAR_HEIGHT = 10, 20

STAR_VEL = 3

TIME_FONT = pygame.font.Font("Silkscreen-Regular.ttf", 30)
GAME_OVER_FONT = pygame.font.Font("Silkscreen-Regular.ttf", 70)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = TIME_FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)
    #WIN.blit(SPACESHIP, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 1000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, random.randint(-300, -STAR_HEIGHT), STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = GAME_OVER_FONT.render("You Lost!", 1, "red")
            score_text = GAME_OVER_FONT.render(f"Score: {round(elapsed_time)}", 1, "red")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2 - 100))
            WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2 - score_text.get_height()/2 + 100))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)
    
    pygame.quit()

if __name__ == "__main__":
    main()