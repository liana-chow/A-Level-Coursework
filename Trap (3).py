from microbit import *
import random
import radio #importing everything that is needed

screen = Image("99999:99999:99999:99999:99999")
#this will made a full red screen

radio.on()
radio.config(channel = 1)
auto_attack = False
user_attack = False
attempts = 0 #setting up

while True: #this will make the code constantly run
    while user_attack == False or auto_attack == False:
    #while the user isn't correct or hasn't failed 3 times
        correct_answer = ['.', '.', '.', '-'] #answer (3) is hard coded in
        user_input = ['', '', '', ''] #all the answers will be 4 in length
        answer_comparison = ['f', 'f', 'f', 'f'] #compare the user input and correct answer

        user_correct = False #if the user is correct

        index = 0 #this keeps a note of the next empty space

        while index != 4: #while they haven't reached the end of the list
            if button_a.was_pressed(): #input is a '.'
                user_input[index] = '.' #putting the input into the list
                display.scroll(user_input[index]) #display the user's input
                index = index + 1 #move to the next empty space
            if button_b.was_pressed(): #input is a '-'
                user_input[index] = '-' #putting the input into the list
                display.scroll(user_input[index]) #display the user's input
                index = index + 1 #move to the next empty space

        for i in range(0,4): #for the whole list
            if user_input[i] == correct_answer[i]: #if the user input matches the answer
                answer_comparison[i] = 't' #change the f to t

        if 'f' in answer_comparison: #if there is one wrong input
            attempts = attempts + 1 #they have attempted it
            signal_strength = random.randint(0,3)
            radio.config(power = signal_strength)
            attack = random.randint(0, 25)
            display.show(screen) #Show they did it wrong
            signal = "attk//"+str(attack)
            radio.send(signal)
            sleep(1000)
            display.clear()
            user_input = ['', '', '', ''] #all the answers will be 4 in length
            answer_comparison = ['f', 'f', 'f', 'f'] #reset the comparison
            if attempts == 3: #if the user has had three failed attempts
                display.scroll("Failed.")
                auto_attack = True #the auto-attack will trigger
        else: #if they are correct
            display.scroll("Trap set.") #inform the user
            sleep(3000) #giving time for them to set it
            user_attack = True #it will change to true

        while user_attack == True: #if player got it right
            attack = random.randint(0, 50) #randomly generate an attack strength
            display.show(screen) #show a red screen
            signal_strength = random.randint(2,4)
            radio.config(power = signal_strength)
            signal = "attk//"+str(attack)
            radio.send(signal)
            sleep(500)
            display.clear()
            sleep(3000) #rest for a bit

        while auto_attack == True: #if the player got it wrong
            attack = random.randint(50, 100) #randomly generate an attack strength
            display.show(screen) #show a red screen
            signal_strength = random.randint(4,7)
            radio.config(power = signal_strength)
            signal = "attk//"+str(attack)
            radio.send(signal)
            sleep(500)
            display.clear()
            sleep(1500) #rest for a bit