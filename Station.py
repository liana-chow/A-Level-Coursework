from microbit import *
import random
import radio #importing all libraries

microbit_name = "Station"
radio.on()
radio.config(channel=1, power=7)
leaderboard = ["", "", "", "", "", ""]
place = 0
game_over = False
detective = True #setting up the microbit

while True:
    signal = radio.receive() #reciving any signals sent
    incoming = (str(signal)).split('//') #splitting the signal

    if button_a.was_pressed(): #start of a new game
        radio.config(channel = 1)
        display.scroll("New Game")#display for the players to see that a new game will start
        for i in range(0,7):
            radio.config(channel = int(i))
            radio.send("chnl//public") #makes sure that they on the public channel for the rest
        sleep(1000) #sleep to allow the players to switch
        radio.send ("game//reset") #this will have all the microbits reset
        display.scroll("Reset")
        sleep(1000) #sleep to allow the players to reset
        radio.send("chnl//private") #switch back to private channel

        station_players = [["Red", 2, "", True], ["Orange", 3, "", True], ["Yellow", 4, "", True],
        ["Green", 5, "", True], ["Blue", 6, "", True], ["Indigo", 7, "", True], ["Violet", 8, "", True]]
        #storing all of the player information in the format [name, channel, state, role]

        station_roles = ["Dt", "Md", "Dr", "Cv", "Cv", "Cv", "Cv"] #these are the avaliable roles
        assigned_roles = ["", "", "", "", "", "", ""] #this will be the order the roles are assigned
        players = [0, 1, 2, 3, 4, 5, 6] #this list prevents duplication of unnecessary roles
        assigned = False #this will make sure that the programmed is looped until all the roles are assigned
        index = 0 #this is the index of the assigned roles

        while assigned == False: #while not all of the roles have been assigned
            selection = random.randint(0, 6) #randomize the role that they will take
            if selection in players: #if the number is still in the list, a role has not been assigned
                players[selection] = "" #change the element to an empty one to prevent duplication
                assigned_roles[index] = station_roles[selection] #this puts the roles in order
                index = index + 1 #moving the index to the next empty role
            if "" not in assigned_roles: #if there aren't any unassigned roles
                assigned = True #end the loop

        for i in range(0, len(assigned_roles)): #going through the assigned roles
            station_players[i][2] = assigned_roles[i] #make sure that it's stored in the station's list
            radio.config(channel = int(station_players[i][1])) #switch to the private channels
            signal = "role//"+assigned_roles[i] #make a string with the role
            radio.send(signal) #send the string
            sleep(100)
            radio.send("chnl//public") #ensure that they switch back to the public channel
        sleep(3000) #give the players time to display everything

        display.scroll("Roles assigned.")

        while game_over == False:
            signal = radio.receive() #reciving any signals sent
            incoming = (str(signal)).split('//') #splitting the signal

            if incoming[0] == "dead":
                for i in range(0, len(station_players)):
                    if incoming[1] == station_players[i][0]:
                        if station_players[i][3] == True:
                            station_players[i][3] = False
                            leaderboard[place] = station_players[i][1]
                            place = place +1
                    if station_players[i][2] == "Md":
                        game_over = True
                    if place == 5:
                        game_over = True
                    if station_players[i][2] == "Dt":
                        detective = False
                station_players[i][2] = ""

            while detective == False:
                radio.send("role//replace")
                if incoming[0] == "detective":
                    for i in range(0, len(station_players)):
                        if station_players[i][0] == incoming[2]:
                            station_players[i][2] = "Dt"
                    detective = True
            if place == 5:
                for i in range(0, len(station_players)):
                    if station_players[i][3] == True:
                        leaderboard[6] = station_players[i][1]
                game_over == True


        while game_over == True:
            display.scroll("Game Over.")
            radio.send("chnl//private")
            if button_b.is_pressed():
                sleep(3000)
                if place != 5:
                    display.scroll("Murderer has lost!")
                else:
                    for i in range(0, len(leaderboard)):
                        radio.config(channel = int(leaderboard[i]))
                        signal = "lead//"+str((place+1))
                        place = place - 1
                        sleep(2000)