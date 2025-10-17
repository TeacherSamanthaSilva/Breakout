import pygame
import random
import math

# =======================
# 1. CONFIGURAÇÕES INICIAIS
# =======================

pygame.init()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Pygame Breakout Simples")

# Relógio e FPS
clock = pygame.time.Clock()
FPS = 60

# =======================
# 2. DEFINIÇÃO DOS OBJETOS
# =======================

# 2.1. Barra (Paddle)
BARRA_LARGURA = 100
BARRA_ALTURA = 10
VELOCIDADE_BARRA = 8
barra_rect = pygame.Rect(
    (LARGURA_TELA - BARRA_LARGURA) // 2, 
    ALTURA_TELA - 40, 
    BARRA_LARGURA, 
    BARRA_ALTURA
)

# 2.2. Bola
BOLA_RAIO = 8
bola_rect = pygame.Rect(LARGURA_TELA // 2 - BOLA_RAIO, ALTURA_TELA // 2 - BOLA_RAIO, BOLA_RAIO * 2, BOLA_RAIO * 2)
VELOCIDADE_INICIAL = 2
bola_dx = VELOCIDADE_INICIAL * random.choice([-1, 1])  # Começa para a esquerda ou direita
bola_dy = -VELOCIDADE_INICIAL  # Começa subindo

# 2.3. Tijolos
tijolos = []
TIJOLO_LARGURA = 70
TIJOLO_ALTURA = 20
LINHAS = 5
TIJOLOS_POR_LINHA = LARGURA_TELA // (TIJOLO_LARGURA + 10) - 1 # Calcula quantos cabem
MARGIN_SUPERIOR = 50

# Lista de cores para as linhas de tijolos
CORES_TIJOLOS = [VERMELHO, AMARELO, VERDE, AZUL, VERMELHO]

def criar_tijolos():
    global tijolos
    tijolos = []
    
    # Cálculo para centralizar os tijolos
    espaco_total_necessario = TIJOLOS_POR_LINHA * (TIJOLO_LARGURA + 10) - 10
    offset_x = (LARGURA_TELA - espaco_total_necessario) // 2
    
    for linha in range(LINHAS):
        for coluna in range(TIJOLOS_POR_LINHA):
            tijolo_x = offset_x + coluna * (TIJOLO_LARGURA + 10)
            tijolo_y = MARGIN_SUPERIOR + linha * (TIJOLO_ALTURA + 10)
            
            cor = CORES_TIJOLOS[linha % len(CORES_TIJOLOS)]
            
            tijolo_rect = pygame.Rect(tijolo_x, tijolo_y, TIJOLO_LARGURA, TIJOLO_ALTURA)
            tijolos.append((tijolo_rect, cor)) # Armazena o Rect e a cor

criar_tijolos()


# =======================
# 3. FUNÇÕES DO JOGO
# =======================

def mover_barra(teclas):
    """Atualiza a posição da barra com base nas teclas pressionadas."""
    if teclas[pygame.K_LEFT]:
        barra_rect.x -= VELOCIDADE_BARRA
    if teclas[pygame.K_RIGHT]:
        barra_rect.x += VELOCIDADE_BARRA

    # Limita a barra na tela
    if barra_rect.left < 0:
        barra_rect.left = 0
    if barra_rect.right > LARGURA_TELA:
        barra_rect.right = LARGURA_TELA


def mover_bola():
    """Atualiza a posição da bola e lida com colisões de paredes."""
    global bola_dx, bola_dy
    
    # 3.1. Movimento
    bola_rect.x += bola_dx
    bola_rect.y += bola_dy

    # 3.2. Colisão com paredes laterais
    if bola_rect.left < 0 or bola_rect.right > LARGURA_TELA:
        bola_dx = -bola_dx

    # 3.3. Colisão com a parede superior
    if bola_rect.top < 0:
        bola_dy = -bola_dy

    # 3.4. Colisão com a parede inferior (GAME OVER)
    if bola_rect.bottom > ALTURA_TELA:
        return True # Indica Game Over
    
    return False # Jogo continua

def checar_colisoes():
    """Lida com as colisões da bola com a barra e os tijolos."""
    global bola_dx, bola_dy, tijolos
    
    # 4.1. Colisão com a Barra
    if bola_rect.colliderect(barra_rect) and bola_dy > 0:
        bola_dy = -bola_dy
        
        # Lógica simples para mudar a direção horizontal baseado em onde a bola bateu na barra
        diferenca = bola_rect.centerx - barra_rect.centerx
        bola_dx = diferenca * 0.1 # Ajusta a direção, valor menor para mudança sutil

    # 4.2. Colisão com os Tijolos
    tijolos_a_remover = []
    
    for i in range(len(tijolos)):
        tijolo_rect, tijolo_cor = tijolos[i]
        
        if bola_rect.colliderect(tijolo_rect):
            # Encontrou o tijolo, marca para remoção
            tijolos_a_remover.append(i)
            
            # Inverte a direção vertical da bola (regra mais simples)
            bola_dy = -bola_dy 
            
            # **NOTA:** Uma lógica de colisão mais avançada checaria se a bola bateu na lateral 
            # do tijolo para inverter bola_dx, mas vamos manter simples por enquanto!
            
            break # Processa apenas um tijolo por vez para evitar bugs de colisão dupla

    # Remove os tijolos atingidos (de trás para frente para não bagunçar os índices)
    for i in sorted(tijolos_a_remover, reverse=True):
        tijolos.pop(i)


def desenhar_tudo():
    """Desenha todos os elementos na tela."""
    TELA.fill(PRETO) # Limpa a tela

    # Desenha a Barra
    pygame.draw.rect(TELA, BRANCO, barra_rect)
    
    # Desenha a Bola (círculo no centro do rect)
    pygame.draw.circle(TELA, BRANCO, bola_rect.center, BOLA_RAIO)

    # Desenha os Tijolos
    for tijolo_rect, cor in tijolos:
        pygame.draw.rect(TELA, cor, tijolo_rect)
        
    # Atualiza a tela
    pygame.display.flip()

# =======================
# 4. LOOP PRINCIPAL
# =======================

game_over = False
rodando = True
while rodando:
    # 4.1. Lidar com Eventos (Teclado/Mouse)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
    # Checa o estado do teclado (para movimento contínuo)
    teclas = pygame.key.get_pressed()

    if not game_over:
        # 4.2. Atualizar a Lógica do Jogo
        
        mover_barra(teclas)
        game_over = mover_bola() # Retorna True se a bola cair
        checar_colisoes()
        
        # Verifica se o jogador ganhou
        if not tijolos:
            print("Parabéns! Você venceu!")
            game_over = True

    # 4.3. Desenhar na Tela
    desenhar_tudo()
    
    if game_over:
        # Exibe mensagem de Game Over ou Vitória
        TELA.fill(PRETO)
        fonte = pygame.font.Font(None, 74)
        
        if not tijolos:
             texto = fonte.render("VITÓRIA!", True, AMARELO)
        else:
             texto = fonte.render("GAME OVER", True, VERMELHO)
             
        texto_rect = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        TELA.blit(texto, texto_rect)
        pygame.display.flip()
        
        # Adiciona um pequeno atraso para o usuário ver a mensagem antes de fechar
        # (Você pode adicionar um loop para reiniciar o jogo aqui)
        pygame.time.wait(3000)
        rodando = False


    # Controlar o FPS
    clock.tick(FPS)

pygame.quit()