import os

def main():
	file = open(os.path.dirname(os.path.dirname( __file__ )) + "\\input.txt")
	lines = file.read().splitlines()

	total_points = 0
	card_index = 1
	for line in lines:
		points = get_points_from_card(line)
		total_points += points
		card_index += 1

	print(f"Total amount of points: {total_points}")

def get_points_from_card(line):
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

	# If we don't have any matching numbers, return.
	if matching_numbers == 0:
		return 0
	
	points = 1
	for _ in range(1, matching_numbers):
		points *= 2 # 1, 2, 4, 8, etc.
	
	return points
	
main()