import os
import pygame
import random

###########################################################
# 기본 초기화 (반드시 해야하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("DDONG") # 게임 이름

#FPS
clock = pygame.time.Clock()
###########################################################

current_path = os.path.dirname(__file__)

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 폰트 등)
#배경 만들기
background = pygame.image.load(os.path.join(current_path, "background.png"))

#캐릭터 만들기
character = pygame.image.load(os.path.join(current_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

#이동 위치
to_x_LEFT = 0
to_x_RIGHT = 0

#캐릭터 속도
character_speed = 6
#폰트 정의
game_font = pygame.font.Font(None, 40)
result_font = pygame.font.Font(None, 40)
#점수
score = 0

# 똥 만들기
ddong = pygame.image.load(os.path.join(current_path, "enemy.png"))
ddong_size = ddong.get_rect().size
ddong_width = ddong_size[0]
ddong_height = ddong_size[1]
ddong_x_pos = random.randint(0, screen_width - ddong_width)
ddong_y_pos = 0
ddong_speed = 5

ddongs = []

ddongs.append([ddong_x_pos, ddong_y_pos])

running = True
while running:
    dt = clock.tick(60)
    
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x_RIGHT += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                to_x_RIGHT = 0


    # 3. 게임 캐릭터 위치 정의    
    character_x_pos += to_x_LEFT + to_x_RIGHT

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 똥 위치 정의
    for d in ddongs:
        d[1] += ddong_speed
        if d[1] == 300:
            ddong_x = random.randint(0, screen_width - ddong_width)
            ddongs.append([ddong_x, ddong_y_pos])
        if d[1] == screen_height:
            score += 10

    

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for d in ddongs:
        ddong_rect = ddong.get_rect()
        ddong_rect.left = d[0] 
        ddong_rect.top = d[1]

        if character_rect.colliderect(ddong_rect):
            print("충돌했어요")
            pygame.time.delay(1000)
        
            running = False


    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for d in ddongs:
        screen.blit(ddong, (d[0], d[1]))
    
    score_view = game_font.render("score : " + str(score), True, (0, 0, 0))
    screen.blit(score_view, (0, 0))

    pygame.display.update()

pygame.quit()