import numpy as np
import math

REDOVI = 6
STUPCI = 7
IGRAC = 1
AI = 2
PRAZNO = 0
DUZINA_PROZORA = 4

# Kreiranje ploce
def kreiraj_plocu():
    return np.zeros((REDOVI, STUPCI), dtype=int)

# Ubacivanje figure u plocu
def ubaci_figuru(ploca, red, stupac, figura):
    ploca[red][stupac] = figura

# Provjera je li stupac valjan
def je_valjana_lokacija(ploca, stupac):
    return ploca[REDOVI - 1][stupac] == 0

# Dohvati sljedeci slobodan red u stupcu
def sljedeci_slobodan_red(ploca, stupac):
    for r in range(REDOVI):
        if ploca[r][stupac] == 0:
            return r

# Evaluacija prozora duljine 4
def evaluiraj_prozor(prozor, figura):
    protivnik = IGRAC if figura == AI else AI
    score = 0

    if prozor.count(figura) == 4:  # Pobjednička linija
        score += 100
    elif prozor.count(figura) == 3 and prozor.count(PRAZNO) == 1:  # Tri figure i jedno prazno polje
        score += 10
    elif prozor.count(figura) == 2 and prozor.count(PRAZNO) == 2:  # Dvije figure i dva prazna polja
        score += 5

    if prozor.count(protivnik) == 3 and prozor.count(PRAZNO) == 1:  # Blokiranje protivnika
        score -= 80

    return score

# Evaluacija stanja ploče
def evaluiraj_stanje(ploca, figura):
    rezultat = 0

    # Horizontalno
    for r in range(REDOVI):
        redak = [ploca[r][c] for c in range(STUPCI)]
        for c in range(STUPCI - 3):
            prozor = redak[c:c + DUZINA_PROZORA]
            rezultat += evaluiraj_prozor(prozor, figura)

    # Vertikalno
    for c in range(STUPCI):
        stupac = [ploca[r][c] for r in range(REDOVI)]
        for r in range(REDOVI - 3):
            prozor = stupac[r:r + DUZINA_PROZORA]
            rezultat += evaluiraj_prozor(prozor, figura)

    # Dijagonalno (pozitivan nagib)
    for r in range(REDOVI - 3):
        for c in range(STUPCI - 3):
            prozor = [ploca[r + i][c + i] for i in range(DUZINA_PROZORA)]
            rezultat += evaluiraj_prozor(prozor, figura)

    # Dijagonalno (negativan nagib)
    for r in range(3, REDOVI):
        for c in range(STUPCI - 3):
            prozor = [ploca[r - i][c + i] for i in range(DUZINA_PROZORA)]
            rezultat += evaluiraj_prozor(prozor, figura)

    return rezultat

# Provjera uvjeta za pobjedu
def pobjednicki_potez(ploca, figura):
    # Provjera horizontalnih lokacija
    for r in range(REDOVI):
        for c in range(STUPCI - 3):
            if all(ploca[r][c + i] == figura for i in range(DUZINA_PROZORA)):
                return True

    # Provjera vertikalnih lokacija
    for c in range(STUPCI):
        for r in range(REDOVI - 3):
            if all(ploca[r + i][c] == figura for i in range(DUZINA_PROZORA)):
                return True

    # Provjera dijagonala s pozitivnim nagibom
    for r in range(REDOVI - 3):
        for c in range(STUPCI - 3):
            if all(ploca[r + i][c + i] == figura for i in range(DUZINA_PROZORA)):
                return True

    # Provjera dijagonala s negativnim nagibom
    for r in range(3, REDOVI):
        for c in range(STUPCI - 3):
            if all(ploca[r - i][c + i] == figura for i in range(DUZINA_PROZORA)):
                return True

    return False

# Provjera je li ploca puna
def je_krajnje_stanje(ploca):
    return pobjednicki_potez(ploca, IGRAC) or pobjednicki_potez(ploca, AI) or len(dohvati_valjane_lokacije(ploca)) == 0

# Dohvati valjane stupce
def dohvati_valjane_lokacije(ploca):
    return [c for c in range(STUPCI) if je_valjana_lokacija(ploca, c)]

# Odabir najboljeg stupca koristeci Minimax
def minimax(ploca, dubina, alfa, beta, maksimizirajuci_igrac):
    valjane_lokacije = dohvati_valjane_lokacije(ploca)
    je_kraj = je_krajnje_stanje(ploca)

    if dubina == 0 or je_kraj:
        if je_kraj:
            if pobjednicki_potez(ploca, AI):
                return (None, 100000000000000)
            elif pobjednicki_potez(ploca, IGRAC):
                return (None, -10000000000000)
            else:  # Kraj igre, nema vise valjanih poteza
                return (None, 0)
        else:  # Dubina je nula
            return (None, evaluiraj_stanje(ploca, AI))  # Evaluacija stanja

    if maksimizirajuci_igrac:
        vrijednost = -math.inf
        najbolji_stupac = None

        for stupac in valjane_lokacije:
            red = sljedeci_slobodan_red(ploca, stupac)
            kopija_ploce = ploca.copy()
            ubaci_figuru(kopija_ploce, red, stupac, AI)
            nova_vrijednost = minimax(kopija_ploce, dubina - 1, alfa, beta, False)[1]
            if nova_vrijednost > vrijednost:
                vrijednost = nova_vrijednost
                najbolji_stupac = stupac
            alfa = max(alfa, vrijednost)
            if alfa >= beta:
                break
        return najbolji_stupac, vrijednost

    else:  # Minimizirajuci igrac
        vrijednost = math.inf
        najbolji_stupac = None

        for stupac in valjane_lokacije:
            red = sljedeci_slobodan_red(ploca, stupac)
            kopija_ploce = ploca.copy()
            ubaci_figuru(kopija_ploce, red, stupac, IGRAC)
            nova_vrijednost = minimax(kopija_ploce, dubina - 1, alfa, beta, True)[1]
            if nova_vrijednost < vrijednost:
                vrijednost = nova_vrijednost
                najbolji_stupac = stupac
            beta = min(beta, vrijednost)
            if alfa >= beta:
                break
        return najbolji_stupac, vrijednost

# Ispis ploce
def ispisi_plocu(ploca):
    print(np.flip(ploca, 0))

# Glavna petlja igre
def igraj_igru():
    ploca = kreiraj_plocu()
    igra_gotova = False
    na_potezu = 0

    while not igra_gotova:
        # Potez igraca
        if na_potezu == 0:
            ispisi_plocu(ploca)
            stupac = int(input("Igrac 1, odaberi stupac (0-6): "))

            if je_valjana_lokacija(ploca, stupac):
                red = sljedeci_slobodan_red(ploca, stupac)
                ubaci_figuru(ploca, red, stupac, IGRAC)

                if pobjednicki_potez(ploca, IGRAC):
                    ispisi_plocu(ploca)
                    print("Igrac 1 pobjeđuje!")
                    igra_gotova = True

        # Potez AI-a
        else:
            stupac, minimax_bodovi = minimax(ploca, 4, -math.inf, math.inf, True)
            if je_valjana_lokacija(ploca, stupac):
                red = sljedeci_slobodan_red(ploca, stupac)
                ubaci_figuru(ploca, red, stupac, AI)

                if pobjednicki_potez(ploca, AI):
                    ispisi_plocu(ploca)
                    print("AI pobjeđuje!")
                    igra_gotova = True

        na_potezu += 1
        na_potezu %= 2

        if not igra_gotova:
            ispisi_plocu(ploca)

if __name__ == "__main__":
    igraj_igru()
