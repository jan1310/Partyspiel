import time

from helper import animations

try:
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

#Setup:
GPIO.setmode(GPIO.BCM)


max_life = 1
player_life = []

game_selected = 0

control_led = [14, 15, 18]
control_button = [16, 20]
player_led = [23, 24, 25, 8, 7]
player_button = [26, 19, 13, 6, 5]
max_player = len(player_button)

all_led = [14, 15, 18, 23, 24, 25, 8, 7]
all_button = [16, 20, 26, 19, 13, 6, 5]

#16 -> Back; 20 -> Next
active_player = 0
active_button = []
active_led = []

def initialize():
    for i in all_led:
        GPIO.setup(i, GPIO.OUT)
    for i in all_button:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Removes Callback
def remove_callback():
    for i in active_button:
        GPIO.remove_event_detect(i)

def subtractLifeFromPlayer(loser_num):

    animations.all_blink(5, 0.3)

    substractLifeAnimation(loser_num)

    player_life[loser_num] -= 1
    animations.array_off(control_led)

    time.sleep(1)

def subtractLifeFromPlayerArray(loser_num):

    animations.all_blink(5, 0.3)

    for i in loser_num:
        substractLifeAnimation(i)
        player_life[i] -= 1

    animations.array_off(control_led)
    time.sleep(1)

#!!!Duplicate as method above!!!
def subtractLifeFromPlayerWithWinner(loser_num, winner_num):
    animations.all_blink(5, 0.3)

    animations.one_blink(active_led[winner_num], 5, 0.2)

    substractLifeAnimation(loser_num)

    player_life[loser_num] -= 1
    animations.array_off(control_led)

    time.sleep(1)

def substractLifeAnimation(loser_num):
    GPIO.output(active_led[loser_num], 1)

    if player_life[loser_num] == 1:
        GPIO.output(control_led[2], 2)
        time.sleep(1)
        animations.one_blink(control_led[2], 3, 0.5)
    if player_life[loser_num] == 2:
        GPIO.output(control_led[1], 1)
        GPIO.output(control_led[2], 1)
        time.sleep(1)
        animations.one_blink(control_led[1], 3, 0.5)
    if player_life[loser_num] == 3:
        GPIO.output(control_led[0], 1)
        GPIO.output(control_led[1], 1)
        GPIO.output(control_led[2], 1)
        time.sleep(1)
        animations.one_blink(control_led[0], 3, 0.5)
    if player_life[loser_num] >= 4:
        animations.array_on(control_led)
        time.sleep(1)

    time.sleep(1)
    GPIO.output(active_led[loser_num], 0)

def areAllPlayerAlive():
    for i in player_life:
        if i <= 0:
            return False
    return True