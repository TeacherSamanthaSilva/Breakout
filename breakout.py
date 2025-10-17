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
AMARELO = (255, 255, 0)
CINZA_CLARO = (200, 200, 200)

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Pygame Breakout Simples")

# Relógio e FPS
clock = pygame.time.Clock()
FPS = 60

# Fontes
fonte_titulo = pygame.font.Font(None, 74)
fonte_menu = pygame.font.Font(None, 40)

# Estados do Jogo
MENU = 0
JOGANDO = 1
GAME_OVER = 2
VITORIA = 3
estado_jogo = MENU # Começa no Menu!

# =======================
# 2. DEFINIÇÃO DOS OBJETOS (Iniciais)
# =======================

# 2.1. Barra (Paddle)
BARRA_LARGURA = 100
BARRA_ALTURA = 10
VELOCIDADE_BARRA = 8

# 2.2. Bola
BOLA_RAIO = 8
VELOCIDADE_INICIAL = 4 # Velocidade diminuída conforme solicitado

# Variáveis para a bola e tijolos (serão inicializadas na função 'reiniciar_jogo')
barra_rect = None
bola_rect = None
bola_dx = 0
bola_dy = 0
tijolos = []


# =======================
# 3. FUNÇÕES DO JOGO
# =======================

def criar_tijolos():
    """Cria a parede de tijolos."""
    global tijolos
    tijolos = []
    
    TIJOLO_LARGURA = 70
    TIJOLO_ALTURA = 20
    LINHAS = 5
    TIJOLOS_POR_LINHA = LARGURA_TELA // (TIJOLO_LARGURA + 10) - 1
    MARGIN_SUPERIOR = 50
    CORES_TIJOLOS = [(255, 0, 0), (255, 100, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)] # Verm, Laranja, Amar, Verd, Azul

    espaco_total_necessario = TIJOLOS_POR_LINHA * (TIJOLO_LARGURA + 10) - 10
    offset_x = (LARGURA_TELA - espaco_total_necessario) // 2
    
    for linha in range(LINHAS):
        for coluna in range(TIJOLOS_POR_LINHA):
            tijolo_x = offset_x + coluna * (TIJOLO_LARGURA + 10)
            tijolo_y = MARGIN_SUPERIOR + linha * (TIJOLO_ALTURA + 10)
            
            cor = CORES_TIJOLOS[linha % len(CORES_TIJOLOS)]
            
            tijolo_rect = pygame.Rect(tijolo_x, tijolo_y, TIJOLO_LARGURA, TIJOLO_ALTURA)
            tijolos.append((tijolo_rect, cor))


def reiniciar_jogo():
    """Define as posições iniciais para a barra e a bola."""
    global barra_rect, bola_rect, bola_dx, bola_dy
    
    # 3.1. Reinicia a Barra
    barra_rect = pygame.Rect(
        (LARGURA_TELA - BARRA_LARGURA) // 2, 
        ALTURA_TELA - 40, 
        BARRA_LARGURA, 
        BARRA_ALTURA
    )

    # 3.2. Reinicia a Bola
    bola_rect = pygame.Rect(LARGURA_TELA // 2 - BOLA_RAIO, ALTURA_TELA - 60, BOLA_RAIO * 2, BOLA_RAIO * 2)
    bola_dx = VELOCIDADE_INICIAL * random.choice([-1, 1])
    bola_dy = -VELOCIDADE_INICIAL 

    # 3.3. Cria os Tijolos
    criar_tijolos()


def mover_barra(teclas):
    """Atualiza a posição da barra."""
    if teclas[pygame.K_LEFT]:
        barra_rect.x -= VELOCIDADE_BARRA
    if teclas[pygame.K_RIGHT]:
        barra_rect.x += VELOCIDADE_BARRA

    if barra_rect.left < 0:
        barra_rect.left = 0
    if barra_rect.right > LARGURA_TELA:
        barra_rect.right = LARGURA_TELA


def mover_bola():
    """Atualiza a posição da bola e checa as paredes."""
    global bola_dx, bola_dy, estado_jogo
    
    bola_rect.x += bola_dx
    bola_rect.y += bola_dy

    # Colisão com paredes laterais e superior
    if bola_rect.left < 0 or bola_rect.right > LARGURA_TELA:
        bola_dx = -bola_dx
    if bola_rect.top < 0:
        bola_dy = -bola_dy

    # Colisão com a parede inferior (Game Over)
    if bola_rect.bottom > ALTURA_TELA:
        estado_jogo = GAME_OVER # Muda o estado para Game Over


def checar_colisoes():
    """Lida com as colisões da bola com a barra e os tijolos."""
    global bola_dx, bola_dy, tijolos, estado_jogo
    
    # Colisão com a Barra
    if bola_rect.colliderect(barra_rect) and bola_dy > 0:
        bola_dy = -bola_dy
        diferenca = bola_rect.centerx - barra_rect.centerx
        bola_dx = diferenca * 0.1 

    # Colisão com os Tijolos
    tijolos_a_remover = []
    
    for i in range(len(tijolos)):
        tijolo_rect, tijolo_cor = tijolos[i]
        
        if bola_rect.colliderect(tijolo_rect):
            tijolos_a_remover.append(i)
            bola_dy = -bola_dy
            break 

    # Remove os tijolos atingidos
    for i in sorted(tijolos_a_remover, reverse=True):
        tijolos.pop(i)
        
    # Verifica se o jogador ganhou
    if not tijolos:
        estado_jogo = VITORIA


def desenhar_jogo():
    """Desenha a tela do jogo (barra, bola, tijolos)."""
    TELA.fill(PRETO)
    
    # Desenha a Barra
    pygame.draw.rect(TELA, BRANCO, barra_rect)
    
    # Desenha a Bola
    pygame.draw.circle(TELA, BRANCO, bola_rect.center, BOLA_RAIO)

    # Desenha os Tijolos
    for tijolo_rect, cor in tijolos:
        pygame.draw.rect(TELA, cor, tijolo_rect)


def tela_menu():
    """Exibe o menu inicial e espera pelo 'Start'."""
    TELA.fill(PRETO)
    
    # Título do Jogo
    titulo = fonte_titulo.render("BREAKOUT CLÁSSICO", True, AMARELO)
    titulo_rect = titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 3))
    TELA.blit(titulo, titulo_rect)
    
    # Mensagem "Pressione ESPAÇO para Iniciar"
    start_msg = fonte_menu.render("Pressione ESPAÇO para INICIAR", True, CINZA_CLARO)
    start_rect = start_msg.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50))
    TELA.blit(start_msg, start_rect)


# =======================
# 4. LOOP PRINCIPAL
# =======================

rodando = True
while rodando:
    # 4.1. Lidar com Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Lógica de Transição de Estado:
        if estado_jogo == MENU or estado_jogo == GAME_OVER or estado_jogo == VITORIA:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                # Se apertar ESPAÇO no menu/fim de jogo, o jogo começa/reinicia
                reiniciar_jogo()
                estado_jogo = JOGANDO

    # Checa o estado do teclado (para movimento contínuo da barra)
    teclas = pygame.key.get_pressed()

    # 4.2. Executar Lógica Baseado no Estado
    
    if estado_jogo == MENU:
        tela_menu()
        
    elif estado_jogo == JOGANDO:
        mover_barra(teclas)
        mover_bola() # Vai mudar o estado se for Game Over
        checar_colisoes() # Vai mudar o estado se for Vitória
        desenhar_jogo()
        
    elif estado_jogo == GAME_OVER or estado_jogo == VITORIA:
        # Reutiliza o desenhar_jogo para ver o resultado final do jogo antes da mensagem
        desenhar_jogo()
        
        # Exibe a mensagem
        TELA.fill(PRETO)
        
        if estado_jogo == VITORIA:
            msg = fonte_titulo.render("VITÓRIA!", True, VERMELHO)
            sub_msg = fonte_menu.render("Pressione ESPAÇO para REINICIAR", True, CINZA_CLARO)
        else: # GAME_OVER
            msg = fonte_titulo.render("GAME OVER", True, AMARELO)
            sub_msg = fonte_menu.render("Pressione ESPAÇO para REINICIAR", True, CINZA_CLARO)
            
        msg_rect = msg.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 20))
        sub_rect = sub_msg.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50))
        
        TELA.blit(msg, msg_rect)
        TELA.blit(sub_msg, sub_rect)
        

    # 4.3. Atualizar a Tela
    pygame.display.flip()
    
    # 4.4. Controlar o FPS
    clock.tick(FPS)

pygame.quit()