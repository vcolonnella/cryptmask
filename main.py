import random
import drawSvg as draw

nsq = 4
mw = 15
mh = 32
msg = [["PRIMA IL GELATO POI IL DENTISTA", "FATTI I CAPELLI ROSSI",
    "RIPARA LE TUE SCARPE", "AGGIUSTA MOTO E BICI"],
    ["IMPARA A GUIDARE", "LAVI E IGIENIZZI DA SOLO",
    "IL BAR DEL PARCO VICINO", "ARREDA LA TUA CASA"],
    ["VINO SFUSO FRESCO", "UN MARE DI SOLDI",
    "SPEDISCI PACCHI E LETTERE", "ODORE DI GIADA"],
    ["LIBRI E PENNE PER COPIARE", "IMPARA INGLESE CON AMICI",
    "TI ASSISTE IN PANNE", "STAMPA SU OGNI OGGETTO"]]
canvas = [[['_' for c1 in range(mw)] for c2 in range(mh)] for c3 in range(nsq)]

def printcanvas(c):
    out = ""
    for x in c:
        for y in x:
            out += y
        out+="\n"
    return out

def outtransf(arr, pos, mode):
    oy = int(pos / mw)
    ox = pos % mw
    if 'w' in mode:
        ox = mw - ox - 1
    if 'h' in mode:
        oy = mh - oy - 1
    return arr[oy][ox]

def outtransf_xy(pos, mode):
    oy = int(pos / mw)
    ox = pos % mw
    if 'w' in mode:
        ox = mw - ox - 1
    if 'h' in mode:
        oy = mh - oy - 1
    return [ox, oy]

def outtransf_idx(pos, mode):
    oy = int(pos / mw)
    ox = pos % mw
    if 'w' in mode:
        ox = mw - ox - 1
    if 'h' in mode:
        oy = mh - oy - 1
    return oy * mw + ox

fc = open("canvas.txt", "w")
fs = open("solution.txt", "w")
ff = open("nonsense.txt", "w")

# disponi msg su canvas tracciando le posizioni
# la distanza di ogni passo varia attorno alla distanza media su tutta la matrice (15 * 32 / length(msg))
# senza superare la media dello spazio restante
fal = [None] * nsq
msglen = [len(x) for y in range(len(msg[0])) for x in msg[y]]
sol = [[[-1 for c1 in range(max(msglen))] for c2 in range(len(msg[0]))] for c3 in range(nsq)]
for sq in range(nsq):
    #msglen = [len(x) for x in msg[sq]]
    #pos = [x[:] for x in [[-1] * max(msglen)] * len(msg[sq])]
    for j in range(len(msg[sq])):
        cvj = 0
        for x in range(len(msg[sq][j])):
            minstep = int(mw * mh / len(msg[sq][j]) * .75)
            maxstep = int(min(mw * mh / len(msg[sq][j]) * .95, (mw * mh) - cvj))
            step = random.randint(minstep, maxstep)
            cvj += step
            while canvas[sq][int(cvj / mw)][cvj % mw] != '_':
                cvj += 1
            sol[sq][j][x] = cvj
            canvas[sq][int(cvj / mw)][cvj % mw] = msg[sq][j][x]

# riempi lo spazio restante di caratteri casuali
    for y in range(mh):
        for x in range(mw):
            if canvas[sq][y][x] == '_':
                canvas[sq][y][x] = chr(65 + random.randint(0, 25))
    fc.write("--- Map {}\n".format(sq))
    fc.write("{}\n".format(printcanvas(canvas[sq])))

# costruisci maschere spurie distinte da posizioni
    fal[sq] = []
    for x in range(2):
        falr = []
        for y in range(random.randint(16, 24)):
            falr.append(random.randint(0, mw * mh - 1))
        fal[sq].append(falr)

# verifica tutte le disposizioni delle maschere solutive producendo il relativo output
fs.write("--- Solution")
for sq in range(nsq):
    for k, o in enumerate(sol[sq]):
        v1 = v2 = v3 = v4 = ''
        for i in o:
            if i != -1:
                #print("{}, ".format(i))
                v1 += outtransf(canvas[sq], i, '')
                v2 += outtransf(canvas[sq], i, 'w')
                v3 += outtransf(canvas[sq], i, 'h')
                v4 += outtransf(canvas[sq], i, 'wh')
        fs.write("{}\n{}\n{}\n{}\n".format(v1, v2, v3, v4))

# verifica tutte le disposizioni spurie di maschere producendo il relativo output
ff.write("--- Check false")
for sk in range(nsq):
    for sq in range(nsq):
        for k, o in enumerate(fal[sk]):
            v1 = v2 = v3 = v4 = ''
            for i in o:
                if i != -1:
                    #print("{}, ".format(i), end='')
                    v1 += outtransf(canvas[sq], i, '')
                    v2 += outtransf(canvas[sq], i, 'w')
                    v3 += outtransf(canvas[sq], i, 'h')
                    v4 += outtransf(canvas[sq], i, 'wh')
            ff.write("{}\n{}\n{}\n{}\n".format(v1, v2, v3, v4))

fc.close()
fs.close()
ff.close()

# draw canvas
bo=[[9, 9], [102, 9], [195, 9]]
d = draw.Drawing(297, 210, origin=[0, 0])
d.setRenderSize(3465,2450)
for roc in range(len(canvas)):
#for roc in range(3):
    ro = roc % 3
    r = draw.Rectangle(bo[ro][0], bo[ro][1], 90, 192, fill='transparent', stroke='#333333', stroke_width=0.2)
    d.append(r)
    for cy in range(mh):
        for cx in range(mw):
            c = draw.Circle(bo[ro][0] + 3 + 6 * cx, bo[ro][1] + 3 + 6 * (mh - cy - 1), 3, fill='transparent', stroke='#333333', stroke_width=0.2)
            d.append(c)
            t = draw.Text(canvas[roc][cy][cx], 4, bo[ro][0] + 3 + 6 * cx, bo[ro][1] + 3.3 + 6 * (mh - cy - 1), center=True, fill='black', stroke='transparent')
            d.append(t)
    if ro == 2:
        d.savePng('canvas{}.png'.format(roc))
        d.clear()
if ro != 2:
    d.savePng('canvas{}.png'.format(roc))
    d.clear()

# draw solution masks
mode = ['', 'w', 'h', 'wh']
for c3 in range(nsq):
    for c2 in range(len(sol[c3])):
        roc = len(sol[0]) * c3 + c2
        ro = roc % 3
        r = draw.Rectangle(bo[ro][0], bo[ro][1], 90, 192, fill='transparent', stroke='#FF0000', stroke_width=0.2)
        d.append(r)
        th = draw.Text("S-{}.{}".format(c3, c2), 3, bo[ro][0], bo[ro][1] - 5, fill='black', stroke='transparent')
        d.append(th)
        for c1 in range(len(sol[c3][c2])):
            if sol[c3][c2][c1] != -1:
                cc = outtransf_xy(sol[c3][c2][c1], mode[(c2 + c3) % 4])
                c = draw.Circle(bo[ro][0] + 3 + 6 * cc[0], bo[ro][1] + 3 + 6 * (mh - cc[1] - 1), 3, fill='transparent', stroke='#FF0000', stroke_width=0.2)
                d.append(c)
        if ro == 2:
            d.savePng('solution{}_{}.png'.format(c3, c2))
            d.clear()
if ro != 2:
    d.savePng('solution{}_{}.png'.format(c3, c2))
    d.clear()

# draw nonsense masks
for c3 in range(nsq):
    for c2 in range(len(fal[c3])):
        roc = len(fal[0]) * c3 + c2
        ro = roc % 3
        r = draw.Rectangle(bo[ro][0], bo[ro][1], 90, 192, fill='transparent', stroke='#FF0000', stroke_width=0.2)
        d.append(r)
        for c1 in range(len(fal[c3][c2])):
            if fal[c3][c2][c1] != -1:
                cc = outtransf_xy(fal[c3][c2][c1], '')
                c = draw.Circle(bo[ro][0] + 3 + 6 * cc[0], bo[ro][1] + 3 + 6 * (mh - cc[1] - 1), 3, fill='transparent', stroke='#FF0000', stroke_width=0.2)
                d.append(c)
        if ro == 2:
            d.savePng('nonsense{}_{}.png'.format(c3, c2))
            d.clear()
if ro != 2:
    d.savePng('nonsense{}_{}.png'.format(c3, c2))
    d.clear()

