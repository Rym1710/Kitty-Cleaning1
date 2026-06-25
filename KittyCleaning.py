import pygame

pygame.init()
pygame.mixer.init()

# =====================
# CONFIGURATION
# =====================

TILE_SIZE = 64

WIDTH = 10 * TILE_SIZE
HEIGHT = 8 * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kitty Cleaning")

# =====================
# IMAGES
# =====================

chat_img = pygame.image.load("chat.png")
dechet_img = pygame.image.load("dechet.png")
poubelle_img = pygame.image.load("poubelle.png")
mur_img = pygame.image.load("mur.png")

# =====================
# NIVEAU
# =====================

level = [
    "##########",
    "#        #",
    "#    B   #",
    "#  X     #",
    "#        #",
    "#    P   #",
    "#        #",
    "##########"
]

walls = set()
targets = set()
blocks = set()

player = None

for y, row in enumerate(level):

    for x, cell in enumerate(row):

        if cell == "#":
            walls.add((x, y))

        elif cell == "P":
            player = (x, y)

        elif cell == "B":
            blocks.add((x, y))

        elif cell == "X":
            targets.add((x, y))

# =====================
# VARIABLES
# =====================

moves = 0
win = False
game_over = False

font = pygame.font.SysFont(None, 42)
clock = pygame.time.Clock()

# =====================
# TIMER (1 minute)
# =====================

TIME_LIMIT = 60
start_time = pygame.time.get_ticks()

# =====================
# DÉPLACEMENT
# =====================

def move_player(dx, dy):

    global player
    global moves
    global win
    global game_over

    if win or game_over:
        return

    nx = player[0] + dx
    ny = player[1] + dy

    # Mur
    if (nx, ny) in walls:
        return

    # Déchet
    if (nx, ny) in blocks:

        bx = nx + dx
        by = ny + dy

        if (bx, by) in walls:
            return

        if (bx, by) in blocks:
            return

        blocks.remove((nx, ny))
        blocks.add((bx, by))

    # Déplacement joueur
    player = (nx, ny)

    moves += 1

    # Vérification victoire
    if blocks == targets:
        win = True

# =====================
# BOUCLE PRINCIPALE
# =====================

running = True

while running:

    # =====================
    # TIMER
    # =====================

    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    time_left = max(0, TIME_LIMIT - elapsed)

    if time_left == 0 and not win:
        game_over = True

    # =====================
    # ÉVÉNEMENTS
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                move_player(0, -1)

            elif event.key == pygame.K_DOWN:
                move_player(0, 1)

            elif event.key == pygame.K_LEFT:
                move_player(-1, 0)

            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)

    # =====================
    # FOND
    # =====================

    screen.fill((255, 226, 168))

    # =====================
    # CARTE
    # =====================

    for y in range(len(level)):

        for x in range(len(level[0])):

            rect = pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            pygame.draw.rect(
                screen,
                (143, 117, 49),
                rect,
                1
            )

            if (x, y) in walls:

                screen.blit(
                    mur_img,
                    (x * TILE_SIZE, y * TILE_SIZE)
                )

            if (x, y) in targets:

                screen.blit(
                    poubelle_img,
                    (x * TILE_SIZE, y * TILE_SIZE)
                )

    # =====================
    # DÉCHETS
    # =====================

    for bx, by in blocks:

        screen.blit(
            dechet_img,
            (
                bx * TILE_SIZE,
                by * TILE_SIZE
            )
        )

    # =====================
    # CHAT
    # =====================

    screen.blit(
        chat_img,
        (
            player[0] * TILE_SIZE,
            player[1] * TILE_SIZE
        )
    )

    # =====================
    # AFFICHAGE TEXTE
    # =====================

    moves_text = font.render(
        f"Coups : {moves}",
        True,
        (0, 0, 0)
    )

    screen.blit(moves_text, (10, 10))

    minutes = time_left // 60
    seconds = time_left % 60

    timer_text = font.render(
        f"{minutes:02}:{seconds:02}",
        True,
        (255, 0, 0)
    )

    screen.blit(timer_text, (10, 50))

    # =====================
    # VICTOIRE
    # =====================

    if win:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        msg = font.render(
            "VICTOIRE !",
            True,
            (255, 255, 0)
        )

        screen.blit(
            msg,
            (
                WIDTH // 2 - msg.get_width() // 2,
                HEIGHT // 2
            )
        )

    # =====================
    # DÉFAITE
    # =====================

    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        msg = font.render(
            "TEMPS ÉCOULÉ !",
            True,
            (255, 0, 0)
        )

        screen.blit(
            msg,
            (
                WIDTH // 2 - msg.get_width() // 2,
                HEIGHT // 2
            )
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
