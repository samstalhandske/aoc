package main

import "core:fmt"
import "core:os"
import "core:strings"
import "core:strconv"
import "core:slice"

input_path := "../input.txt"

spelled_out_digits := map[string]byte {
	"zero" = 0,
	"one" = 1,
	"two" = 2,
	"three" = 3,
	"four" = 4,
	"five" = 5,
	"six" = 6,
	"seven" = 7,
	"eight" = 8,
	"nine" = 9,
}

main :: proc() {
	data, ok := os.read_entire_file(input_path, context.allocator)
	if(!ok)
	{
		return;
	}
	defer delete(data, context.allocator)

	total_sum: int

	result_string_builder := strings.builder_make()
	defer strings.builder_destroy(&result_string_builder)

	it := string(data)
	for line in strings.split_lines_iterator(&it)
	{
		digits := get_digits_in_string(line)
		defer delete_dynamic_array(digits)

		strings.builder_reset(&result_string_builder)
		strings.write_byte(&result_string_builder, digits[0] + 48)
		strings.write_byte(&result_string_builder, digits[len(digits)-1] + 48)
		parsed_value, success := strconv.parse_int(strings.to_string(result_string_builder))
		total_sum += parsed_value
	}

	fmt.println("total sum:", total_sum)
}

Number_Value :: struct
{
	value: byte,
	index: int
}

get_digits_in_string :: proc(str: string) -> [dynamic]byte
{
	clean_str := str

	i: int = 0
	buf: [4]byte
	for i < len(str)
	{
		if(is_num(byte(str[i])))
		{
			key, success := number_to_word(byte(str[i]))
			val := strconv.itoa(buf[:], auto_cast str[i] - 48)
			new_string, ok := strings.replace_all(clean_str, val, key)
			clean_str = new_string
		}
		i += 1
	}

	number_values: [dynamic]Number_Value

	for key, value in spelled_out_digits
	{
		i := 0;
		for i < len(clean_str)
		{
			index := strings.index(clean_str[i:], key)

			if(index < 0)
			{
				break
			}

			append(&number_values, Number_Value {value, index + i})
			
			i += index + 1;
		}
	}

	i = 0
	for i < len(number_values)
	{
		j := i + 1

		for j < len(number_values)
		{
			a := number_values[i]
			b := number_values[j]

			if(a.index > b.index)
			{
				temp := a
				number_values[i] = b
				number_values[j] = temp
			}

			j += 1
		}
		
		i += 1
	}

	to_return: [dynamic]byte
	for	element, index in number_values
	{
		append(&to_return, element.value)
	}

	return to_return
}

is_num :: proc(c: byte) -> bool
{
	return c >= 48 && c <= 57
}

number_to_word :: proc(num: byte) -> (key: string, success: bool)
{
	for key, value in spelled_out_digits
	{
		if(num - 48 == byte(value))
		{
			return key, true
		}
	}

	return "", false
}