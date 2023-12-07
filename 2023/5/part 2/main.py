import os

def main():
	file = open(os.path.dirname(os.path.dirname( __file__ )) + "\\input.txt")
	lines = file.read().splitlines()

	seed_input = lines[0]
	seed_values = seed_input.split()[1:]
	seeds = []
	for i in range(0, len(seed_values), 2):
		start = int(seed_values[i])
		length = int(seed_values[i + 1])
		seeds.append((start, start + length))

	converters = []
	current_converter_index = -1
	for line in lines[2:]:
		if len(line) == 0:
			continue
		if not line[0].isdigit():
			comma = line.find(" map:")
			if comma >= 0:
				current_converter_index += 1
				converters.append([])
		else:
			converters[current_converter_index].append(line.split())

	lowest_location = None
	for seed_pair in seeds:
		for seed in range(seed_pair[0], seed_pair[1]):
			value = int(seed)

			for converter_map in converters:
				for convert_values in converter_map:
					source_range_start 		= int(convert_values[1])
					if value < source_range_start:
						continue
					range_length 			= int(convert_values[2])

					if value - source_range_start < range_length:
						value += int(convert_values[0]) - source_range_start
						break

			if lowest_location == None:
				lowest_location = value
			else:
				if value < lowest_location:
					lowest_location = value
	
	print(f"Lowest location: {lowest_location}")

main()