package main

import "../../saoc"
import "core:fmt"
import "core:strconv"
import "core:bytes"
import "core:slice"

main :: proc() {
	ctx := saoc.Context {
		solutions = { solution_1, solution_2 },
		print_input = false,
	}

	saoc.solve(&ctx, .First,  example = true, expected_result = 11)
	saoc.solve(&ctx, .Second, example = true, expected_result = 31)

	saoc.solve(&ctx, .First,  expected_result = 2196996)
	saoc.solve(&ctx, .Second, expected_result = 23655822)
}

solution_1 :: proc(input: []u8) -> int {
	fields := bytes.fields(input)
	defer delete(fields)

	left, right: [dynamic]int
	defer {
		delete(left)
		delete(right)
	}

	for f, index in fields {
		value, ok := strconv.parse_int(transmute(string)f)
		assert(ok)

		if index % 2 == 0 {
			append(&left, value)
		}
		else {
			append(&right, value)
		}
	}

	slice.sort(left[:])
	slice.sort(right[:])

	total_distance := 0
	for i in 0..<len(fields) / 2 {
		total_distance += abs(left[i] - right[i])
	}

	return total_distance
}

solution_2 :: proc(input: []u8) -> int {
	fields := bytes.fields(input)
	defer delete(fields)

	Location :: struct {
		times_found_in_left_array: int,
		times_found_in_right_array: uint
	}

	left: map[int]Location
	right: [dynamic]int
	defer {
		delete(left)
		delete(right)
	}

	for f, index in fields {
		value, ok := strconv.parse_int(transmute(string)f)
		assert(ok)

		if index % 2 == 0 {
			if value not_in left {
				left[value] = {}
			}

			elem := &left[value]
			elem.times_found_in_left_array += 1
		}
		else {
			append(&right, value)
		}
	}

	for r in right {
		if elem, ok := &left[r]; ok {
			elem.times_found_in_right_array += 1
		}
	}

	simularity_score := 0
	for key, value in left {
		simularity_score += value.times_found_in_left_array * (key * int(value.times_found_in_right_array))
	}

	return simularity_score
}