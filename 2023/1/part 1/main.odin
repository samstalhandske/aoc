package main

import "core:fmt"
import "core:os"
import "core:strings"
import "core:strconv"

input_path := "../input.txt"

main :: proc() {
	data, ok := os.read_entire_file(input_path, context.allocator)
	if(!ok)
	{
		return;
	}
	defer delete(data, context.allocator)

	total_sum: int
	results: [2]byte
	temp: byte

	result_string_builder := strings.builder_make()

	it := string(data)
	for line in strings.split_lines_iterator(&it)
	{
		// Finds the first digit
		for c in line
		{
			temp := byte(c)
			if(is_num(temp))
			{
				results[0] = byte(c)
				break
			}
		}

		// Finds the last digit
		#reverse for c in line
		{
			temp := byte(c)
			if(is_num(temp))
			{
				results[1] = byte(c)
				break
			}
		}

		// Clear/reset the string-builder
		strings.builder_reset(&result_string_builder)

		// Join the found bytes together to get a string
		strings.write_bytes(&result_string_builder, results[:])
		s := strings.to_string(result_string_builder)

		total_sum += strconv.atoi(s)
	}

	fmt.println("total sum:", total_sum)
}

is_num :: proc(c: byte) -> bool
{
	return c >= 48 && c <= 57
}