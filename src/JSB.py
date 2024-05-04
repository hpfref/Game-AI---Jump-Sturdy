import pygame as pg
import zuggenerator as gen


def sz2xy(sz):
  return sz[0]*FELD, sz[1]*FELD
def xy2sz(xy):
  return xy[0]//FELD, xy[1]//FELD


def board2fen(board, zugrecht):
    fen = ''
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for z in range(7, -1, -1):
        empty_count = 0
        row_fen = ''
        for s in range(8):
            if (s, z) in special_fields:
                continue  # Ignoriere spezielle Felder bei der FEN-Generierung
            piece = board[z][s]
            if piece == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    row_fen += str(empty_count)
                    empty_count = 0
                if piece == 'b':  # Spezialfall für bluepawn
                    row_fen += 'b0'
                elif piece == 'r':  # Spezialfall für bluepawn
                    row_fen += 'r0'
                else:
                    row_fen += piece  # Normales Hinzufügen von Figuren
        if empty_count > 0:
            row_fen += str(empty_count)
        fen += row_fen
        if z != 0:
            fen += '/'
    fen += ' ' + zugrecht
    return fen

def fen2board(fen):
    board = [["" for _ in range(8)] for _ in range(8)]
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for field in special_fields:
        board[field[1]][field[0]] = "X"

    s, z = 0, 7
    figurenstellung, zugrecht = fen.split()
    i = 0
    while i < len(figurenstellung):
        if (s, z) in special_fields:
            s += 1  # Überspringe das Setzen von Figuren in speziellen Feldern
            continue



        char = figurenstellung[i]

        if char.isalpha():
            if i + 1 < len(figurenstellung):
                next_char = figurenstellung[i + 1]
                if char == next_char:
                    piece = char + next_char
                    board[z][s] = piece
                    i += 1
                elif (char == 'r' and next_char == '0') or (char == 'b' and next_char == '0'):
                    piece = 'r' if char == 'r' else 'b'
                    board[z][s] = piece
                    i += 1
                elif (char == 'r' and next_char == 'b') or (char == 'b' and next_char == 'r'):
                    piece = 'rb' if char == 'r' else 'br'
                    board[z][s] = piece
                    i += 1
            else:
                board[z][s] = char
            s += 1

        elif char.isdigit():
            s += int(char)
        elif char == '/':
            z -= 1
            s = 0
        i += 1
    return board, zugrecht

def ladeFiguren():
    bilder = {}
    fig2datei = {
        'r': 'redpawn', 'b': 'bluepawn', 'rr': 'redtower', 'bb': 'bluetower',
        'br': 'rotaufblau', 'rb': 'blauaufrot'
    }
    for fig, datei in fig2datei.items():
        bild = pg.image.load(f'graphics/{datei}.png')
        bilder[fig] = pg.transform.smoothscale(bild, (FELD, FELD))
    return bilder

def zeichneBrett(board):
    for z in range(8):
        for s in range(8):
            farbe = '#DFBF93' if (s + z) % 2 == 0 else '#C5844E'
            if board[z][s] == "X":
                farbe = (0,0,0)  # Rote Farbe für unbenutzbare Felder
            pg.draw.rect(fenster, farbe, (*sz2xy((s, z)), FELD, FELD))
def zeichneFiguren(board):
    for z in range(8):
        for s in range(8):
            fig = board[z][s]
            if fig == "X":  # Überspringe das Zeichnen für spezielle Felder
                continue
            if fig:  # Prüft, ob das Feld nicht leer ist
                fenster.blit(FIGUREN[fig], sz2xy((s, z)))

pg.init()
größe = breite, höhe = 800, 800
FELD = breite // 8
FPS = 40
fenster = pg.display.set_mode(größe)
BRETT = [["" for _ in range(8)] for _ in range(8)]
for z in range(8):
    for s in range(8):
        if (s, z) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            BRETT[z][s] = "X"
        else:
            BRETT[z][s] = ""
fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
fen1 = '3b02/2bb2b02/5b0bb1/2r0b04/2rb3b01/1rr1rr2r0r0/5r02/2rr3 b'
FIGUREN = ladeFiguren()
board, zugrecht = fen2board(fen1)
fen2= board2fen(board, zugrecht)
print(board)
print(fen2)
weitermachen = True
clock = pg.time.Clock()
drag = None



while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
        weitermachen = False
    elif ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
        von = xy2sz(pg.mouse.get_pos())
        if board[von[1]][von[0]]:  # Zugriff auf das 2D-Array
            fig = board[von[1]][von[0]]
            drag = FIGUREN[fig]
            board[von[1]][von[0]] = ''  # Löscht die Figur von der Startposition
        elif ereignis.type == pg.MOUSEBUTTONUP and drag:
            zu = xy2sz(pg.mouse.get_pos())
            board[zu[1]][zu[0]] = fig  # Setzt die Figur auf die neue Position
            drag = None

  fenster.fill((0, 0, 0))
  zeichneBrett(BRETT)
  zeichneFiguren(board)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    fenster.blit(drag, rect)
  pg.display.flip()

pg.quit()

#a