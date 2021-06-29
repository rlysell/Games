import random
import pygame
from pygame import draw
import sys

#from time import sleep
#from random_word import RandomWords

#answers = RandomWords()

pygame.init()
pygame.time.Clock()
WIDTH = 1024
HEIGHT = 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
headline_font = pygame.font.SysFont("Arial", 44)
guess_font = pygame.font.SysFont("Times new Roman", 50)

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
answers = ["PROFESSOR", "PYTHON", "HANGMAN", "POLITICS", "PRESIDENT", "CONFLICT", "HOUSE", "DEMOCRATS", "SUMMER"]



game_close = False
game_over = True

def find_index(letter_guess, answer):
    return [i for i, letter in enumerate(answer) if letter == letter_guess ]

def write(text, x = WIDTH/2, y = HEIGHT/2, color = red, font = headline_font):
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center = (x, y))
    screen.blit(text, text_rect)
    return

def write_guess(guess, x = WIDTH/2, y = HEIGHT/2, color = blue, font = guess_font):
    text = ""
    for letter in guess:
        text += letter + " "
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center = (x, y))
    screen.blit(text, text_rect)
    return

def write_wrong_guesses(guess, x = WIDTH/16, y = 4/5*HEIGHT, color = blue, font = guess_font):
    text = ""
    for letter in guess:
        text += letter + "   "
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(bottomleft = (x, y))
    screen.blit(text, text_rect)
    return

def draw_buttons(text, x = WIDTH/2, y = HEIGHT/2, width = 100, height = 40, color = blue, font = headline_font):
    text = font.render(text, 1, pygame.Color(black))
    text_rect = text.get_rect(center = (x, y))
    l = x - width/2
    b = y - height/2
    draw.rect(screen, color, pygame.Rect(l, b, width, height))
    screen.blit(text, text_rect)
    r = l + width 
    t = b + height
    return l, b, r, t

def draw_hang(count):
    l = [WIDTH/2, WIDTH/2, 2*WIDTH/3]
    t = [HEIGHT/6, HEIGHT/6, HEIGHT/6]
    h = [HEIGHT*(0.6-1/6), 20, HEIGHT/4 - HEIGHT/6]
    w = [20, (2/3 - 1/2)*WIDTH, 20]
    arc_w = 300
    arc_h = 150
    for i in range(1, count + 1):
        if i == 1:
            draw.arc(screen, black, [(2*l[0] + w[0])/2 - arc_w/2, t[0]+h[0], arc_w, arc_h], 0, 3.14, width = 10)
        if i in range(2, 5):
            draw.rect(screen, black, pygame.Rect(l[i-2], t[i-2], w[i-2], h[i-2]))
        if i == 5:
            draw.circle(screen, black, center = (2/3*WIDTH + w[2]/2, 0.3*HEIGHT), radius = (0.3 - 1/4)*HEIGHT, width = 3)
        if i == 6:
            draw.rect(screen, black, pygame.Rect(2/3*WIDTH + w[2]/2, 0.3*HEIGHT + (0.3 - 1/4)*HEIGHT, 2, 60))
        if i == 7:
            draw.rect(screen, black, pygame.Rect(2/3*WIDTH + w[2]/2 - 20, 0.3*HEIGHT + 1.3*(0.3 - 1/4)*HEIGHT,40, 2))
        if i == 8:
            draw.line(screen, black, start_pos = (2/3*WIDTH + w[2]/2, 0.3*HEIGHT + 1.3*(0.3 - 1/4)*HEIGHT + 45), end_pos = (2/3*WIDTH + w[2]/2 - 30,0.3*HEIGHT + 1.3*(0.3 - 1/4)*HEIGHT + 75), width = 3)
        if i == 9:
            draw.line(screen, black, start_pos = (2/3*WIDTH + w[2]/2, 0.3*HEIGHT + 1.3*(0.3 - 1/4)*HEIGHT + 45), end_pos = (2/3*WIDTH + w[2]/2 + 30,0.3*HEIGHT + 1.3*(0.3 - 1/4)*HEIGHT + 75), width = 3)


while not game_close:
    mouse = pygame.mouse.get_pos()
    screen.fill(white)
    write("Welcome to Hangman!", y = HEIGHT/4)
    l, b, r, t = draw_buttons("Play!", y = HEIGHT/2 + HEIGHT/16, height = 60)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if l <= mouse[0] <= r and b <= mouse[1] <= t:
                game_over = False
                answer = random.choice(answers)
                guess = []
                wrong_guesses = []
                correct_guesses = []
                count = 0
                for letters in answer:
                    guess.append("_")
        if event.type == pygame.QUIT:
            game_close = True
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
                game_over = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_a, pygame.K_z + 1):
                    letter = event.unicode
                    letter = letter.upper()
                    if letter in wrong_guesses or letter in correct_guesses:
                        continue

                    if letter in answer:
                        correct_guesses.append(letter)
                        positions = find_index(letter, answer)
                        for position in positions:
                            guess[position] = letter
                    else:
                        wrong_guesses.append(letter)
                        count += 1
        screen.fill(white)
        draw_hang(count)
        write_guess(guess, y = 3/4*HEIGHT)
        write_wrong_guesses(wrong_guesses, y = 9/10*HEIGHT)
        pygame.display.update()

        if count == 9:
            screen.fill(white)
            game_over = True
            write("Game Over!!", y = 0.05*HEIGHT)
            write("The answer was " + answer, y = 0.75*HEIGHT)
            draw_hang(count)
        if ''.join(guess) == answer:
            screen.fill(white)
            game_over = True
            write("You got it!", y = HEIGHT/4)
            write_guess(guess)
        if game_over:
           write("Do you wish to play again?", y = 0.8*HEIGHT)
           ls, bs, rs, ts = draw_buttons("Play", x = WIDTH/4, y = 9/10*HEIGHT, height = 60)
           lq, bq, rq, tq = draw_buttons("Quit", x = 3*WIDTH/4, y = 9/10*HEIGHT, height = 60)
           pygame.display.update()
           while game_over and not game_close:
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_close = True
                        game_over = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ls <= mouse[0] <= rs and bs <= mouse[1] <= ts:
                            game_over = False
                            answer = random.choice(answers)
                            guess = []
                            wrong_guesses = []
                            correct_guesses = []
                            count = 0
                            for letters in answer:
                                guess.append("_")
                        elif lq <= mouse[0] <= rq and bq <= mouse[1] <= tq:
                            game_close = True
                            pygame.quit()
                            sys.exit()
                        