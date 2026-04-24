import pygame
import random

pygame.init()

tela = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Jogo de Flashcards - Trabalho Alessandro")

fundo = pygame.image.load("sala.jpg")
fundo = pygame.transform.scale(fundo, (800, 800))

flashcards = [
    {"pergunta": "No conjunto 2, 4, 6 e 8, a média é 5.", "correta": True},
    {"pergunta": "No conjunto 10, 20 e 30, a média é 25.", "correta": False},
    {"pergunta": "No conjunto 1, 3, 5, 7, 9, a mediana é 5.", "correta": True},
    {"pergunta": "No conjunto 2, 4, 6, 8, a mediana é 6.", "correta": False},
    {"pergunta": "No conjunto 1, 2, 2, 3, 3, a moda é 2 e 3.", "correta": True},
    {"pergunta": "No conjunto 4, 5, 6, 7, não existe moda.", "correta": True},
    {"pergunta": "No conjunto 5, 7 e 9, a média é 8.", "correta": False},
    {"pergunta": "No conjunto 3, 6, 9, 12, a média é 7.5.", "correta": True},
    {"pergunta": "No conjunto 1, 2, 3, 4, 100, a mediana é 3.", "correta": True},
    {"pergunta": "No conjunto 1, 2, 3, 4, 100, a média é 22.", "correta": True},
    {"pergunta": "No conjunto 2, 2, 2, 2, o desvio padrão é 0.", "correta": True},
    {"pergunta": "No conjunto 2, 4, 6, 8, o desvio padrão é 0.", "correta": False},
    {"pergunta": "No conjunto 1, 1, 10, 10, a média é 5.5.", "correta": True},
    {"pergunta": "No conjunto 1, 1, 10, 10, a mediana é 5.5.", "correta": True},
    {"pergunta": "A média sempre é igual à mediana.", "correta": False},
    {"pergunta": "A mediana não é afetada por valores extremos.", "correta": True},
    {"pergunta": "No conjunto 1, 2, 2, 3, a moda é 3.", "correta": False},
    {"pergunta": "No conjunto 7, 7, 7, 7, a moda é 7.", "correta": True},
    {"pergunta": "Quanto maior o desvio padrão, maior a dispersão dos dados.", "correta": True},
    {"pergunta": "O desvio padrão nunca pode ser zero.", "correta": False}
]

indice_atual = 0
estado = "inicio"
acertos = 0
erros = 0

botao_iniciar = pygame.Rect(300, 500, 200, 60)
botao_mostrar = pygame.Rect(300, 650, 200, 60)
botao_certo = pygame.Rect(150, 650, 200, 60)
botao_errado = pygame.Rect(450, 650, 200, 60)
botao_recomecar = pygame.Rect(300, 500, 200, 60)
botao_sair = pygame.Rect(300, 580, 200, 60)

def desenhar_texto_ajustado(texto, rect, cor=(0, 0, 0)):
    tamanho_fonte = 48

    while tamanho_fonte > 20:
        fonte = pygame.font.Font(None, tamanho_fonte)

        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste = linha_atual + palavra + " "
            largura, _ = fonte.size(teste)

            if largura <= rect.width - 40:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "

        linhas.append(linha_atual)

        altura_total = len(linhas) * fonte.get_height()

        if altura_total <= rect.height - 40:
            break

        tamanho_fonte -= 2

    y = rect.top + (rect.height - altura_total) // 2

    for linha in linhas:
        render = fonte.render(linha.strip(), True, cor)
        tela.blit(render, render.get_rect(center=(rect.centerx, y)))
        y += fonte.get_height()

def texto_centro(texto, rect, cor=(0, 0, 0)):
    fonte = pygame.font.Font(None, 40)
    render = fonte.render(texto, True, cor)
    tela.blit(render, render.get_rect(center=rect.center))

def resetar_jogo():
    global indice_atual, estado, acertos, erros
    indice_atual = 0
    estado = "pergunta"
    acertos = 0
    erros = 0
    random.shuffle(flashcards)

def desenhar():
    tela.blit(fundo, (0, 0))

    overlay = pygame.Surface((800, 800))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, 0))

    carta = pygame.Rect(100, 200, 600, 300)

    pygame.draw.rect(tela, (20, 20, 20), carta.move(5, 5), border_radius=15)
    pygame.draw.rect(tela, (240, 240, 240), carta, border_radius=15)

    if estado == "inicio":
        texto = "Bem-vindo ao jogo! Teste seus conhecimentos."
    elif estado != "fim":
        texto = flashcards[indice_atual]["pergunta"]
    else:
        texto = f"Fim! {acertos} acertos / {erros} erros"

    desenhar_texto_ajustado(texto, carta)

    if estado != "inicio":
        progresso = f"{min(indice_atual + 1, len(flashcards))}/{len(flashcards)}"
        fonte = pygame.font.Font(None, 36)
        tela.blit(fonte.render(progresso, True, (200, 200, 200)), (360, 50))

    if estado == "inicio":
        pygame.draw.rect(tela, (0, 120, 255), botao_iniciar, border_radius=10)
        texto_centro("INICIAR", botao_iniciar, (255, 255, 255))

    elif estado == "pergunta":
        pygame.draw.rect(tela, (0, 120, 255), botao_mostrar, border_radius=10)
        texto_centro("MOSTRAR", botao_mostrar, (255, 255, 255))

    elif estado == "resposta":
        pygame.draw.rect(tela, (0, 200, 100), botao_certo, border_radius=10)
        pygame.draw.rect(tela, (200, 50, 50), botao_errado, border_radius=10)

        texto_centro("CERTO", botao_certo, (255, 255, 255))
        texto_centro("ERRADO", botao_errado, (255, 255, 255))

    elif estado == "fim":
        pygame.draw.rect(tela, (0, 120, 255), botao_recomecar, border_radius=10)
        pygame.draw.rect(tela, (180, 40, 40), botao_sair, border_radius=10)

        texto_centro("RECOMEÇAR", botao_recomecar, (255, 255, 255))
        texto_centro("MENU", botao_sair, (255, 255, 255))

    pygame.display.flip()

rodando = True
while rodando:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            rodando = False

        if e.type == pygame.MOUSEBUTTONDOWN:

            if estado == "inicio":
                if botao_iniciar.collidepoint(e.pos):
                    resetar_jogo()

            elif estado == "pergunta":
                if botao_mostrar.collidepoint(e.pos):
                    estado = "resposta"

            elif estado == "resposta":
                if botao_certo.collidepoint(e.pos):
                    if flashcards[indice_atual]["correta"]:
                        acertos += 1
                    else:
                        erros += 1
                    indice_atual += 1

                elif botao_errado.collidepoint(e.pos):
                    if not flashcards[indice_atual]["correta"]:
                        acertos += 1
                    else:
                        erros += 1
                    indice_atual += 1

                if indice_atual >= len(flashcards):
                    estado = "fim"
                else:
                    estado = "pergunta"

            elif estado == "fim":
                if botao_recomecar.collidepoint(e.pos):
                    resetar_jogo()
                elif botao_sair.collidepoint(e.pos):
                    estado = "inicio"

    desenhar()

pygame.quit()