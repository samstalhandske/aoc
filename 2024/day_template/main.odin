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

	saoc.solve(&ctx, .First,  example = true, expected_result = 0)
	saoc.solve(&ctx, .Second, example = true, expected_result = 0)

	saoc.solve(&ctx, .First)
	saoc.solve(&ctx, .Second)
}

solution_1 :: proc(input: []u8) -> int {
	panic("TODO!")
}

solution_2 :: proc(input: []u8) -> int {
	panic("TODO!")
}