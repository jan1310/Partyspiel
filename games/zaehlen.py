import time
import random

from control import setup
from helper import animations

# GPIO Import
try:
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

ran_num = 0
nummer = []

#Nummern Speichern
def callback_hochzaehlen(switch):
    global nummer
    player = setup.active_button.index(switch)
    nummer[player] = nummer[player] + 1

def startGame():
    #Vorbereiten
    global nummer, ran_num
    setup.add_eventDetect(250)

    while setup.areAllPlayerAlive():
        #Warten
        animations.all_blink(1, random.randint(2, 5))

        #Start
        nummer = []
        for i in range(setup.active_player):
            nummer.append(0)

        ran_num = random.randint(9, 21)
        time.sleep(1)

        # Blinken
        for t in range(ran_num):
            sleepTime = random.randint(150, 350)
            animations.one_blink(setup.all_led[random.randint(0, setup.max_player-1)], 1, sleepTime/1000)
            time.sleep(sleepTime/1000)

        #Auf Ende Warten
        time.sleep(6)

        print("nummer vorher: ", nummer)
        #Gewinner/Verlierer berechnen
        for player in range(setup.active_player):
            nummer[player] = abs(nummer[player] - ran_num)

        minimum = min(nummer)
        maximum = max(nummer)
        winner = []
        loser = []
        for player in range(setup.active_player):
            if nummer[player] == minimum:
                winner.append(player)
            elif nummer[player] == maximum:
                loser.append(player)

        print("nummer: ", nummer)
        print("minimum: ", minimum)
        print("maximum: ", maximum)
        print("winner: ", winner)
        print("loser: ", loser)
        setup.subtractLifeFromPlayerArrayWithWinnerArray(loser, winner)

        if setup.areAllPlayerAlive():
            setup.waitForContinue()

    #Ende
    setup.remove_eventDetect()