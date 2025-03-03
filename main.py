import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("무한의 계단 게임")

clock = pygame.time.Clock()
FPS = 30

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)

# 플레이어 설정
player_size = 30
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 60
player_speed = 5
direction = 1  # 1: 오른쪽, -1: 왼쪽

# 계단 설정
stair_width = 100
stair_height = 10
stairs = []
# 초기 계단 생성 (총 20개)
for i in range(20):
    x = random.randint(0, WIDTH - stair_width)
    y = HEIGHT - (i * 30) - 40
    stairs.append([x, y])

score = 0

def move_stairs():
    global score
    # 계단을 아래로 이동
    for stair in stairs:
        stair[1] += 2
    # 가장 아래 계단이 화면 아래로 벗어나면 제거하고 새 계단 추가
    if stairs[-1][1] > HEIGHT:
        score += 1
        stairs.pop(-1)
        new_x = random.randint(0, WIDTH - stair_width)
        new_y = stairs[0][1] - 30
        stairs.insert(0, [new_x, new_y])

def check_collision():
    # 플레이어가 계단 위에 있는지 확인
    for stair in stairs:
        stair_x, stair_y = stair
        # 플레이어 발바닥이 계단 범위 내에 있는지 (여유를 조금 줌)
        if player_y + player_size >= stair_y and player_y + player_size <= stair_y + stair_height + 5:
            # 플레이어의 가로 범위가 계단 안에 겹치는지 체크
            if player_x + player_size > stair_x and player_x < stair_x + stair_width:
                return True
    return False

running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 스페이스바를 누르면 이동 방향 전환
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                direction *= -1

    # 플레이어 이동
    player_x += player_speed * direction
    # 화면 밖으로 나가지 않도록 처리
    if player_x < 0:
        player_x = 0
        direction *= -1
    elif player_x > WIDTH - player_size:
        player_x = WIDTH - player_size
        direction *= -1

    move_stairs()

    # 계단과 충돌하지 않으면 게임 종료
    if not check_collision():
        print("Game Over! Score:", score)
        running = False

    # 화면 그리기
    screen.fill(WHITE)
    # 계단 그리기
    for stair in stairs:
        pygame.draw.rect(screen, BLUE, (stair[0], stair[1], stair_width, stair_height))
    # 플레이어 그리기
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
