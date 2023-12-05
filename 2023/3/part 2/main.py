import os

part_numbers = []
gears = []

def main():
	file = open(os.path.dirname(os.path.dirname( __file__ )) + "\\input.txt")
	lines = file.read().splitlines()

	matrix = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]

	temp_x = 0
	temp_y = 0

	# Step one, add the input to a 2d-array.
	for line in lines:
		for symbol in line:
			if symbol == '.':
				symbol = None
			elif symbol.isdigit() == False:
				if symbol != '*':
					symbol = '#'
			matrix[temp_y][temp_x] = symbol
			temp_x += 1
		temp_y += 1
		temp_x = 0
	
	# Step two, scan for numbers and add them to part_numbers if they are one.
	for row_index, row in enumerate(matrix):
		number_buffer = ""
		for col_index, symbol in enumerate(row):
			if symbol != None and symbol.isdigit():
				number_buffer += symbol
			else:
				if symbol == '*':
					gears.append((col_index + 1, row_index))

				if len(number_buffer) > 0:
					add_number_if_part_number(matrix, number_buffer, col_index, row_index)
					number_buffer = ""
		
		if len(number_buffer) > 0:
			add_number_if_part_number(matrix, number_buffer, col_index, row_index)
			number_buffer = ""

	# Step three, go through all the gears and calculate one-dimensional values 
	# which we'll then use to find out what part_numbers to multiply together.
	sum_of_gear_ratios = 0

	for gear in gears:
		adjacent = get_adjacent_symbols(matrix, '*', gear[0], gear[1])
		a = None
		b = None
		need_none = False
		for adjacent_symbol in adjacent:
			if need_none == True:
				if adjacent_symbol[0] is None:
					need_none = False
				else:
					continue
				
			if adjacent_symbol[0] != None and adjacent_symbol[0].isdigit():
				if a == None:
					a = adjacent_symbol
					need_none = True
				elif b == None:
					b = adjacent_symbol
					need_none = True
				else:
					break

		if a == None or b == None:
			# Invalid gear.
			continue
			
		a_1d = to_one_dimensional_value(matrix, a[1], a[2])
		b_1d = to_one_dimensional_value(matrix, b[1], b[2])

		a_num = None
		for number in reversed(part_numbers):
			number_1d = number[1]
			if number_1d <= a_1d:
				a_num = number[0]
				break
		b_num = None
		for number in reversed(part_numbers):
			number_1d = number[1]
			if number_1d <= b_1d:
				b_num = number[0]
				break

		gear_ratio = int(a_num) * int(b_num)
		sum_of_gear_ratios += gear_ratio
	
	print(f"Sum of all of the gear ratios in my engine schematic: {sum_of_gear_ratios}")

def to_one_dimensional_value(matrix, x, y):
	return len(matrix[0]) * y + x

def add_number_if_part_number(matrix, number, x, y):
	for symbol in get_adjacent_symbols(matrix, number, x, y):
		if symbol_is_part_number(symbol[0]):
			one_dimensional_value = to_one_dimensional_value(matrix, x, y) - len(number)
			part_numbers.append((number, one_dimensional_value))
			return

def get_adjacent_symbols(matrix, number, x, y):
	adjacent = []

	x -= len(number)
	width = len(number) + 2

	for w in range(0, width):  # Top
		symbol = get_symbol_at_x_y(matrix, x + w - 1, y - 1)
		adjacent.append(symbol)

	adjacent.append((None, -1, -1)) # Seperator

	for w in range(0, width):  # Bottom
		symbol = get_symbol_at_x_y(matrix, x + w - 1, y + 1)
		adjacent.append(symbol)

	adjacent.append((None, -1, -1)) # Seperator
	# Left
	adjacent.append(get_symbol_at_x_y(matrix, x - 1, y))
	adjacent.append((None, -1, -1)) # Seperator
	# Right
	adjacent.append(get_symbol_at_x_y(matrix, x + width - 2, y))

	return adjacent

def symbol_is_part_number(symbol):
	return symbol is not None and symbol in ['#', '*']

def get_symbol_at_x_y(matrix, x, y):
	if x < 0 or x >= len(matrix):
		return (None, -1, -1)
	if y < 0 or y >= len(matrix):
		return (None, -1, -1)
	
	return (matrix[y][x], x, y)
	
if __name__ == "__main__":
	main()