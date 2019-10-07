import random
import os
import matplotlib.pyplot as plt

# Suits and card_ranks are global variables because they are used in the card class and deck functions

# Code to print the card symbols in the order of spades, club, diamond,heart
suits = ("\u2660", "\u2663", "\u2666", "\u2665")
card_ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

# card_value holds the actual numerical value that a card rank represents
card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
               "J": 10, "Q": 10, "K": 10, "A": 11}


class Card:
    # Card object holds the suit and card number of a card
    # Also allows for the card to be easily printed

    def __init__(self, card_rank, suit):
        # Gives each card a suit and rank
        self.card_rank = card_rank
        self.suit = suit


class Hand:
    # Hands holds the dealer and player's hands as well as the current amount bet on the individual hand

    def __init__(self):
        # The value of the players hand begins at zero
        self.hand_value = 0
        # Keeps track of the total number of aces that are in the hand
        self.total_aces = 0
        # Keeps track of the number of aces that have their value still at 11 and have not been reduced to to avoid a
        # 1 to avoid a bust
        self.aces_not_reduced = 0
        # Keeps track if the hand has busted (could just use one line to check if > 21)
        self.bust = False

    def add_card(self, new_card):
        # Adds a card to the users hand based on the card object passed to it as new_card
        # Updates the value of the hand
        self.hand_value += card_values[new_card.card_rank]

        # if the player is dealt an ace then it adds to the players number of aces, which will  be used for changing
        # aces value from 11 to 1
        if new_card.card_rank == "A":
            self.total_aces += 1
            # When an ace is added to the hand aces_not_reduced increases. When an ace changes from 11 to 1
            # aces_not_reduced will decrease
            self.aces_not_reduced += 1


class Deck:
    # Creates and holds a four decks of 52 unique cards that eventually gets smaller as deal is called

    def __init__(self):
        # deck is a list of the card objects

        self.deck = []
        # Create a stack of 4 decks of 52 cards
        for s in suits:
            for r in card_ranks:
                # Adds four of each cards
                self.deck.extend([Card(r, s) for i in range(4)])
        # shuffle the deck
        random.shuffle(self.deck)

    def deal(self):
        # Removes the last card object from the deck and returns it
        return self.deck.pop()


#######################################################################################

direc_loc = "/Users/AidanLee/Desktop/Blackjack_Sim/"

# Create the directory for holding simulation data
try:
    os.mkdir(direc_loc + "Diff_start_card")
# Prints an error if the folder has already been created
except:
    print("Folder already exists")

try:
    os.mkdir(direc_loc + "Diff_start_card/DiffPerspective")
# Prints an error if the folder has already been created
except:
    print("Folder already exists")

# This holds all of the data in the form lists_of_lists_of_data[starting card][ending hand value]
# AKA [[all the ending values % when the dealer starts with a 2],[" " 3], etc.]
start_card_and_end_value_data = []

# All of the possible cards a dealer could have as their showing card (Jack, King, and Queen are ignored because same
# as 10. Used for the dictionary to get the card values, but also for naming files
starting_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]

# Index that runs through all of the possible starting cards a dealer can show
start_card_index = 0

# Instead of plotting all of the data, a list is made and when the number of hands that have been simulated equals the
# the value in this list, the data is recorded for plotting and for a text file
data_recorded = []
# The following range is the hand simulation numbers that will be recorded range(start,final, increment)
# I chose to not starting taking data until 20,000 simulations because I want the data to somewhat converge, so that the
# scale of the vertical axes are not between 0 and 100 percent
for starting_value in range(50, 30000, 250):
    data_recorded.append(starting_value)

# First loop that simulates the dealer starting with one specific card over and over again set by the previous two lines
# of code
while start_card_index < len(starting_cards):

    # print just to keep track of the progress of the simulations
    print(starting_cards[start_card_index])

    # Keeps track of what occurs during each simulated hand
    num_of_bust = 0
    num_of_seventeen = 0
    num_of_eighteen = 0
    num_of_nineteen = 0
    num_of_twenty = 0
    num_of_twenty_one = 0

    # Holds the percentage that this value is ended on each time data is recorded
    list_of_17 = []
    list_of_18 = []
    list_of_19 = []
    list_of_20 = []
    list_of_21 = []
    list_of_bust = []

    # Loops the dealer's hand simulation with a specific starting card over and over again
    index_of_rounds = 1
    while index_of_rounds <= data_recorded[-1]:
        # Create a brand stack of four 52 card decks and shuffles them
        the_deck = Deck()
        # Creates an empty hand for the player
        dealer_hand = Hand()

        # Force the dealer's first card to be a specific card (suit doesn't matter so I just call it "suit"
        first_card = Card(starting_cards[start_card_index], "suit")

        # To keep the simulation accurate for calculating probability, one instance of a card with that same value has
        # to be removed from the deck
        delete_card_index = 0
        for cards in the_deck.deck:
            # Finds one instance of that card and deletes it then breaks from the loop
            if cards.card_rank == starting_cards[start_card_index]:
                the_deck.deck.pop(delete_card_index)
                break
            delete_card_index += 1

        # Gives the dealer the forced first card and then a random card because you cannot bust on two cards
        dealer_hand.add_card(first_card)
        dealer_hand.add_card(the_deck.deal())

        # dealer hits until they reach a hard seventeen or hits one more time on a soft 17
        while dealer_hand.hand_value < 17 or (dealer_hand.hand_value == 17 and
                                              dealer_hand.aces_not_reduced == dealer_hand.total_aces
                                              and dealer_hand.total_aces > 0):
            dealer_hand.add_card(the_deck.deal())
            # Check if the dealer has an ace that they can reduce from 11 to 1
            if dealer_hand.hand_value > 21:
                if dealer_hand.aces_not_reduced > 0:
                    # Subtracts 10 is the same as changing the ace from an 11 to 1
                    dealer_hand.hand_value -= 10
                    # Reduces this variable so that the ace can't be used to reduce the value by 10 again
                    dealer_hand.aces_not_reduced -= 1
                # if the dealer doesn't have any aces to reduce their hand then they bust
                else:
                    dealer_hand.bust = True

        # record outcome
        if not dealer_hand.bust:
            if dealer_hand.hand_value == 17:
                num_of_seventeen += 1
            elif dealer_hand.hand_value == 18:
                num_of_eighteen += 1
            elif dealer_hand.hand_value == 19:
                num_of_nineteen += 1
            elif dealer_hand.hand_value == 20:
                num_of_twenty += 1
            elif dealer_hand.hand_value == 21:
                num_of_twenty_one += 1
        else:
            num_of_bust += 1

        # Record the data only for certain simulation number results
        if index_of_rounds in data_recorded:
            list_of_17.append(100 * num_of_seventeen / index_of_rounds)
            list_of_18.append(100 * num_of_eighteen / index_of_rounds)
            list_of_19.append(100 * num_of_nineteen / index_of_rounds)
            list_of_20.append(100 * num_of_twenty / index_of_rounds)
            list_of_21.append(100 * num_of_twenty_one / index_of_rounds)
            list_of_bust.append(100 * num_of_bust / index_of_rounds)
        if index_of_rounds % 5000 == 0:
            print(index_of_rounds)

        index_of_rounds += 1

    # Empty temporary list
    temp_list_of_end_num = []

    # Add all of the data to the temporary list for the dealer starting with a specific hand
    temp_list_of_end_num.append(list_of_17)
    temp_list_of_end_num.append(list_of_18)
    temp_list_of_end_num.append(list_of_19)
    temp_list_of_end_num.append(list_of_20)
    temp_list_of_end_num.append(list_of_21)
    temp_list_of_end_num.append(list_of_bust)

    # lists_of_lists_of_data[starting hand value][ending hand value]
    # AKA [[all the ending values that start with 2],[all the ending values that start with 3], etc.]
    start_card_and_end_value_data.append(temp_list_of_end_num)

    # Switch to the next starting card simulation
    start_card_index += 1

# Used for naming files as well as range(len()) for number of times to loop a for loop
name_of_end_value = ["17", "18", "19", "20", "21", "Bust"]
# Sets colors for plots
plot_color = ["red", "darkorange", "yellow", "forestgreen", "turquoise", "dodgerblue", "plum",
              "hotpink", "black", "darkgray"]

# This loop creates figures for each ending outcome value (17,18,29,20,21,bust) and shows the probability that those
# outcomes would occur for each starting card
# Loop over the values that a dealer can end with
for ending_value in range(len(name_of_end_value)):
    # Loop over the number of starting cards possible
    for starting_value in range(len(starting_cards)):
        plt.plot(data_recorded, start_card_and_end_value_data[starting_value][ending_value], '-o', markersize=3,
                 color=plot_color[starting_value], label=starting_cards[starting_value])
    # fixes the legend outside of the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    # adds tick marks but no label to the right side of the vertical axes
    plt.tick_params(right=True)
    # axs = plt.subplot(1,1,1)
    plt.ylabel(f'% Dealer ends on {name_of_end_value[ending_value]}')
    # Labels right side axes?
    plt.tick_params(labeltop=False, labelright=True)
    plt.xlabel("Number of hands played in Simulation")
    plt.title("Probability that dealer ends with " + name_of_end_value[ending_value] + " based on shown card")
    plt.xlim(data_recorded[0], data_recorded[-1] + 1)
    plt.savefig(direc_loc + "Diff_start_card/" + name_of_end_value[ending_value] + ".png",
                bbox_inches='tight')
    # clear plot
    plt.clf()

# This set of for loops shows another method of illustrating the data by creating a file for each starting hand and then
# the odds that they will have each possible outcome
for starting_value in range(len(starting_cards)):
    # Loop over the values that a dealer can end with
    for ending_value in range(len(name_of_end_value)):
        # Loop over the number of starting cards possible
        plt.plot(data_recorded, start_card_and_end_value_data[starting_value][ending_value], '-o', markersize=3,
                 color=plot_color[ending_value], label=name_of_end_value[ending_value])
    # plt.legend(loc='upper right',prop={'size': 6})
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    # adds tick marks but no label to the right side of the vertical axes
    plt.tick_params(right=True)
    # axs = plt.subplot(1,1,1)
    plt.ylabel('% of dealers ending value')
    # Labels right side axes?
    plt.tick_params(labeltop=False, labelright=True)
    plt.xlabel("Number of hands played in Simulation")
    plt.title("Probability of dealer's end hand value when starting with " + starting_cards[starting_value])
    plt.xlim(data_recorded[0], data_recorded[-1] + 1)
    plt.savefig(
        direc_loc + "Diff_start_card/DiffPerspective/" + starting_cards[starting_value]
        + ".png", bbox_inches='tight')
    # clear plot
    plt.clf()

# This creates one giant plot with all of the plots put together for the first method of illustrating the data
# Locations for plots on a 3 x 2 grid of plots
subplot_locations = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
# Change size
plt.figure(figsize=(15, 10), dpi=160)
# Loop over the possible outcomes
for ending_value in range(len(name_of_end_value)):
    # Places the subplot in the correct grid location
    plt.subplot2grid((3, 2), subplot_locations[ending_value])
    # Loop over the number of starting cards possible
    for starting_value in range(len(starting_cards)):
        plt.plot(data_recorded, start_card_and_end_value_data[starting_value][ending_value], '-o', markersize=3,
                 color=plot_color[starting_value], label=starting_cards[starting_value])
    # adds tick marks but no label to the right side of the vertical axes
    plt.tick_params(right=True)
    # axs = plt.subplot(1,1,1)
    plt.ylabel('Probability', size=15)
    # Labels right side axes?
    plt.tick_params(labeltop=False, labelright=True)
    plt.xlabel("Number of Hands Simulated", size=15)
    plt.title(name_of_end_value[ending_value], size=15)
    plt.xlim(data_recorded[0], data_recorded[-1] + 1)
# Adds space between the subplots so they do not overlap
plt.subplots_adjust(wspace=0.2)
plt.subplots_adjust(hspace=0.5)
# Take the legend off the last subplot and use it as a big legend for all of the plots. Have to play with anchor values
# positions based on plots and size
plt.legend(bbox_to_anchor=(1.4, 3.2), loc='upper right', ncol=1, prop={'size': 20})
# Creates one large title for all of the plots
plt.suptitle("Probability of dealer outcomes based on starting card", size=20)
plt.savefig(direc_loc + "Diff_start_card/all_ending_values_together.png", bbox_inches='tight')
plt.clf()

# This creates one giant plot with all of the plots put together for the second method of illustrating the data
# Locations for plots on a 3 x 4 grid of plots
subplot_locations = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3)]
# Change size
plt.figure(figsize=(20, 10), dpi=160)
for starting_value in range(len(starting_cards)):
    plt.subplot2grid((3, 4), subplot_locations[starting_value])
    # Loop over the values that a dealer can end with
    for ending_value in range(len(name_of_end_value)):
        # Loop over the number of starting cards possible
        plt.plot(data_recorded, start_card_and_end_value_data[starting_value][ending_value], '-o', markersize=3,
                 color=plot_color[ending_value], label=name_of_end_value[ending_value])
    # adds tick marks but no label to the right side of the vertical axes
    plt.tick_params(right=True)
    # axs = plt.subplot(1,1,1)
    plt.ylabel('Probability', size=15)
    # Labels right side axes?
    plt.tick_params(labeltop=False, labelright=True)
    plt.xlabel("Number of Hands Simulated", size=15)
    plt.title(starting_cards[starting_value], size=15)
    plt.xlim(data_recorded[0], data_recorded[-1] + 1)
    plt.ylim(0, 50)
# Adjust subplot spacing
plt.subplots_adjust(wspace=0.4)
plt.subplots_adjust(hspace=0.5)
# Take the legend off the last subplot and use it as a big legend for all of the plots. Have to play with bbox_to_anchor
# positions based on plots and size
plt.legend(bbox_to_anchor=(3, 0.8), loc='upper right', ncol=3, prop={'size': 20})
# Creates large title for all subplots
plt.suptitle("Probability of dealer outcomes for different starting cards", size=20)
plt.savefig(direc_loc + "Diff_start_card/DiffPerspective/all_ending_values_together.png",
            bbox_inches='tight')
# clear plot
plt.clf()

# Add titles to each column for text files such as % dealer starts with 2,3,4, etc.
data_recorded.insert(0, "Num of hands in simulation")
for end_v in range(len(name_of_end_value)):
    for start_v in range(len(starting_cards)):
        start_card_and_end_value_data[start_v][end_v].insert(0, "% Dealer starts with " + starting_cards[start_v])

# Write data to files for each end value outcome possible
for end_val in range(len(name_of_end_value)):
    with open(direc_loc + "Diff_start_card/" + name_of_end_value[end_val] + ".txt",
              "w+") as new_file:
        # Loop through each row of data where the data was recorded for specific number of hands simulated
        for row in range(len(data_recorded)):
            # Write the x-axis num of hands simulated
            new_file.write(str(data_recorded[row]))
            # Now loop through the starting cards
            for start_v in range(len(starting_cards)):
                new_file.write("\t" + str(start_card_and_end_value_data[start_v][end_val][row]))
            new_file.write("\n")

# Now remove the titles so that new titles can be added when the data is illustrated with the second method with the
# starting cards as the file names
data_recorded.pop(0)
for end_v in range(len(name_of_end_value)):
    for start_v in range(len(starting_cards)):
        start_card_and_end_value_data[start_v][end_v].pop(0)

# Add titles to each column for the different perspective of illustrating the data
data_recorded.insert(0, "Num of hands in simulation")
for end_v in range(len(name_of_end_value)):
    for start_v in range(len(starting_cards)):
        start_card_and_end_value_data[start_v][end_v].insert(0, "% Dealer ends with " + name_of_end_value[end_v])

# Now write the data for each starting card option and the percentage of possible outcomes
for start_v in range(len(starting_cards)):
    with open(
            direc_loc + "Diff_start_card/DiffPerspective/" + starting_cards[start_v] + ".txt",
            "w+") as new_file:
        # Loop through each row of data where the data was recorded for specific number of hands simulated
        for row in range(len(data_recorded)):
            new_file.write(str(data_recorded[row]))
            # Now loop through the starting cards
            for end_val in range(len(name_of_end_value)):
                new_file.write("\t" + str(start_card_and_end_value_data[start_v][end_val][row]))
            new_file.write("\n")
