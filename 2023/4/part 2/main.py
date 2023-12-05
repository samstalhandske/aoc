import os

def main():
	file = open(os.path.dirname(os.path.dirname( __file__ )) + "\\input.txt")
	cards = file.read().splitlines()

	# This is where we set up the cards.
	# Each card is assigned it's index, the number of cards it will affect as well as the 
	# amount of copies. Since we start with the cards, each card category's count will be 1.
	card_list = []
	card_index = 0
	for card in cards:
		matching_numbers_count = get_matching_numbers_in_card(card)
		card_list.append([card_index, matching_numbers_count, 1])
		card_index += 1

	# Here we create a list which we'll use as a stack.
	# The existing cards are added in reversed order to get the order right when looping.
	new_cards = []
	for card in reversed(card_list):
		new_cards.append(card)

	while len(new_cards) > 0:
		card = new_cards.pop() # Pop the top card
		for i in range(card[1]): # Loop 'matching_numbers_count' times
			target_card_index = card[0] + i + 1	# Calculate the index of the card to copy
			card_list[target_card_index][2] += 1 # Increment the amount of copies we have of the card at 'target_card_index'.
			new_cards.append(card_list[target_card_index]) # Create a copy and add it to the top of the stack.

	# Add each card's amount of copies together to get the final result.
	total_sum = 0
	for card in card_list:
		total_sum += card[2] 
	
	print(f"total sum: {total_sum}")

def get_matching_numbers_in_card(line):
	# Remove the 'Card X: ' part from the line as it's not necessary to keep.
	line = line[(line.find(':') + 1):]
	
	winning_numbers = []
	my_numbers = []
	
	collecting_winning_numbers = True
	
	# Check every space-seperated entry.
	for entry in line.split():
		if entry == '|':
			# If we've reached the divider, stop appending the winning numbers and start append our numbers.
			collecting_winning_numbers = False
			continue

		if collecting_winning_numbers:
			winning_numbers.append(int(entry))
		else:
			my_numbers.append(int(entry))

	# Count the amount of matching numbers by comparing our numbers to the winning numbers.
	matching_numbers = 0
	for my_number in my_numbers:
		for winning_number in winning_numbers:
			if my_number == winning_number:
				matching_numbers += 1
	
	return matching_numbers
	
main()