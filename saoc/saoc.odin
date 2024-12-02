package saoc

import "core:os"
import "core:fmt"
import "core:time"
import "core:strconv"

Solution :: proc(input: []u8) -> int

Solution_Index :: enum {
	First,
	Second,
}

Context :: struct {
	solutions: [len(Solution_Index)]Solution,
	print_input: bool,
}

solve :: proc(c: ^Context, index: Solution_Index, example := false, expected_result := max(int)) -> int {
	using c

	fmt.printf("Solving %v (example: %v) ...\n", index, example)

	input_path := fmt.tprintf("%v_%v.txt", example ? "example" : "input", i32(index) + 1)

	input, success := os.read_entire_file_from_filename(input_path)
	defer delete(input)
	assert(success, fmt.tprintf("Failed to read input, path: %v", input_path))

	if print_input {
		fmt.println("Input:")
		fmt.println(transmute(string)input)
		fmt.println()
	}

	solution := solutions[i32(index)]
	assert(solution != nil, "Missing solution.")

	sw: time.Stopwatch
	time.stopwatch_start(&sw)
	result := solution(input)
	time.stopwatch_stop(&sw)

	fmt.println(" Result:", result)
	fmt.printf(" Duration: %.6v ms\n\n", time.duration_milliseconds(time.stopwatch_duration(sw)))

	if expected_result != max(int) {
		assert(result == expected_result, fmt.tprintf("	Expected %v, got %v.", expected_result, result))
	}

	return result
}