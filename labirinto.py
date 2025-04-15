import pygame
import random

# Definições
CELULA_LARGURA = 20
CELULA_ALTURA = 20
LARGURA = 20 * CELULA_LARGURA
ALTURA = 20 * CELULA_ALTURA
COR_PAREDE = (0, 0, 0)
COR_CAMINHO = (255, 255, 255)
COR_INICIO = (0, 255, 0)
COR_FIM = (255, 0, 0)
COR_SEM_SOLUCAO = (255, 0, 255)
COR_CAMINHO_SOLUCAO = (255, 165, 0)  # Laranja
FPS = 30

def criar_labirinto(altura, largura):
    """
    Gera um labirinto aleatório com entrada fixa (1, 0) e saída fixa (N-1, M-1).
    """
    labirinto = [[1 for _ in range(largura)] for _ in range(altura)]

    def furar_caminho(linha, coluna):
        labirinto[linha][coluna] = 0
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(direcoes)

        for dl, dc in direcoes:
            nova_linha, nova_coluna = linha + 2 * dl, coluna + 2 * dc
            if 0 < nova_linha < altura and 0 < nova_coluna < largura and labirinto[nova_linha][nova_coluna] == 1:
                labirinto[linha + dl][coluna + dc] = 0
                furar_caminho(nova_linha, nova_coluna)

    # Começar a geração a partir de um ponto próximo à entrada para tentar criar um caminho
    linha_inicial = 1
    coluna_inicial = 0
    furar_caminho(linha_inicial, coluna_inicial)

    # Garantir que a entrada e a saída sejam caminhos
    labirinto[1][0] = 0
    labirinto[altura - 1][largura - 1] = 0

    return labirinto

def desenhar_labirinto(tela, labirinto, inicio, fim, caminho=None, sem_solucao=False):
    altura = len(labirinto)
    largura = len(labirinto[0])

    for linha in range(altura):
        for coluna in range(largura):
            x = coluna * CELULA_LARGURA
            y = linha * CELULA_ALTURA
            rect = (x, y, CELULA_LARGURA, CELULA_ALTURA)
            if labirinto[linha][coluna] == 1:
                pygame.draw.rect(tela, COR_PAREDE, rect)
            elif (linha, coluna) == inicio:
                pygame.draw.rect(tela, COR_INICIO, rect)
            elif (linha, coluna) == fim:
                pygame.draw.rect(tela, COR_FIM, rect)
            elif caminho and (linha, coluna) in caminho:
                pygame.draw.rect(tela, COR_CAMINHO_SOLUCAO, rect)
            else:
                pygame.draw.rect(tela, COR_CAMINHO, rect)

    if sem_solucao:
        fonte = pygame.font.Font(None, 48)
        texto = fonte.render("Sem Solução!", True, COR_SEM_SOLUCAO)
        texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(texto, texto_rect)

def busca_forca_bruta(labirinto, inicio, fim, caminho_atual=None, visitados=None):
    if caminho_atual is None:
        caminho_atual = [inicio]
    if visitados is None:
        visitados = {inicio}

    if inicio == fim:
        return caminho_atual

    linha, coluna = inicio
    movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dl, dc in movimentos:
        nova_linha, nova_coluna = linha + dl, coluna + dc
        if 0 <= nova_linha < len(labirinto) and 0 <= nova_coluna < len(labirinto[0]) and \
           labirinto[nova_linha][nova_coluna] == 0 and (nova_linha, nova_coluna) not in visitados:
            novo_ponto = (nova_linha, nova_coluna)
            novo_caminho = caminho_atual + [novo_ponto]
            novos_visitados = visitados.union({novo_ponto})
            resultado = busca_forca_bruta(labirinto, novo_ponto, fim, novo_caminho, novos_visitados)
            if resultado:
                return resultado
    return None

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Labirinto 20x20 - Força Bruta")
    clock = pygame.time.Clock()
    pygame.font.init()

    altura = 20
    largura = 20
    labirinto = criar_labirinto(altura, largura)
    inicio = (1, 0)
    fim = (altura - 1, largura - 1)
    caminho_solucao = None
    sem_solucao_flag = False

    print(f"Ponto de Início: {inicio}")
    print(f"Ponto de Fim: {fim}")

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and caminho_solucao is None and not sem_solucao_flag:
                    print("Buscando solução por força bruta...")
                    caminho_solucao = busca_forca_bruta(labirinto, inicio, fim)
                    if caminho_solucao is None:
                        print("Nenhuma solução encontrada.")
                        sem_solucao_flag = True

        tela.fill(COR_CAMINHO)
        desenhar_labirinto(tela, labirinto, inicio, fim, caminho_solucao, sem_solucao_flag)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()