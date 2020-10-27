from microbit import *
import random
import radio #importing all required libraries

microbit_name = "Orange"
radio.on()
radio.config(channel=1, power = 1)
screen = Image("99999:99999:99999:99999:99999")
lock_out = False
player_role = "" #setting everything up

class Doctor: #defining all of the roles
    def __init__(self):
        self.health = 100 #how much health the player starts with
        self.healed = False #for the doctor only, if they healed themselves
        self.status = True #if they are dead or alive
        self.minimum = 10 #the minimum heal they can do
        self.maximum = 40 #the maximum heal they can do

class Murderer: #definining the roles
    def __init__(self):
        self.health = 100 #how much health the player starts with
        self.status = True #if they are dead or alive
        self.minimum = 5 #the minimum damage they can do
        self.maximum = 25 #the maximum maximum they can do

class Detective:
    def __init__(self):
        self.health = 100
        self.status = True
        self.minimum = 5
        self.maximum = 30

class Civilian:
    def __init__(self):
        self.health = 100
        self.status = True
        self.minimum = 0
        self.maximum = 20

def attack(minimum, maximum): #defining the function
    attack_strength = random.randint(minimum, maximum) #randomizing the strength
    signal = "attk//"+str(attack_strength) #creating the signal
    radio.send(signal) #sending the signal

def heal_others(minimum, maximum): #defining the function
    heal_strength = random.randint(minimum, maximum) #randomizing the strength
    signal = "heal//"+str(heal_strength) #creating the signal
    radio.send(signal) #sending the signal

def heal_self(minimum, maximum, health): #defining the function
    heal_strength = random.randint(minimum, maximum) #randomizing the strength
    health = health + heal_strength #increasing the health
    if health > 100: #capping the health
        return 100
    else:
        return health #making sure health is returned

while True:
    signal = radio.receive() #reciving any signals sent
    incoming = (str(signal)).split('//') #splitting the signal

    if incoming[0] == "game":
        if incoming[1] == "reset":
            player = Civilian() #if this was a new game, there would be no player and this would have caused an error
            del player #this combination ensures that regardless of what round, there will be a reset
            lock_out = False #reset all variables
            player_role = ""
            display.scroll("reset")

    if incoming[0] == "chnl": #if it's a channel signal
        if incoming[1] == "public": #if the signal says public
            radio.config(channel = 1) #switch to the public channel
            display.scroll("pub")
        if incoming[1] == "private": #if the signal says private
            display.scroll("priv")
            radio.config(channel = 3) #switch to the private channel

    if incoming[0] == "role": #if it assigns the roles
        player_role = incoming[1]
        if incoming[1] == "Dt": #this is where it will initialize the player class based on the role
            player = Detective()
            display.scroll("Dt")
        elif incoming[1] == "Md":
            player = Murderer()
            display.scroll("Md")
        elif incoming[1] == "Dr":
            player = Doctor()
            display.scroll("Dr")
        elif incoming[1] == "Cv":
            player = Civilian()
            display.scroll("Cv")

    if incoming[0] == "lead":
        display.show(incoming[1])

    while player_role != "":
        while lock_out == False:
            signal = radio.receive() #reciving any signals sent
            incoming = (str(signal)).split('//') #splitting the signal

            if incoming[0] == "dead": #if the player they meet is dead
                display.scroll(str(incoming[2])) #display their role
                display.clear()

            if incoming[0]=="role": #if the station replaces the detective
                if incoming[1] == "replace":
                    if player_role == "Cv":
                        temporary_health = player.health
                        del player #their health is saved and object deleted
                        player = Detective() #they make a new object
                        player.health = temporary_health #their health is carried over
                        player_role = "Dt" #their role has changed
                        signal = ("detective//replaced//" + microbit_name)
                        radio.send(signal) #ensure the stations knows they were replaced.


            if incoming[0] == "attk": #if it's an attack signal
                player.health = player.health - int(incoming[1])
                display.show(screen)
                sleep (10)
                display.clear()
                sleep(3000)
                if player.health<=0: #if the result is 0 or less
                    lock_out = True #lock them out
            if incoming[0] == "heal": #if it's an attack signal
                player.health = player.health + int(incoming[1])
                if player.health>100: #if the result is 100 or more
                    player.health = 100 #cap them at 100

            if button_a.is_pressed(): #if a is pressed
                if player_role != "Dr": #if they arent the doctor
                    attack(player.minimum, player.maximum) #send an attack signal
                else:
                    heal_others(player.minimum, player.maximum) #otherwise send a heal
            if button_b.is_pressed(): #if b is pressed
                if player_role != "Dr": #if they arent the doctor
                    display.scroll(player.health) #display the health
                else:
                    if player.healed == False: #if the doctor hasn't healed themselves
                        heal_self(player.minimum, player.maximum, player.health) #heal them
                        player.healed = True #and ensure they cant heal again
                        display.scroll("Healed.")
                    else:
                        display.scroll("Heal used.") #notify the player they have used the heal

        while lock_out == True: #if the user is out of the game
            signal = radio.receive() #reciving any signals sent
            incoming = (str(signal)).split('//') #splitting the signal

            display.show(screen) #show the full red screen
            radio.send("dead//"+microbit_name+"//"+player_role) #constantly send out the signal
            sleep(5000) #make it sleep so it doesnt clog up the queue

            if incoming[0] == "game": #have a reset
                if incoming[1] == "reset":
                    player = Civilian() #if this was a new game, there would be no player and this would have caused an error
                    del player #this combination ensures that regardless of what round, there will be a reset
                    lock_out = False
                    player_role = ""
                    display.clear()