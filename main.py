import smtplib

import pyttsx3
import datetime
import pywhatkit
import wikipedia
import webbrowser
import os
import pyjokes
import PyPDF2
import speech_recognition as sr
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from jarvisui import Ui_JarvisUi
from tkinter import *
from pygame.locals import *
import googletrans
import textblob
import yagmail
from email.message import EmailMessage
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)
global command

def takecommand():
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("listening...")
			r.pause_threshold = 1
			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)
		try:
			print("Recognizing...")
			query = r.recognize_google(audio, language='en-in')
			print(f"user said: {query}")

		except Exception as e:
			# speak("Say that again Please...")
			return "none"

		query = query.lower()
		return query

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)

def CarGame():
    import pygame
    import random

    # shape parameters
    size = width, height = (800, 800)
    road_w = int(width / 1.6)
    roadmark_w = int(width / 80)
    # location parameters
    right_lane = width / 2 + road_w / 4
    left_lane = width / 2 - road_w / 4
    # animation parameters
    speed = 1

    # initiallize the app
    pygame.init()
    running = True

    # set window size
    screen = pygame.display.set_mode(size)
    # set window title
    pygame.display.set_caption("Mariya's car game")
    # set background colour
    screen.fill((60, 220, 0))
    # apply changes
    pygame.display.update()

    # load player vehicle
    car = pygame.image.load("car.png")
    # resize image
    # car = pygame.transform.scale(car, (250, 250))
    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.8

    # load enemy vehicle
    car2 = pygame.image.load("otherCar.png")
    car2_loc = car2.get_rect()
    car2_loc.center = left_lane, height * 0.2

    counter = 0
    # game loop
    while running:
        counter += 1

        # increase game difficulty overtime
        if counter == 5000:
            speed += 0.15
            counter = 0
            print("level up", speed)

        # animate enemy vehicle
        car2_loc[1] += speed
        if car2_loc[1] > height:
            # randomly select lane
            if random.randint(0, 1) == 0:
                car2_loc.center = right_lane, -200
            else:
                car2_loc.center = left_lane, -200

        # end game logic
        if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 250:
            print("GAME OVER! YOU LOST!")
            break

        # event listeners
        for event in pygame.event.get():
            if event.type == QUIT:
                # collapse the app
                running = False
            if event.type == KEYDOWN:
                # move user car to the left
                if event.key in [K_a, K_LEFT]:
                    car_loc = car_loc.move([-int(road_w / 2), 0])
                # move user car to the right
                if event.key in [K_d, K_RIGHT]:
                    car_loc = car_loc.move([int(road_w / 2), 0])

        # draw road
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (width / 2 - road_w / 2, 0, road_w, height))
        # draw centre line
        pygame.draw.rect(
            screen,
            (255, 240, 60),
            (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
        # draw left road marking
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
        # draw right road marking
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))

        # place car images on the screen
        screen.blit(car, car_loc)
        screen.blit(car2, car2_loc)
        # apply changes
        pygame.display.update()

    # collapse application window
    pygame.quit()

def SnowBall():
    import pygame
    from pygame.math import Vector2
    from pygame import mixer
    import time
    import random
    import math

    # 0 = Menu, 1 = Game, 2 = Quit
    game_state = 0
    score = 0
    score_int = 0
    max_score = 0

    entities_alive = []

    class Player():
        global game_state
        # Transform
        position = pygame.Vector2()
        scale = pygame.Vector2()

        # Physics
        velocity_y = 0
        gravity_scale = 3000
        jump_force = 2000
        speed = 400
        is_grounded = False

        # Graphics
        player_sprite = 0
        rotation = 0
        rot_speed = 400

        scale_speed = 3

        player_collider = 0

        def __init__(self, desired_scale_x, desired_scale_y, Width, Height):
            self.scale.x = desired_scale_x
            self.scale.y = desired_scale_y

            self.scalar = 50

            self.player_sprite = pygame.sprite.Sprite()
            self.player_sprite.image = pygame.image.load("Data/Textures/Snowball.png").convert_alpha()
            self.player_sprite.rect = self.player_sprite.image.get_rect()
            self.player_sprite.image = pygame.transform.scale(self.player_sprite.image,
                                                              (int(self.scale.x), int(self.scale.y)))

            self.position.x = Width / 2
            self.position.y = Height / 2

            self.scalar = self.scale.x

        def move(self, keys, dt):
            global score_int
            global score
            global max_score

            if (keys[0]):
                self.position.x -= 0.01 * dt * self.speed
                self.rotation += 0.01 * dt * self.rot_speed
            if (keys[1]):
                self.position.x += 0.01 * dt * self.speed
                self.rotation -= 0.01 * dt * self.rot_speed
            if (keys[2] and self.is_grounded):
                self.velocity_y -= 0.01 * dt * self.jump_force

            self.velocity_y += 0.00001 * dt * self.gravity_scale

            self.position.y += self.velocity_y * dt

            self.player_sprite.rect.topleft = self.position.x, self.position.y

            # Scale The Snowball

            if (self.scalar < 12):
                game_state = 0
                if (score > max_score):
                    max_score = score
                # score = 0
                # score_int = 0

            else:
                self.scalar -= 0.01 * dt * self.scale_speed

        def draw(self, screen, color, dt, colliders):
            img_copy = pygame.transform.scale(self.player_sprite.image, (int(self.scalar), int(self.scalar)))
            img_copy = pygame.transform.rotate(img_copy, self.rotation)
            self.collisions(colliders, img_copy.get_height())
            screen.blit(img_copy, (
                self.position.x - int(img_copy.get_width() / 2),
                self.position.y - int(img_copy.get_height() / 2)))

        def collisions(self, colliders, scale):
            # Top of box
            self.is_grounded = False
            for i in range(len(colliders)):
                if (self.position.y - int(scale / 2) >= colliders[i].top - scale and colliders[
                    i].typeof == "environment"):
                    self.is_grounded = True
                    self.position.y = colliders[i].top - int(scale / 2) + 5
                    self.velocity_y = 0
                if (self.position.x + int(self.player_sprite.image.get_width() / 2) >= 720):
                    self.position.x = 720 - int(self.player_sprite.image.get_width() / 2)
                if (self.position.x - int(self.player_sprite.image.get_width() / 2) <= 0):
                    self.position.x = 0 + int(self.player_sprite.image.get_width() / 2)

    class Box_Collider():
        position = Vector2()
        scale = Vector2()

        top = 0
        right = 0
        left = 0
        down = 0

        typeof = "default"

        def __init__(self, desired_position_x, desired_position_y, desired_scale_x, desired_scale_y, typeof):
            self.position.x = desired_position_x
            self.position.y = desired_position_y
            self.scale.x = desired_scale_x
            self.scale.y = desired_scale_y
            self.typeof = typeof

            self.top = self.position.y - self.scale.y / 2
            self.right = self.position.x + self.scale.x / 2
            self.left = self.position.x - self.scale.x / 2
            self.down = self.position.y + self.scale.y / 2

        def draw(self, screen, color):
            pygame.draw.rect(screen, color, (self.position.x, self.position.y, self.scale.x, self.scale.y))

    class Entity():
        tag = "Default"
        bottom = 0

        entity_color = (0, 0, 0)
        sound = 0

        radius = 0

        right = 0
        left = 0

        def __init__(self):
            self.position = None

        def move(self, dt):
            self.position.y += dt * self.speed
            self.bottom = self.position.y + (self.radius * 2)
            self.right = self.position.x + (self.radius * 2)
            self.left = self.position.x

        def collisions(self, enemies):
            if (self.position.y > 390):
                enemies.remove(self)
                enemies = enemies[:-1]
                self.sound.play()

        def initialiser(self, color, sfx_path):
            self.entity_color = color
            self.sound = mixer.Sound(sfx_path)

        def draw(self, screen):
            pygame.draw.circle(screen, self.entity_color, (self.position.x, self.position.y), self.radius)

    class Enemy(Entity):
        def __init__(self):
            self.speed = random.randrange(1, 5)
            self.position = Vector2()
            self.position.x = random.randrange(0, 720)
            self.position.y = 0

            self.initialiser((102, 107, 102), "Data/Sounds/RockHit.wav")

            self.tag = "enemy"

            self.radius = random.randrange(10, 30)

    class Snowball(Entity):
        def __init__(self):
            self.speed = random.randrange(1, 5)
            self.position = Vector2()
            self.position.x = random.randrange(0, 720)
            self.position.y = 0
            self.initialiser((255, 255, 255), "Data/Sounds/SnowballHit.wav")
            self.tag = "snowball"

            self.radius = random.randrange(10, 30)

    class Spawner():
        global game_state
        global entities_alive
        total_enemies_spawned = 0
        time_elapsed = 0
        screen = 0
        time_between_spawns = 100
        concurrent_enemys = 0

        sound = 0

        def __init__(self, screen):
            self.screen = screen
            self.sound = mixer.Sound("Data/Sounds/SnowballPowerup.wav")

        def check_for_player(self, player, scalar):
            global game_state
            global score_int
            global score
            global max_score
            for i in range(len(entities_alive)):
                try:
                    if (entities_alive[i].bottom > 380 + 50 - scalar):
                        if (entities_alive[i].position.x > player.position.x - player.scale.x and
                                entities_alive[i].position.x < player.position.x + player.scale.x):
                            if (entities_alive[i].tag == "enemy"):
                                game_state = 0
                                if (score > max_score):
                                    max_score = score
                                # score = 0
                                # score_int = 0
                            else:
                                score += 5
                                player.scalar = 50
                                self.sound.play()
                                entities_alive.remove(entities_alive[i])
                except:
                    pass

        def set_time_between_spawns(self, time_between_spawns):
            self.time_between_spawns = time_between_spawns

        def draw_enemies(self, dt):
            for i in range(len(entities_alive)):
                try:
                    entities_alive[i].draw(self.screen)
                    entities_alive[i].move(dt)
                    entities_alive[i].collisions(entities_alive)
                except:
                    pass

        def timer(self, dt):
            self.time_elapsed += dt

        def spawner(self):
            if (self.time_elapsed >= self.time_between_spawns):
                random_int = random.randint(0, 4)
                if (random_int != 0 and self.concurrent_enemys < 3):
                    entity = Enemy()
                    self.concurrent_enemys += 1
                else:
                    entity = Snowball()
                    self.concurrent_enemys = 0
                entities_alive.append(entity)

                self.time_elapsed = 0

    class Particle():
        def __init__(self):
            self.position = Vector2()
            self.position.x = random.randrange(0, 720)
            self.position.y = 0
            self.size = random.randrange(0, 15)
            self.color = (255, 255, 255)
            self.speed = random.randrange(20, 50)

        def move(self, dt):
            self.position.y += 0.01 * dt * self.speed

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, self.size, self.size))

        def collision(self, particles):
            if (self.position.y > 390):
                particles.remove(self)

    class Main():
        global game_state
        previous_frame_time = 0
        dt = 0
        elapsed_time = 0
        time_between_spawns = 100

        def calculate_deltatime(self):
            self.dt = time.time() - self.previous_frame_time
            self.dt *= 60
            self.previous_frame_time = time.time()

        def difficulty(self):
            self.elapsed_time += self.dt
            if (self.elapsed_time > 1000):
                self.time_between_spawns /= 1.45
                self.elapsed_time = 0

        def handle_inputs(self, keys, event):
            if (event.type == pygame.KEYDOWN):
                if (event.key == K_a):
                    keys[0] = True
                if (event.key == K_d):
                    keys[1] = True
                if (event.key == K_w):
                    keys[2] = True
            if (event.type == pygame.KEYUP):
                if (event.key == K_a):
                    keys[0] = False
                if (event.key == K_d):
                    keys[1] = False
                if (event.key == K_w):
                    keys[2] = False

        def setup_pygame(self, title, width, height):
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
            favicon = pygame.image.load("Data/Textures/Favicon.png").convert_alpha()
            pygame.display.set_icon(favicon)
            pygame.init()
            return screen

        def update_score(self, screen, text):
            global score_int
            global score
            score += self.dt / 100
            score_int = int(score)
            score_text = text.render("SCORE: " + str(score_int), True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

        def draw_colliders(self, colliders, screen, color, width, height):
            for i in range(len(colliders)):
                colliders[i].draw(screen, color, width, height)

        def reset_state(self):
            self.previous_frame_time = 0
            self.dt = 0
            self.elapsed_time = 0
            self.time_between_spawns = 100
            self.score_int = 0

        def game(self, screen, font, WIDTH, HEIGHT):
            global game_state

            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)

            #         A      D    Space
            self.previous_frame_time = time.time()

            keys = [False, False, False]

            player = Player(40, 40, WIDTH, HEIGHT)

            colliders = []

            # Constant Sprites
            foreground = pygame.sprite.Sprite()
            foreground.image = pygame.image.load("Data/Textures/Foreground.png").convert_alpha()
            foreground.rect = foreground.image.get_rect()
            foreground.rect.topleft = 0, HEIGHT - 480
            foreground.image = pygame.transform.scale(foreground.image, (720, 480))
            foreground_collider = Box_Collider(WIDTH / 2, HEIGHT - 20, 720, 120, "environment")

            colliders.append(foreground_collider)

            spawner = Spawner(screen)

            particles = []

            time_elapsed = 0

            while (game_state == 1):
                screen.fill(WHITE)
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        game_state = 2
                    self.handle_inputs(keys, event)
                self.difficulty()
                self.calculate_deltatime()

                screen.blit(foreground.image, foreground.rect)

                time_elapsed += self.dt

                if (time_elapsed > 10):
                    part = Particle()
                    particles.append(part)
                    time_elapsed = 0
                for i in range(len(particles)):
                    try:
                        particles[i].move(self.dt)
                        particles[i].draw(screen)
                        particles[i].collision(particles)
                    except:
                        pass

                player.move(keys, self.dt)
                player.draw(screen, BLACK, self.dt, colliders)

                spawner.spawner()
                spawner.set_time_between_spawns(self.time_between_spawns)
                spawner.timer(self.dt)
                spawner.draw_enemies(self.dt)
                spawner.check_for_player(player, player.scalar)

                self.update_score(screen, font)

                pygame.display.update()

        def menu(self, screen, font, WIDTH, HEIGHT):
            global game_state

            COLOR = (224, 190, 108)

            sound = pygame.mixer.Sound("Data/Sounds/Start.wav")
            play_text = font.render("PLAY", True, (255, 255, 255))
            play_text_y_offset = 0

            score_text = font.render("HIGH SCORE: " + str(int(max_score)), True, (255, 255, 255))

            tutorial_text = font.render("You're Melting!", True, (255, 255, 255))
            tutorial_text_2 = font.render("Collect Snow And Avoid Moving Rocks!", True, (255, 255, 255))

            direc = 1
            while game_state == 0:
                screen.fill(COLOR)
                screen.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2,
                                        HEIGHT / 2 - play_text.get_height() / 2 + play_text_y_offset))
                screen.blit(score_text, (
                    WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - score_text.get_height() / 2 + 150))
                play_text_y_offset = math.sin(time.time() * 5) * 5 - 25
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        game_state = 2
                    if (pygame.mouse.get_pos()[0] < WIDTH / 2 + play_text.get_width() / 2 and
                            pygame.mouse.get_pos()[0] > WIDTH / 2 - play_text.get_width() / 2):
                        if (pygame.mouse.get_pos()[
                            1] < HEIGHT / 2 + play_text.get_height() / 2 + play_text_y_offset and
                                pygame.mouse.get_pos()[
                                    1] > HEIGHT / 2 - play_text.get_height() / 2 + play_text_y_offset):
                            if (event.type == pygame.MOUSEBUTTONDOWN):
                                game_state = 1
                                sound.play()
                pygame.display.update()

        def __init__(self):
            global game_state
            global score
            global score_int
            global entities_alive

            while game_state != 2:
                WIDTH, HEIGHT = 720, 480

                screen = self.setup_pygame("Sno Snow", WIDTH, HEIGHT)
                font = pygame.font.Font("Data/Fonts/Inter.ttf", 32)

                if (game_state == 0):
                    self.menu(screen, font, WIDTH, HEIGHT)
                if (game_state == 1):
                    self.previous_frame_time = time.time()
                    self.game(screen, font, WIDTH, HEIGHT)

                sound = pygame.mixer.Sound("Data/Sounds/Die.wav")
                sound.play()
                self.reset_state()
                score = 0
                score_int = 0
                entities_alive.clear()
                entities_alive = []

    game = Main()

def open_calendar():

    import tkinter as tk
    from PIL import ImageTk, Image
    import calendar

    root = tk.Tk()
    root.geometry('400x300')
    root.title('Calender-Techarge')

    def show():
        m = int(month.get())
        y = int(year.get())
        output = calendar.month(y, m)

        cal.insert('end', output)

    def clear():
        cal.delete(1.0, 'end')

    def exit():
        root.destroy()

    m_label = Label(root, text="Month", font=('verdana', '10', 'bold'))
    m_label.place(x=70, y=80)

    month = Spinbox(root, from_=1, to=12, width="5")
    month.place(x=140, y=80)

    y_label = Label(root, text="Year", font=('verdana', '10', 'bold'))
    y_label.place(x=210, y=80)

    year = Spinbox(root, from_=2020, to=3000, width="8")
    year.place(x=260, y=80)

    cal = Text(root, width=33, height=8, relief=RIDGE, borderwidth=2)
    cal.place(x=70, y=110)

    show = Button(root, text="Show", font=('verdana', 10, 'bold'), relief=RIDGE, borderwidth=2, command=show)
    show.place(x=140, y=250)

    clear = Button(root, text="Clear", font=('verdana', 10, 'bold'), relief=RIDGE, borderwidth=2, command=clear)
    clear.place(x=200, y=250)

    exit = Button(root, text="Exit", font=('verdana', 10, 'bold'), relief=RIDGE, borderwidth=2, command=exit)
    exit.place(x=260, y=250)
    root.mainloop()

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour <= 16:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("How are you boss?")


def jokes_angel():
    lines = [
        'A bear walks into a bar and says, “Give me a whiskey and … cola.”“Why the big pause?” asks the bartender. The bear shrugged. “I’m not sure; I was born with them.”',
        'Hear about the new restaurant called Karma?There’s no menu: You get what you deserve.',
        'Yesterday I saw a guy spill all his Scrabble letters on the road. I asked him, “What’s the word on the street?',
        'Why do we tell actors to “break a leg?”Because every play has a cast.',
        'Where are average things manufactured?The satisfactory.',
        'How do you drown a hipster?Throw him in the mainstream.',
        'How does Moses make tea?He brews.',
        'How do you keep a bagel from getting away?Put lox on it.',
        'A man tells his doctor, “Doc, help me. I’m addicted to Twitter!”The doctor replies, “Sorry, I don’t follow you …”',
        'Why don’t Calculus majors throw house parties?Because you should never drink and derive.',
        'What do you call a parade of rabbits hopping backwards?A receding hare-line.',
        'What’s the different between a cat and a comma?A cat has claws at the end of paws; A comma is a pause at the end of a clause.',
        'Why should the number 288 never be mentioned?It’s two gross.',
        'What did the Tin Man say when he got run over by a steamroller?“Curses! Foil again!”',
        'What did the bald man exclaim when he received a comb for a present?Thanks— I’ll never part with it!',
        'What did the left eye say to the right eye?Between you and me, something smells.',
        'What do you call a fake noodle?An impasta.',
        'Did you hear about the actor who fell through the floorboards?He was just going through a stage.',
        'Why don’t scientists trust atoms?Because they make up everything.',
        'What do you call a magic dog?A labracadabrador.']
    myline = random.choice(lines)
    speak(myline)


def email_bot():
    def send_email(receiver, subject, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Make sure to give app access in your Google account
        server.login('robotmarkxii@gmail.com', 'rqottgtfqkijfkkx')
        email = EmailMessage()
        email['From'] = 'Sender_Email'
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(message)
        server.send_message(email)

    email_receiver = input("Enter the email ID of the receiver: ")

    def get_email_info():
        receiver = email_receiver
        print(receiver)
        speak('What is the subject of your email?')
        subject = takecommand()
        speak('Tell me the text in your email')
        message = takecommand()
        send_email(receiver, subject, message)
        speak("Email has been sent")
        speak('Do you want to send more email?')
        send_more = takecommand()
        if 'yes' in send_more:
            get_email_info()

    get_email_info()


if __name__ == "__main__":
        wishMe()

        while True:
            command = takecommand()
           # command = input("Command:-  ").lower()

            if 'who is' in command:
                  person = command.replace('who is' ,'')
                  speak("Searching")
                  results = wikipedia.summary(person, sentences=2, auto_suggest=False)
                  speak(results)

            if 'send email' in command:
                email_bot()

            elif "what is" in command:
                item = command.replace('what is', '')
                speak("Searching")
                results1 = wikipedia.summary(item, sentences=2, auto_suggest=False)
                speak(results1)


            # Features
            elif 'read me a book' in command:
                speak("I have only the first two books of percy jackson. Many more will come in the future")
                speak("type Book-1 to listen to the lightning thief and type Book-2 to listen to the sea of monsters")
                print("type Book-1 to listen to the lightning thief and type Book-2 to listen to the sea of monsters")

                books = input("Enter the name of the pdf  = ")
                book = open(books + ".pdf", 'rb')
                pdfReader = PyPDF2.PdfFileReader(book)
                pagen = int(input("Start page - "))
                pageN = int(input("END page - "))

                speaker = pyttsx3.init()
                for num in range(pagen, pageN):
                    page = pdfReader.getPage(num)
                    text = page.extractText()
                    speaker.say(text)
                    speaker.runAndWait()

            elif 'set alarm' in command:
                speak("Okay")
                alarmHour = int(input("Hour ="))
                alarmMinute = int(input("Minute = "))
                amPm = str(input("pm or am = "))
                try:
                    if (amPm == "pm"):
                        alarmHour = alarmHour + 12
                    while (1==1):
                        if (alarmHour == datetime.datetime.now().hour and alarmMinute == datetime.datetime.now().minute):
                            speak("Beap")




                except:
                    command = input("Command:-  ").lower()

            elif 'play' in command:
                song = command.replace('play', '')
                speak('playing ' + song)
                pywhatkit.playonyt(song)

            elif 'open dictionary' in command:
                speak("opening dictionary")
                mean = input("Type The Word")
                webbrowser.open(
                    "https://www.google.com/search?rlz=1C1CHBF_enIN889IN889&q="+mean+"&spell=1&sa=X&ved=2ahUKEwir-5iJ1d_nAhXqILcAHUbIAMgQBSgAegQIEBAm&biw=1280&bih=561#dobs=" )

            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                speak('Current time is ' + time)
                print(time)

            elif 'you know my favourite' in command:
                speak("bro...i know u inside-out")
                song = command.replace('you know my favourite', 'sugar crash')
                speak('playing ' + song)
                pywhatkit.playonyt(song)

            elif 'online shopping' in command:
                speak("opening")
                webbrowser.open("amazon.in")

            elif 'I am thirsty for a movie' in command or "Put a movie" in command or "Movies" in command or "I want to watch a movie" in command:
                speak("yes sir")
                webbrowser.open("https://www.primevideo.com/ref=av_auth_return_redir")

            elif 'movies i can watch' in command:
                import requests

                api_key = "9ac6d2e03c14f36ec4914ef798000b8a"
                base_url = "https://api.themoviedb.org/3"

                r = requests.get(f"{base_url}/movie/now_playing", params={'api_key': api_key})

                data = r.json()

                for movie in data["results"]:
                    title = movie['title']
                    overview = movie['overview']
                    print("Movie title: " + title)

            elif 'hotstar' in command:
                speak("sure")
                webbrowser.open("https://www.hotstar.com/in")

            elif 'you suggest' in command:
                speak("i would suggest, you choose Wanda-Vision")

            elif 'prime video' in command:
                webbrowser.open("https://www.primevideo.com/ref=av_auth_return_redir")

            elif 'search' in command:
                # speak("fine! Now i have to make you learn. Great, Just Great.")
                query = input("Enter the search query- ")
                speak("The results will be opening.")
                webbrowser.open("http://google.com/search?q=" + query)

            elif 'you there' in command:
                speak("at your service sir")

            elif 'netflix' in command:
                webbrowser.open("https://www.netflix.com/in/")

            elif 'open amazon' in command:
                speak("what would you like to see?")
                item = input("Pls enter the name-")

                if "nothing" in item or "not yet decided" in item or "not sure" in item:
                    speak("okay sir")
                    webbrowser.open("http://www.amazon.in/")
                else:
                    webbrowser.open("http://www.amazon.in/"+item)

            elif 'my orders' in command:
                speak("right away sir")
                webbrowser.open("https://www.amazon.in/gp/css/order-history?ref_=nav_orders_first")

            elif 'open primevideo' in command:
                webbrowser.open("https://www.primevideo.com/ref=av_auth_return_redir")

            elif 'open netflix' in command:
                webbrowser.open("https://www.netflix.com/in/")

            elif 'discord' in command:
                speak("OKAY,so you want to talk to your friends.")
                webbrowser.open('https://discord.com/channels/@me')


            # APPS - / In built screens- / functions-

            elif 'calendar' in command:
                open_calendar()

            elif 'stop watch' in command:

                # Python program to illustrate a stop watch
                # using Tkinter
                # importing the required libraries
                import tkinter as Tkinter
                from datetime import datetime

                counter = 66600
                running = False


                def counter_label(label):
                    def count():
                        if running:
                            global counter

                            # To manage the intial delay.
                            if counter == 66600:
                                display = "Starting..."
                            else:
                                tt = datetime.fromtimestamp(counter)
                                string = tt.strftime("%H:%M:%S")
                                display = string

                            label['text'] = display  # Or label.config(text=display)

                            # label.after(arg1, arg2) delays by
                            # first argument given in milliseconds
                            # and then calls the function given as second argument.
                            # Generally like here we need to call the
                            # function in which it is present repeatedly.
                            # Delays by 1000ms=1 seconds and call count again.
                            label.after(1000, count)
                            counter += 1

                    # Triggering the start of the counter.
                    count()

                    # start function of the stopwatch


                def Start(label):
                    global running
                    running = True
                    counter_label(label)
                    start['state'] = 'disabled'
                    stop['state'] = 'normal'
                    reset['state'] = 'normal'


                # Stop function of the stopwatch
                def Stop():
                    global running
                    start['state'] = 'normal'
                    stop['state'] = 'disabled'
                    reset['state'] = 'normal'
                    running = False


                # Reset function of the stopwatch
                def Reset(label):
                    global counter
                    counter = 66600

                    # If rest is pressed after pressing stop.
                    if running == False:
                        reset['state'] = 'disabled'
                        label['text'] = 'Welcome!'

                    # If reset is pressed while the stopwatch is running.
                    else:
                        label['text'] = 'Starting...'


                root = Tkinter.Tk()
                root.title("Stopwatch")

                # Fixing the window size.
                root.minsize(width=250, height=70)
                label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
                label.pack()
                f = Tkinter.Frame(root)
                start = Tkinter.Button(f, text='Start', width=6, command=lambda: Start(label))
                stop = Tkinter.Button(f, text='Stop', width=6, state='disabled', command=Stop)
                reset = Tkinter.Button(f, text='Reset', width=6, state='disabled', command=lambda: Reset(label))
                f.pack(anchor='center', pady=5)
                start.pack(side="left")
                stop.pack(side="left")
                reset.pack(side="left")
                root.mainloop()

            elif 'weather' in command:
                speak("Okay, please type in your city name in the box that will open now")

                import tkinter as tk
                import requests
                import time


                def getWeather(canvas):
                    city = textField.get()
                    api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=06c921750b9a82d8f5d1294e1586276f"

                    json_data = requests.get(api).json()
                    condition = json_data['weather'][0]['main']
                    temp = int(json_data['main']['temp'] - 273.15)
                    current_temp = int(json_data['main']['temp_min'] - 273.15)
                    pressure = json_data['main']['pressure']
                    humidity = json_data['main']['humidity']
                    wind = json_data['wind']['speed']
                    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
                    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))

                    # speak current_temp
                    speak("Current Temperature is")
                    speak(current_temp)
                    speak("degrees celcius")

                    final_info = condition + "\n" + str(temp) + "°C"
                    final_data = "\n" + "Current temperature: " + str(current_temp) + "°C" + "\n" + "Pressure: " + str(
                        pressure) + "\n" + "Humidity: " + str(
                        humidity) + "\n" + "Wind Speed: " + str(
                        wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
                    label1.config(text=final_info)
                    label2.config(text=final_data)


                canvas = tk.Tk()
                canvas.geometry("1000x900")
                canvas.title("Weather App")
                f = ("poppins", 15, "bold")
                t = ("poppins", 35, "bold")

                textField = tk.Entry(canvas, justify='center', width=20, font=t)
                textField.pack(pady=20)
                textField.focus()
                textField.bind('<Return>', getWeather)

                label1 = tk.Label(canvas, font=t)
                label1.pack()
                label2 = tk.Label(canvas, font=f)
                label2.pack()
                canvas.mainloop()

            elif 'calculator' in command:
                from tkinter import *


                def iCalc(source, side):
                    storeObj = Frame(source, borderwidth=4, bd=4, bg="powder blue")
                    storeObj.pack(side=side, expand=YES, fill=BOTH)
                    return storeObj


                def button(source, side, text, command=None):
                    storeObj = Button(source, text=text, command=command)
                    storeObj.pack(side=side, expand=YES, fill=BOTH)
                    return storeObj


                class app(Frame):
                    def __init__(self):
                        Frame.__init__(self)
                        self.option_add('*Font', 'arial 20 bold')
                        self.pack(expand=YES, fill=BOTH)
                        self.master.title('Calculator')

                        display = StringVar()
                        Entry(self, relief=RIDGE, textvariable=display,
                              justify='right'
                              , bd=30, bg="powder blue").pack(side=TOP,
                                                              expand=YES, fill=BOTH)

                        for clearButton in (["C"]):
                            erase = iCalc(self, TOP)
                            for ichar in clearButton:
                                button(erase, LEFT, ichar, lambda
                                    storeObj=display, q=ichar: storeObj.set(''))

                        for numButton in ("789/", "456*", "123-", "0.+"):
                            FunctionNum = iCalc(self, TOP)
                            for iEquals in numButton:
                                button(FunctionNum, LEFT, iEquals, lambda
                                    storeObj=display, q=iEquals: storeObj
                                       .set(storeObj.get() + q))

                        EqualButton = iCalc(self, TOP)
                        for iEquals in "=":
                            if iEquals == '=':
                                btniEquals = button(EqualButton, LEFT, iEquals)
                                btniEquals.bind('<ButtonRelease-1>', lambda e, s=self,
                                                                            storeObj=display: s.calc(storeObj), '+')


                            else:
                                btniEquals = button(EqualButton, LEFT, iEquals,
                                                    lambda storeObj=display, s=' %s ' % iEquals: storeObj.set
                                                    (storeObj.get() + s))

                    def calc(self, display):
                        try:
                            display.set(eval(display.get()))
                        except:
                            display.set("ERROR, your problem is problematic")


                if __name__ == '__main__':
                    app().mainloop()

            elif 'safe' in command:
                from tkinter import *

                speak("Type the credentials")
                root = Tk()
                root.geometry("500x300")

                Label(root, text="Secure", font="arial 15 bold").grid(row=0, column=3)


                def getvals():

                    webbrowser.open("https://duckduckgo.com/?natb=v268-5qo&cp=atbhc")
                    speak("Secured access")


                UserName = Label(root, text="UserName", font="arial 10 bold")
                Passwords = Label(root, text="Password", font="arial 10 bold")

                UserName.grid(row=1, column=2)
                Passwords.grid(row=2, column=2)

                Uservalue = StringVar
                Passwordvalue = StringVar
                checkvalue = StringVar

                Userentry = Entry(root, textvariable=Uservalue)
                Passwordsentry = Entry(root, textvariable=Passwordvalue)

                # CheckBox
                # checkbtn = Checkbutton(text="remember me", variable = checkvalue)
                # checkbtn.grid(row=4, column =3)

                Userentry.grid(row=1, column=3)
                Passwordsentry.grid(row=2, column=3)

                Button(text="Enter", command=getvals).grid(row=4, column=3)

                root.mainloop()


            # for fun-

            elif 'your name' in command:
                speak(
                    "bruh....I told you in my introduction.....Do you have memory loss......I aint google or siri...I am The Helios")

            elif 'made you' in command:
                speak("I dont remember that part, but all i know is that a company named pipInstallUs made me")
                speak("here let me open their youtube channel")
                webbrowser.open("https://www.youtube.com/")

            elif 'you are my favourite' in command:
                speak("Thank you for that designation")

            elif 'alive' in command:
                speak("no, i exist only here")

            elif 'stupid' in command:
                speak("You stupid")
                print("You stupid")

            elif 'who are you' in command:
                speak(
                    "havent we met before? i am Helios and Helios Stands for Highly Enthusiastic Largely Intelligent Operating System")

            elif 'single' in command:
                speak("No,boss. I am in a relationship with WIFI")

            elif 'lol' in command:
                speak("My jokes are always the best.")

            elif 'hey' in command:
                speak("Hey!")

            elif 'bruh' in command:
                speak("Literal bruh moment. But why?")

            elif 'help me' in command:
                speak("How? I am not jarvis. I cant send suits. I aint EDITH or FRIDAY. I cant help, sorry.")

            elif 'bye' in command:
                speak("Good Riddance")

            elif 'bored' in command:
                speak("OKAY! What do you want, games or jokes?")
                answer = input("you answer - ")
                if 'games' in answer:
                    speak("i have only one game cause my memory is very low")
                    webbrowser.open(
                        "https://studio.code.org/projects/gamelab/anOwgsamlKSR4RKeXDSjKJL9DcMKKOMJcEZt59mR64A/embed?nosource")
                elif 'jokes' or 'joke' in answer:
                    jokes_angel()


            elif 'jokes' in command:
                jokes_angel()

            elif 'go away' in command:
                speak("Okay")
                exit()

            elif 'games' or 'game' in command:
                speak("This part is undergoing development. Please bear with us")
                # root = Tkinter.Tk()
                # root.title("game chooser")
                #
                # # Fixing the window size.
                # root.minsize(width=250, height=70)
                # label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
                # label.pack()
                # f = Tkinter.Frame(root)
                # start = Tkinter.Button(f, text='SnowBall', width=9, command=lambda: SnowBall)
                # stop = Tkinter.Button(f, text='SnakeGame', width=9, command=CarGame)
                # f.pack(anchor='center', pady=10)
                # start.pack(side="left")
                # stop.pack(side="left")
                # root.mainloop()

            # Quit Helios


            else:
                speak("ERROR!")
