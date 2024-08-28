import pygame
import sys

# Inicializando o Pygame
pygame.init()
pygame.mixer.init()  # Inicializa o mixer para tocar sons

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 15
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
PADDLE_SPEED = 10
MAX_SCORE = 7  # Definindo o máximo de pontos para o jogo terminar

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carregar e redimensionar imagens
background_img = pygame.image.load("img/background.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensiona o fundo para a tela

ball_img = pygame.image.load("img/Plan-4.png")
ball_img = pygame.transform.scale(ball_img, (BALL_RADIUS * 2, BALL_RADIUS * 2))  # Ajusta o tamanho da bola

# Carregando os sons
hit_sound = pygame.mixer.Sound("music/au-michael.mp3")
point_sound = pygame.mixer.Sound("music/hehe-michael.mp3")
game_over_sound = pygame.mixer.Sound("music/rusbe-michael.mp3")
background_music = "music/beatit.mp3"

# Onde toca a música de fundo
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # -1 para tocar em loop

# Função para desenhar o retângulo do paddle
def draw_paddle(paddle):
    pygame.draw.rect(screen, WHITE, paddle)

# Função principal
def main():
    clock = pygame.time.Clock()

    # Posições iniciais dos paddles
    left_paddle = pygame.Rect(30, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Posições e velocidade da bola
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_dx = BALL_SPEED_X
    ball_dy = BALL_SPEED_Y

    # Contadores de pontuação
    left_score = 0
    right_score = 0

    font = pygame.font.Font(None, 74)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento dos paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Movimento da bola
        ball.x += ball_dx
        ball.y += ball_dy

        # Colisão com as bordas da tela (vertical)
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_dy *= -1

        # Verificação se a bola passou pelos paddles (pontos)
        if ball.left <= 0:  # Ponto para o jogador da direita
            pygame.mixer.Sound.play(point_sound)  # Toca o som de ponto
            right_score += 1
            ball.x = SCREEN_WIDTH // 2
            ball.y = SCREEN_HEIGHT // 2
            ball_dx *= -1  # Inverte a direção da bola
        if ball.right >= SCREEN_WIDTH:  # Ponto para o jogador da esquerda
            pygame.mixer.Sound.play(point_sound)  # Toca o som de ponto
            left_score += 1
            ball.x = SCREEN_WIDTH // 2
            ball.y = SCREEN_HEIGHT // 2
            ball_dx *= -1  # Inverte a direção da bola

        # Colisão com os paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            pygame.mixer.Sound.play(hit_sound)  # Toca o som de colisão com o paddle
            ball_dx *= -1

        # Checar fim de jogo
        if left_score >= MAX_SCORE or right_score >= MAX_SCORE:
            pygame.mixer.music.stop()  # Para a música de fundo
            pygame.mixer.Sound.play(game_over_sound)  # Toca o som de fim de jogo
            pygame.time.delay(3000)  # Espera 3 segundos antes de fechar o jogo
            pygame.quit()
            sys.exit()

        # Desenhar o fundo
        screen.blit(background_img, (0, 0))

        # Desenhar paddles e bola
        draw_paddle(left_paddle)
        draw_paddle(right_paddle)
        screen.blit(ball_img, ball)

        # Desenhar pontuação
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(right_text, (SCREEN_WIDTH * 3 // 4, 20))

        # Atualizar a tela
        pygame.display.flip()

        # Controlar a taxa de frames
        clock.tick(60)

if __name__ == "__main__":
    main()
