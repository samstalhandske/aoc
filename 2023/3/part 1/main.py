import os

part_numbers = []

def main():
	file = open(os.path.dirname(os.path.dirname( __file__ )) + "\\input.txt")
	lines = file.read().splitlines()

	matrix = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]

	temp_x = 0
	temp_y = 0

	# Step one, add (and clean up) the input to a 2d-array.
	for line in lines:
		for symbol in line:
			if symbol == '.':
				symbol = None
			elif symbol.isdigit() == False:
				symbol = '#'
			matrix[temp_y][temp_x] = symbol
			temp_x += 1
		temp_y += 1
		temp_x = 0
	
	# Step two, scan for numbers and add them to part_numbers if they are one.
	for row_index, row in enumerate(matrix):
		number_buffer = ""
		for col_index, symbol in enumerate(row):
			if symbol != None and symbol != '#':
				number_buffer += symbol
			else:
				if len(number_buffer) > 0:
					add_number_if_part_number(matrix, number_buffer, col_index, row_index)
					number_buffer = ""
		
		if len(number_buffer) > 0:
			add_number_if_part_number(matrix, number_buffer, col_index, row_index)
			number_buffer = ""

	# Step 3, get the sum of all part-numbers
	total_sum = 0
	for num in part_numbers:
		total_sum += int(num)

	print(f"Total sum: {total_sum}")

def add_number_if_part_number(matrix, number, x, y):
	for symbol in get_adjacent_symbols(matrix, number, x, y):
		if symbol_is_part_number(symbol):
			part_numbers.append(number)
			return

def get_adjacent_symbols(matrix, number, x, y):
	adjacent = []

	x -= len(number)

	for w in range(-1, len(number) + 1):
		adjacent.append(get_symbol_at_x_y(matrix, x + w, y - 1))
		adjacent.append(get_symbol_at_x_y(matrix, x + w, y + 1))
	
	adjacent.append(get_symbol_at_x_y(matrix, x - 1, y))
	adjacent.append(get_symbol_at_x_y(matrix, x + len(number), y))

	return adjacent

def symbol_is_part_number(symbol):
	return symbol != None and symbol == '#'

def get_symbol_at_x_y(matrix, x, y):
	if x < 0 or x >= len(matrix):
		return None
	if y < 0 or y >= len(matrix):
		return None
	
	return matrix[y][x]
	
if __name__ == "__main__":
	main()