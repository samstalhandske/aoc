#include <fstream>
#include <iostream>
#include <vector>
#include <string>

struct Race
{
	int64_t time;
	int64_t record_distance;
};

enum class Stat
{
	Invalid,
	Time,
	Record_Distance
};

bool mm_per_ms_from_hold_time(const int64_t hold_time, const int64_t race_time, int64_t& mm_per_ms)
{
	mm_per_ms = 0;

	if (hold_time >= race_time || hold_time <= 0)
		return false;

	mm_per_ms = hold_time * (race_time - hold_time);
	return true;
}

int64_t join_digits_to_one(const std::vector<int64_t>& digits)
{
	std::string str;
	for (size_t i = 0; i < digits.size(); i++)
	{
		str += std::to_string(digits[i]);
	}
	return std::stoll(str);
}

int main()
{
	std::ifstream input_file("../input.txt");
	if (!input_file.is_open())
	{
		std::cout << "Failed to open input.txt, expected it to be in the parent directory.\n";
		return -1;
	}

	std::vector<int64_t> times;
	std::vector<int64_t> record_distances;
	Stat current_stat_to_track_when_reading_input = Stat::Invalid;

	std::string input;
	while (!input_file.eof())
	{
		input_file >> input;

		if (std::isdigit(input[0]))
		{
			int digit = std::stoi(input);

			switch (current_stat_to_track_when_reading_input)
			{
			case Stat::Time:
				times.push_back(digit);
				break;
			case Stat::Record_Distance:
				record_distances.push_back(digit);
				break;
			default:
				std::cout << "Unimplemented stat to track!" << std::endl;
				break;
			}
		}
		else
		{
			current_stat_to_track_when_reading_input = (Stat)((int)current_stat_to_track_when_reading_input + 1);
		}

		if (input_file.eof())
			break;
	}

	Race race = { join_digits_to_one(times), join_digits_to_one(record_distances) };

	int64_t number_of_ways_to_beat_record = 0;
	for (int64_t hold_time = 0; hold_time < race.time; hold_time++)
	{
		int64_t mm_per_ms = 0;

		if (!mm_per_ms_from_hold_time(hold_time, race.time, mm_per_ms))
		{
			continue;
		}

		if (mm_per_ms <= race.record_distance)
		{
			// Not fast enough to beat the record.
			continue;
		}

		number_of_ways_to_beat_record++;
	}

	std::cout << "Answer: " << number_of_ways_to_beat_record << "\n";
}