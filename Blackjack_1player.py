'''
#Author: Aidan Lee
#Date Modified 9/18/10
#This program simulates 4 deck Blackjack
#Blackjack pays 3/2 times the bet
#Dealer stops hitting at a hard 17 or hits one more time at a soft 17
#Only allows user to split deck once
'''

from os import system, name
import random
import colorama
from colorama import Fore,Style
colorama.init()

#Suits and card_ranks are global variables becuase they are used in the card class and deck functions

#Code to print the card symbols in the order of spades, club, diamond,heart
suits = ("\u2660", "\u2663", "\u2666", "\u2665")
card_ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

#card_value holds the actual numerical value that a card rank represents
card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
             "J": 10, "Q": 10, "K": 10, "A": 11}

class Card:
    #Card object holds the suit and card number of a card
    #Also allows for the card to be easily printed

    def __init__(self,card_ranks,suits):
        #Gives each card a suit and rank
        self.card_ranks = card_ranks
        self.suits = suits

    def __str__(self):
        #Automatically prints both the rank and suit of the card

        #Check if the suit is diamond or heart so it should be printed
        if self.suits == "\u2666" or self.suits == "\u2665":
            #Check to see if the card rank is 10 becuase it has one extra digit and the alignment function is not
            #working for me so I just remove one of the spaces between the rank and suit
            if self.card_ranks == "10":
                return (Fore.RED + f"{self.card_ranks} {self.suits}" + Style.RESET_ALL)

            #Any card that is not a 10. AKA has one digit to repreesent the rank
            else:
                return (Fore.RED + f"{self.card_ranks}  {self.suits}" + Style.RESET_ALL)

        #Prints the card rank and suit but without color because it is a spade or club
        else:
            if self.card_ranks == "10":
                return (f"{self.card_ranks} {self.suits}")
            else:
                return (f"{self.card_ranks}  {self.suits}")

class Hand:
    #Hands holds the dealer and player's hands as well as the current amount bet on the individual hand

    def __init__(self,player_name):
        #cards_in_hand is a list of card objects, which starts empty as well as the player's name
        self.cards_in_hand = []
        #The value of the players hand begins at zero
        self.hand_value = 0
        self.player_name = player_name
        #Keeps track of the total number of aces that are in the hand
        self.total_aces = 0
        #Keeps track of the number of aces that have their value still at 11 and have not been reduced to to avoid a
        # 1 to avoid a bust
        self.aces_not_reduced = 0
        #keeps track if player has blackjack, has won the hand, or busted
        self.blackjack = False
        #Keeps track if the hand has busted (could just use one line to check if > 21)
        self.bust = False
        #Keeps track if hand can be hit again (can't if >=21 or double down and already hit once)
        self.hit_allowed = True
        #Checks if a split is allowed based on if the the first two cards have the same value
        self.split_allowed = False
        # Keeps track if doubling down is allowed
        self.dd_allowed = True
        #Hand_over is used to know the dealer should even hit. They should not if bust
        self.hand_over = False
        #Checks if it is the hands first hit card because that means they can have Blackjack or split or double down
        self.first_card = True
        #keeps track of if the hand has been split
        self.hand_split = False
        #Keeps track of each hand's bet (can be different if hand is split and then there is a double down
        self.current_bet = 0


    def __str__(self):
        #cards is the string that will be returned for printing
        cards = ""
        #prints all text regarding the dealer in cyan (blue-ish)
        if self.player_name == 'dealer':
            cards += Fore.CYAN
        #Allows the user to print the cards in a hand as well as the value
        cards += (f"Cards in {self.player_name}:\n")
        #Resets the printing color so it matches the suit color
        cards += Style.RESET_ALL
        for each_card in self.cards_in_hand:
            cards += (each_card.__str__() + "\n")
        #Make the dealer font blue to easily see that it is seperate from the player's hand
        if self.player_name == "dealer":
            cards += (Fore.CYAN + (f"{self.player_name}'s hand value: {self.hand_value}"))
        else:
            cards += (f"{self.player_name}'s hand value: {self.hand_value}")

        return cards


    def add_card(self,new_card):
        #Adds a card to the users hand based on the card object passed to it as new_card
        #Updates the value of the hand
        self.cards_in_hand.append(new_card)
        self.hand_value += card_values[new_card.card_ranks]

        #if the player is dealt an ace then it adds to the players number of aces, which will  be used for changing
        #aces value from 11 to 1
        if new_card.card_ranks == "A":
            self.total_aces += 1
            #When an ace is added to the hand aces_not_reduced increases. When an ace changes from 11 to 1
            #aces_not_reduced will decrease
            self.aces_not_reduced += 1

class Deck:
   # Creates and holds a four decks of 52 unique cards that eventually gets smaller as deal is called

    def __init__(self):
        #deck is a list of the card objects

        self.deck = []
        #Create a stack of 4 decks of 52 cards
        for suit in suits:
            for rank in card_ranks:
                #Adds four of each cards
                self.deck.extend([Card(rank,suit) for i in range(4)])
        #shuffle the deck
        random.shuffle(self.deck)

        # Keeps track of the count of the deck for card counting practice
        self.count = 0
        #Keeps track of number of 10,J,Q,K,and A left in deck for percentages
        self.num_of_tens = 80

        #Code to stack the deck for testing
        #self.deck.append(Card("J", "blah"))

    def deal(self):
        #Removes the last card object from the deck and returns it

        #Basic card counting decreases the count if a 10,J,Q,K, or A is dealt.
        #Increases count if 2,3,4,5, or 6 is dealt
        if card_values[self.deck[-1].card_ranks] <= 6:
            self.count +=1
        elif card_values[self.deck[-1].card_ranks] >= 10:
            self.count -= 1
            self.num_of_tens -= 1

        return self.deck.pop()

    def num_cards_left(self):
        #returns the number of cards left in the deck
        return len(self.deck)

    def odd_of_ten_or_ace(self):
        # Gives the odds that the next card is a 10 or Ace
        return f"{(100*self.num_of_tens/len(self.deck) - 100*(80/208)):.3f}"


def __str__(self):
    # Never used in program directly, but prints the entirety of the remainging deck
    cards_in_deck = ""
    for cards in self.deck:
        cards_in_deck += (cards.__str__() + "\n")

    return cards_in_deck

class Player_bank:
    #Holds the players money left to bet

    def __init__(self,money,name):
        self.money = money
        self.name = name

    #Removes money from the player's bank when they bet
    def make_bet(self,bet_amount):
        self.money -= bet_amount

    #Adds money to the player's bank based on the current hand bet
    def win_money(self,bet):
        self.money += bet

    def __str__(self):
        #Easily prints the player's bank
        return f"{self.name}'s total money: ${self.money:.2f}"


def clear():
    #Clears the terminal screen
    _ = system("clear")

def check_bet_valid():
    #Asks player for a bet. First checks if the bet is an integer. Then checks that they have enough to place that bet

    #bet_to_big is changed to false once the user enters a valid integer and has enough to bet that much
    bet_too_big = True
    while True:
        #This loop runs until they enter an integer and then breaks
        while True:
            try:
               bet = float(input("Enter bet: "))
            #except if the user enters a non-number
            except:
                print("Not a valid bet. Please try again")
            #break out of the while loop and onto the next one
            else:
                break

        #Doesn't let the player bet more than they have in the bank
        if bet > bank.money:
            print(f"You do not have enough to bet ${bet}")
            print("Try again")
        #minimum bet is $1
        elif bet < 1.0:
            print("Minimum bet is $1.00")
        #If the bet is vald then stop looping
        else:
            return bet


def show_board(num_of_splits):
    #Prints the current board with player and dealer cards and bank. Also prints count if the player wanted to

    clear()
    print(dealer_hand)
    print(Fore.CYAN + "----------------------------------" + Style.RESET_ALL)
    print(player_hand)
    print(f"\nCurrent bet: ${player_hand.current_bet:.2f}")

    #Tracks the split hands
    hand_number = 0
    #wrote it like this if I ever want to allow more than one split
    while hand_number < num_of_splits:
        print("----------------------------------")
        #Prints the split hands
        print(list_of_splits[hand_number])
        print(f"\nCurrent bet: ${list_of_splits[hand_number].current_bet}")
        hand_number += 1

    print("----------------------------------")
    print(bank)
    print("----------------------------------")

    #Shows card count and percentages if player wants it
    if show_count.upper() == "Y":
        print(f"Deck count: {the_deck.count}")
        print(f"Additional percentage of 10 or Ace: {the_deck.odd_of_ten_or_ace()} %")

def check_valid_option(enough_money,dd,split):
#Check to see if user entered H, S, or D for to signal if they want to hit, pass, or double down. Otherwise they have to enter another command
#Returns 0: Pass, 1: Hit, 2: Double Down, 3: double down
    while True:
        try:
            #True only if the player has enough money and their first two cards have the same card rank
            if enough_money and split:
                print("Enter 2 for Split")
            #True only if the user can double down becasue they have enough money and its their turn
            if enough_money and dd:
                print("Enter D: Double Down")
            print("Enter H: Hit")
            player_option = input("Enter S: Stay\n")
        except:
            print("Not a valid option. Try again")
        else:
            if player_option.upper() == "H":
                return 1
            elif player_option.upper() == "D" and enough_money and dd:
                return 2
            elif player_option == "2" and enough_money and split:
                return 3
            elif player_option.upper() == "S":
                return 0
            else:
                print("Not a valid option. Try again")

def print_message(fore_color,message):
    #Allows to easily print colored messages for winning, losing, or tie

    if fore_color == "green":
        print(Fore.GREEN)
    if fore_color == "red":
        print(Fore.RED)
    if fore_color == "yellow":
        print(Fore.LIGHTYELLOW_EX)

    print("--------------------------------------------------------")
    print(message)
    print("--------------------------------------------------------" + Style.RESET_ALL)

def player_hitting(hand):
    #Function that allows a hand to hit,stay,double down, or split

    global num_of_split_h,list_of_splits
    # Lets program know if the dealer can make a larger bet by doubling down. Default is true
    enough_for_bigger_bet = True
    # Checks if that is true
    if float(hand.current_bet) > bank.money:
        enough_for_bigger_bet = False

    ######################################################################
    # code to allow split for testing
    #hand.split_allowed = True
    ######################################################################

    option = 0
    if card_values[hand.cards_in_hand[0].card_ranks] == card_values[hand.cards_in_hand[1].card_ranks]:
        hand.split_allowed = True

    # If neither the player or dealer has blackjack, then the game continues
    if not hand.hand_over:
        # Let the player hit until they want to stay, hit 21, or bust (go over 21)
        while hand.hit_allowed:

            #Only prints the current hand that is being played if there are multiple split hands
            if num_of_split_h > 0:
                print(f"\nCurrent hand being played: {hand.player_name}")

            #Checks to see if the user has enough money to increase the bet by doubling down hor splitting
            if float(hand.current_bet) > bank.money:
                enough_for_bigger_bet = False

            #Ask if the user wants to hit,split,double down, or stay
            option = check_valid_option(enough_for_bigger_bet, hand.dd_allowed, hand.split_allowed)
            # option greater than zero means that the player wants to hit, double down, or split
            if option > 0:
                # The user splits
                if option == 3:
                    # keeps track that the base hand has been split
                    hand.hand_split = True
                    # Increases number of player's hands
                    num_of_split_h += 1
                    # Reduces the value of the player's original hand because they no longer have two cards
                    hand.hand_value -= card_values[hand.cards_in_hand[-1].card_ranks]

                    #Creates a new local temporary hand that will eventually be appended to lists_of_split)hands
                    split_h = Hand(f"{hand_name[num_of_split_h]} hand")

                    # Removes the second card from the player's original hand and gives it to the second players hand
                    # add_card automatically updates the player's hand value
                    split_h.add_card(hand.cards_in_hand.pop())
                    # removes money to bet on second hand
                    bank.make_bet(hand.current_bet)
                    #Sets the split hand bet to be the same as the current bet
                    split_h.current_bet = hand.current_bet

                    #Checks if split hand has 21 and should no longer let them hit on it
                    if split_h.hand_value == 21:
                        split_h.hit_allowed = False
                        split_h.hand_over = True

                    #Globally append the new split hand to the list of split hands
                    list_of_splits.append(split_h)

                # If the player doubles down
                elif option == 2:
                    # bet is doubled
                    bank.make_bet(hand.current_bet)
                    hand.current_bet *= 2
                    # If the player doubles down then they can only receive one card
                    hand.hit_allowed = False

                # The player is hitting so give them another card
                hand.add_card(the_deck.deal())

                # Check to see if they 21 in which case they are not allowed to hit again
                if hand.hand_value == 21:
                    hand.hit_allowed = False
                    # If the hand was split, then this is technically only their second card so they can hit Blackjack
                    if hand.hand_split and hand.first_card:
                        hand.blackjack = True
                        hand.hand_over = True

                # Check to see if they have an ace that can reduce their hand_value less than 21
                if hand.hand_value > 21:
                    if hand.aces_not_reduced > 0:
                        # Subtracts 10 is the same as changing the ace from an 11 to 1
                        hand.hand_value -= 10
                        # Reduces this variable so that the ace can't be used to reduce the value by 10 again
                        hand.aces_not_reduced -= 1
                    # If they have no aces then they have busted
                    else:
                        hand.hit_allowed = False
                        hand.bust = True
                        hand.hand_over = True

                # After the first hit, the player cannot double down again so dd_allowed becomes false.
                # Unless they split, in which case it stays true
                if option != 3:
                    hand.dd_allowed = False

                hand.first_card = False

            # else is for if the user chose never hit a card (option = 0)
            else:
                # The user stays
                hand.hit_allowed = False

            show_board(num_of_split_h)

        return


def check_hand_outcome(hand):
    #Check to see the outcome of a hand, prints the outcome, and updates the player's bank

    #Variable that says if the dealer bust message needs to be print becasue if there are multiple hands it only needs
    #to be printed once
    global print_dealer_bust

    # if the player busted then the bust message has already been sent and there is no payout
    if hand.bust:
        print_message("red",f"{hand.player_name} has bust")

    #If both the dealer and player are initially dealt blackjack
    elif hand.blackjack and dealer_hand.blackjack:
        print_message("yellow",f"Push. Both {hand.player_name} and dealer have Blackjack.")
        bank.win_money(hand.current_bet)

    #If only the player is dealt Blackjack.
    elif hand.blackjack and (not dealer_hand.blackjack):
        print_message("green",f"{hand.player_name} has Blackjack!!!")
        bank.win_money(2.5*hand.current_bet)

    #If only the dealer has blacjack
    elif dealer_hand.blackjack and (not hand.blackjack):
        print_message("red", "Sorry, the dealer has Blackjack")

    #If the dealer busted and the player's hand did not bust
    elif dealer_hand.bust and (not hand.bust):
        #only want to print that the dealer's hand busted once if there are multiple split hands
        if print_dealer_bust:
            print(Fore.GREEN + "Dealer Busts!")
            print_dealer_bust = False
        print_message("green", f"{hand.player_name} wins!")
        bank.win_money(2*hand.current_bet)

    #Neither the dealer or the player's hand busted so compare values and dealer has a higher value
    elif dealer_hand.hand_value > hand.hand_value:
        print_message("red", f"Dealer has a higher value than {hand.player_name}. Dealer wins")

    # Neither the dealer or the player's hand busted so compare values and current player hand has a higher value
    elif dealer_hand.hand_value < hand.hand_value:
        print_message("green", f"{hand.player_name} wins!")
        bank.win_money(2 * hand.current_bet)

    #Push (AKA tie) when neither the dealer or player bust and they have the same hand value
    elif dealer_hand.hand_value == hand.hand_value:
        print_message("yellow",f"Push. Dealer and {hand.player_name} have the same value.")
        bank.win_money(hand.current_bet)

#####################################################################################
#begin main program
#####################################################################################

clear()
print("Welcome to Aidan's second program: Blackjack!")
player = input("Enter your name: ")
clear()
print(f"Hello {player}. Let's begin\n")
#Changes the player name for printing reasons later
player += "'s hand"

#boolean if the player wants the count printed
print("Would you like the deck count printed for practicing counting cards?")
show_count = input("Enter 'Y' for yes or press enter for no: ")
if show_count.upper() == "Y":
    clear()
    print("Basic card counting keeps track if lots of low or high cards are being dealt")
    print("Count starts at zero")
    print("If the card is a 10,J,Q,K, or A then the count is decreased")
    print("If the card is a 2,3,4,5, or 6 then the count is increased")
    print("Count remains the same if 7,8, or 9")
    input("Press Enter to exit card counting description")

print("\nBlackjack will be played with four decks")
print("You will start the game with $100. Minimum bet is $1.00")

#GLOBAL VARIABLES
#Creates a shuffled deck of cards
the_deck = Deck()
#Creates an empty hand for the player
player_hand = Hand(player)
#Creates a bank for the player
bank = Player_bank(100,player)
#creates an empty hand for the dealer
dealer_hand = Hand("dealer")

#names hands if player splits hands
hand_name = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth"]

#continue_play is true until the player wants to stop playing hands
continue_play = True

while continue_play:

    #Clears hands by reinitialzing them
    player_hand = Hand(player)
    dealer_hand = Hand("dealer")
    #List to hold the split hands
    list_of_splits = []
    # Keeps track of number of splits
    num_of_split_h = 0

    #Checks to see if the user still has enough money to play
    if bank.money < 1:
        print("You are broke. You lose. Go home.")
        break

    #Determines the amount the player wants to bet
    player_hand.current_bet = check_bet_valid()
    #Removes that amount of money from the player's hand
    bank.make_bet(player_hand.current_bet)

    #Deal the initial cards:
    #Give the player two cards
    player_hand.add_card(the_deck.deal())
    player_hand.add_card(the_deck.deal())
    #Give the dealer one card (the dealer should get two but its easier to pretend they got two but only show one
    dealer_hand.add_card(the_deck.deal())
    #Stores the dealers second card but doesn't give it to the dealer for simplicity of not printing it
    dealer_sec_card = the_deck.deck.pop()

    #This just deals with the one outlier when the player is dealt two aces becasue ace reduce algorithim hasnt run
    if player_hand.hand_value == 22:
        player_hand.hand_value = 12
        show_board(num_of_split_h)
        player_hand.hand_value = 22
    else:
        show_board(num_of_split_h)

    #Check to see if the game ends immediately because of a blackjack. To avoid decimals, blackjack here pays 2:
    if player_hand.hand_value == 21:
        player_hand.blackjack = True
        player_hand.hand_over = True

    #Check to see if the dealer has an ace. If the dealer does, then checks if the next card in the deck has a value of 10
    #If it does, then it adds that card to the dealers hand and ends the round
    if dealer_hand.hand_value == 11:
        print("Dealer has an ace showing")
        print("Press Enter to see if the dealer has Blackjack\n")
        input("")
        if card_values[dealer_sec_card.card_ranks] == 10:
            #Adds the card to the hand for printing
            dealer_hand.add_card(dealer_sec_card)

            #Have to manually change the deck count because a card is being added but not through the deal() function
            if card_values[dealer_hand.cards_in_hand[-1].card_ranks] <= 6:
                the_deck.count += 1
            elif card_values[dealer_hand.cards_in_hand[-1].card_ranks] >= 10:
                the_deck.count -= 1
                the_deck.num_of_tens -= 1

            show_board(num_of_split_h)
            player_hand.hand_over = True
            dealer_hand.blackjack = True
        else:
            print("The dealer does not have blackjack. Let's continue\n")

    # Check to see if the dealer's face up card has a value of 10. If the dealer does, then checks if the next card in
    # the deck (their face down card) is an ace
    # If it does, then it adds that card to the dealers hand and ends the round
    if dealer_hand.hand_value == 10:
        print("Dealer has a hand value of 10 showing")
        input("Press Enter to see if the dealer's other card is an Ace for Blackjack")
        if dealer_sec_card.card_ranks == "A":
            # Adds the card to the hand for printing
            dealer_hand.add_card(dealer_sec_card)

            # Have to manually change the deck count because a card is being added but not through the deal() function
            if card_values[dealer_hand.cards_in_hand[-1].card_ranks] <= 6:
                the_deck.count += 1
            elif card_values[dealer_hand.cards_in_hand[-1].card_ranks] >= 10:
                the_deck.count -= 1
                the_deck.num_of_tens -= 1

            show_board(num_of_split_h)
            player_hand.hand_over = True
            dealer_hand.blackjack = True
        else:
            print("The dealer does not have blackjack. Let's continue")

    ################################################
    #Player has the option to hit,stay, double down, or split
    player_hitting(player_hand)

    #Moves onto additional hands forom splitting
    #hand_number is just an index for going through split hands
    hand_number = 0
    while hand_number < len(list_of_splits):
        #Automatically have to add second card to split hand
        list_of_splits[hand_number].add_card(the_deck.deal())
        #Then have to check for Blackjack
        if list_of_splits[hand_number] == 21:
            list_of_splits[hand_number].blackjack = True
            list_of_splits[hand_number].hit_allowed = False
            list_of_splits[hand_number].hand_over = True
        #Show the board with the new card added to the split hand
        show_board(num_of_split_h)
        #Let the player hit,stay, double down, or split the split hands
        player_hitting(list_of_splits[hand_number])
        hand_number += 1
    ################################################

    #Check if any of the split hands are not over. Start by assuming all split hands are over as default
    a_split_hand_not_over = False
    #Only check if the hand has been split
    if num_of_split_h > 0:
        #Run through all of the spit hands and see if any is not over
        for hand_number in range(num_of_split_h):
            if not list_of_splits[hand_number].hand_over:
                #If a hand isn't over, then a_split_hand_not_over becomes true and the dealer will need to hit cards
                #even if the main hand is over
                a_split_hand_not_over = True

    #Runs if the dealer needs to add cards because they player did not bust or hit 21 for both hands
    if (not player_hand.hand_over) or a_split_hand_not_over:

        #Chose the rule that the dealer hits until they have a value of 17 or higher (normal casino rule)
        #Runs until the dealer has a hard hand value >= 17 or lets the dealer hit again if they have a soft 17
        #soft 17 means that an ace can still be reduced
        while dealer_hand.hand_value < 17 or (dealer_hand.hand_value == 17 and
                                              dealer_hand.aces_not_reduced == dealer_hand.total_aces
                                              and dealer_hand.total_aces > 0):
            #If its the dealer's first additional card then they are technically just flipping over their second card
            #And their second card has already been removed from the deck and stored in dealer_sec_card
            if dealer_hand.first_card:
                print("\nDealer will now flip over card")
                input("Press any key to see the result")
                dealer_hand.add_card(dealer_sec_card)

                #Have to manually change the card count because the card is being added but not through the deal() function
                if card_values[dealer_hand.cards_in_hand[-1].card_ranks] <= 6:
                    the_deck.count +=1
                elif card_values[dealer_hand.cards_in_hand[-1].card_ranks] >= 10:
                    the_deck.count -=1
                    the_deck.num_of_tens -= 1
            #It is the dealers third or more card
            else:
                print("\nDealer will now hit")
                input("Press any key to see the result")
                dealer_hand.add_card(the_deck.deal())
            #Check to se if an ace can be reduced from a value from 11 to 1
            if dealer_hand.hand_value > 21:
                if dealer_hand.aces_not_reduced > 0:
                    # Subtracts 10 is the same as changing the ace from an 11 to 1
                    dealer_hand.hand_value -= 10
                    # Reduces this variable so that the ace can't be used to reduce the value by 10 again
                    dealer_hand.aces_not_reduced -= 1
                  #if the dealer doesn't have any aces to reduce their hand then they bust
                else:
                    dealer_hand.bust = True
            show_board(num_of_split_h)
            #The additional cards will be hit instead of flipped
            dealer_hand.first_card = False

############################################
    #Move on to checking for results
############################################

    # Variable that says if the dealer bust message needs to be print because if there are multiple hands it only needs
    # to be printed once
    print_dealer_bust = True

    ################################################
    #Checks the player's main hand
    check_hand_outcome(player_hand)
    #Then checks the player's split hands
    hand_number = 0
    while hand_number < len(list_of_splits):
        check_hand_outcome(list_of_splits[hand_number])
        hand_number += 1
    ################################################

    #Print your money before the next round
    print(bank, "\n")
    print("Play another hand?")

    #Check to see if the player wants to do another hand
    if input("Hit any key to play again or 'N' for no: ").upper() == "N":
        continue_play = False
        print_message("green",f"{player}, thanks for playing!")

    #If the deck has less than 75 cards (I chose some arbitrary number) left, then its time to reshuffle the deck
    #and sets the count back to zero
    if the_deck.num_cards_left() < 75:
        clear()
        print("Dealer reshuffles all cards")
        the_deck = Deck()
        input("Press any key to start")
