import pygame

pygame.init()

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

moves = 0
win = False

font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# =====================
# DÉPLACEMENT
# =====================

def move_player(dx, dy):
    global player
    global moves
    global win

    if win:
        return

    nx = player[0] + dx
    ny = player[1] + dy

    # mur
    if (nx, ny) in walls:
        return

    # déchet
    if (nx, ny) in blocks:

        bx = nx + dx
        by = ny + dy

        if (bx, by) in walls:
            return

        if (bx, by) in blocks:
            return

        blocks.remove((nx, ny))
        blocks.add((bx, by))

    # déplacement du joueur
    player = (nx, ny)

    moves += 1

    # victoire
    if blocks == targets:
        win = True

# =====================
# BOUCLE PRINCIPALE
# =====================

running = True

while running:

    # événements
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

    # fond
    screen.fill((255, 226, 168))

    # grille + murs + poubelles
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

    # déchets
    for bx, by in blocks:
        screen.blit(
            dechet_img,
            (bx * TILE_SIZE, by * TILE_SIZE)
        )

    # joueur
    screen.blit(
        chat_img,
        (player[0] * TILE_SIZE,
         player[1] * TILE_SIZE)
    )

    # compteur
    txt = font.render(
        f"Coups : {moves}",
        True,
        (0, 0, 0)
    )
    screen.blit(txt, (10, 10))

    # victoire
    if win:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


