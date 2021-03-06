import pygame
import sys

import setuptools_scm

from bullet import Bullet
from alien import Alien
import time

def events(screen, ship, bullets):
    """управление кораблём"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                ship.mright = True
            if event.key == pygame.K_a:
                ship.mleft = True
            if event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, ship)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                ship.mright = False
            if event.key == pygame.K_a:
                ship.mleft = False

def update(bg_color, screen, stats, sc, ship, aliens, bullets):
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.output()
    aliens.draw(screen)
    pygame.display.flip()

def update_bullets(screen, stats, sc, bullets, aliens):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += 10 * len(aliens)
        sc.image_score()
        sc.image_lifes()
        check_hscore(stats, sc)
    if len(aliens) == 0:
        bullets.empty()
        create_army(screen, aliens)

def ship_dest(stats, sc, screen, ship, aliens, bullets):

    if stats.lifes > 0:

        stats.score = 0
        sc.image_score()
        stats.lifes -= 1
        sc.image_lifes()
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens)
        ship.create_ship()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()

def update_aliens(stats, sc, screen, ship, aliens, bullets):
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_dest(stats, sc, screen, ship, aliens, bullets)
    aliens_check(stats, sc, screen, ship, aliens, bullets)

def aliens_check(stats, sc, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            ship_dest(stats, sc, screen, ship, aliens, bullets)
            break

def create_army(screen, aliens):

    alien = Alien(screen)
    alien_width = alien.rect.width
    alien_hight = alien.rect.height

    number_alien_x = int((500 - 2 * alien_width) / alien_width)
    number_alien_y = 3
    for row_number in range(number_alien_y ):
        for alien_number in range (number_alien_x):
            alien = Alien(screen)
            alien.x = alien_width + alien_width * alien_number
            alien.y = alien_hight + alien_hight * row_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + alien.rect.height * row_number
            aliens.add(alien)

def check_hscore(stats, sc):
    if stats.score > stats.hscore:
        stats.hscore = stats.score
        sc.image_hscore()