import os

def main():
	file = open(os.path.dirname(os.path.dirname( __file__ )) + "\\input.txt")
	lines = file.read().splitlines()

	seed_input = lines[0]
	seed_values = seed_input.split()
	seeds = seed_values[1:] # Skip the first index as that is just 'seeds:'
	print(f"Seeds: {seeds}")

	converters = []
	current_converter_index = -1
	for line in lines[2:]:
		if len(line) == 0:
			continue

		comma = line.find(" map:")
		if comma >= 0:
			current_converter_index += 1
			converters.append((line[:comma], []))
		else:
			converters[current_converter_index][1].append(line.split())

	lowest_location = None		
	for seed in seeds:
		value = int(seed)
		for converter in converters:
			for converter_entries in converter[1]:
				source_range_start 		= int(converter_entries[1])
				range_length 			= int(converter_entries[2])

				if value in range(source_range_start, source_range_start + range_length):
					destination_range_start = int(converter_entries[0])
					value += destination_range_start - source_range_start
					break

		if lowest_location == None:
			lowest_location = value
		else:
			if value < lowest_location:
				lowest_location = value
	
	print(f"Lowest location: {lowest_location}")

main()