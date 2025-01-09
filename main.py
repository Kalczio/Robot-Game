import pygame
import random
import math

class Robotti:
    def __init__(self, kuva_tiedosto, leveys, korkeus) -> None:
        self.kuva = pygame.image.load(kuva_tiedosto)
        self.x = 0
        self.y = korkeus - self.kuva.get_height()
        self.leveys = leveys
        self.korkeus = korkeus
        self.oikealle = False
        self.vasemmalle = False
        self.nopeus_y = 0
        self.on_maassa = True

    def liikuta(self):
        if self.oikealle and self.x + self.kuva.get_width() < self.leveys:
            self.x += 4
        if self.vasemmalle and self.x > 0:
            self.x -= 4

        self.nopeus_y += 0.5
        self.y += self.nopeus_y

        if self.y > self.korkeus - self.kuva.get_height():
            self.y = self.korkeus - self.kuva.get_height()
            self.nopeus = 0
            self.on_maassa = True
    
    def piirra(self, naytto):
        naytto.blit(self.kuva, (self.x, self.y))
    
    def kasittele_tapahtuma(self, tapahtuma):
        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_LEFT:
                self.vasemmalle = True
            if tapahtuma.key == pygame.K_RIGHT:
                self.oikealle = True
            if tapahtuma.key == pygame.K_UP and self.on_maassa:
                self.nopeus_y = -12
                self.on_maassa = False
        elif tapahtuma.type == pygame.KEYUP:
            if tapahtuma.key == pygame.K_LEFT:
                self.vasemmalle = False
            if tapahtuma.key == pygame.K_RIGHT:
                self.oikealle = False

class Kolikko:
    def __init__(self, kuva_tiedosto, leveys, korkeus):
        self.kuva = pygame.image.load(kuva_tiedosto)
        self.korkeus = korkeus
        self.leveys = leveys
        self.resetoi()
    
    def resetoi(self):
        self.x = random.randint(0, self.leveys - self.kuva.get_width())
        self.y = -self.kuva.get_height()
        self.nopeus = random.randint(1, 1)
    
    def paivita(self):
        self.y += self.nopeus

    def piirra(self, naytto):
        naytto.blit(self.kuva, (self.x, self.y))
    
    def osuma(self, robotti):
        kolikon_keskipiste = (
            self.x + self.kuva.get_width() / 2,
            self.y + self.kuva.get_height() / 2
        )
        robotin_keskipiste = (
            robotti.x + robotti.kuva.get_width() / 2,
            robotti.y + robotti.kuva.get_height() / 2
        )
        etaisyys = math.sqrt(
            (kolikon_keskipiste[0] - robotin_keskipiste[0]) ** 2 + 
            (kolikon_keskipiste[1] - robotin_keskipiste[1]) ** 2
        )
        kolikon_sade = self.kuva.get_width() / 2
        robotin_sade = robotti.kuva.get_width() / 2

        return etaisyys < (kolikon_sade + robotin_sade)

class Hirvio:
    def __init__(self, kuva_tiedosto, leveys, korkeus):
        self.kuva = pygame.image.load(kuva_tiedosto)
        self.leveys = leveys
        self.korkeus = korkeus
        self.resetoi()

    def resetoi(self):
        if random.choice([True, False]):
            self.x = 0
            self.nopeus = random.randint(1, 1)
        else:
            self.x = self.leveys - self.kuva.get_width()
            self.nopeus = -random.randint(1, 1)
        
        self.y = self.korkeus - self.kuva.get_height()
    
    def paivita(self):
        self.x += self.nopeus

        if self.x < -self.kuva.get_width() or self.x > self.leveys:
            self.resetoi()

    def piirra(self, naytto):
        naytto.blit(self.kuva, (self.x, self.y))

    def osuma(self, robotti):
        hirvion_maski = pygame.mask.from_surface(self.kuva)
        robotin_maski = pygame.mask.from_surface(robotti.kuva)

        offset = (
            int(self.x - robotti.x),
            int(self.y - robotti.y)
        )
        osuma_piste = hirvion_maski.overlap(robotin_maski, offset)

        return osuma_piste is not None

def main():
    pygame.init()
    naytto = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Kolikkojahti")
    kello = pygame.time.Clock()
    fontti = pygame.font.SysFont("Arial", 24)

    

    robotti = Robotti("robo.png", 640, 480)
    kolikko_kuva = "kolikko.png"
    hirvio_kuva = "hirvio.png"
    hirviot = []
    kolikot = []
        
    pisteet = 0

    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            robotti.kasittele_tapahtuma(tapahtuma)

        if random.random() < (0.01):
            kolikot.append(Kolikko(kolikko_kuva, 640, 480))
        
        for kolikko in kolikot[:]:
            kolikko.paivita()
            if kolikko.osuma(robotti):
                pisteet += 1
                kolikot.remove(kolikko)
            if kolikko.y > 480:
                naytto.fill((0, 0, 0))
                lopetus_teksti = fontti.render(f"Peli päättyi! Sait {pisteet} pistettä!", True,(255, 0, 0))
                naytto.blit(lopetus_teksti, (200, 240))
                pygame.display.flip()
                pygame.time.wait(2000)
                exit()

        if random.random() < (0.002):
            hirviot.append(Hirvio(hirvio_kuva, 640, 480))

        for hirvio in hirviot[:]:
            hirvio.paivita()
            if hirvio.osuma(robotti):
                naytto.fill((0, 0, 0))
                lopetus_teksti = fontti.render(f"Peli päättyi! Sait {pisteet} pistettä!", True,(255, 0, 0))
                naytto.blit(lopetus_teksti, (200, 240))
                pygame.display.flip()
                pygame.time.wait(2000)
                exit()
        if pisteet == 10:
            naytto.fill((0, 0, 0))
            voitto_teksti = fontti.render(f"Jahti päättyi. Sait {pisteet} pistettä! Onnea!", True, (255, 255, 0))
            naytto.blit(voitto_teksti, (200, 240))
            pygame.display.flip()
            pygame.time.wait(2000)
            exit()

        robotti.liikuta()
        naytto.fill((50, 50, 100))
        robotti.piirra(naytto)
        for kolikko in kolikot:
            kolikko.piirra(naytto)
        for hirvio in hirviot:
            hirvio.piirra(naytto)
        
        piste_teksti = fontti.render(f"Pisteet: {pisteet} / 10", True, (255, 0, 0))
        naytto.blit(piste_teksti, (520, 10))

        pygame.display.flip()
        kello.tick(60)
        
        

main()