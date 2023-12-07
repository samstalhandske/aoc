#include <fstream>
#include <iostream>
#include <vector>
#include <string>

struct Race
{
	int time;
	int record_distance;
};

enum class Stat
{
	Invalid,
	Time,
	Record_Distance
};

bool mm_per_ms_from_hold_time(const int hold_time, const int race_time, int& mm_per_ms)
{
	mm_per_ms = 0;

	if (hold_time >= race_time || hold_time <= 0)
		return false;

	mm_per_ms = hold_time * (race_time - hold_time);
	return true;
}

int main()
{
	std::ifstream input_file("../input.txt");
	if (!input_file.is_open())
	{
		std::cout << "Failed to open input.txt, expected it to be in the parent directory.\n";
		return -1;
	}

	std::vector<int> times;
	std::vector<int> record_distances;
	Stat current_stat_to_track_when_reading_input = Stat::Invalid;

	std::vector<Race> races;

	std::string input;
	while (input_file)
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
			}
		}
		else
		{
			current_stat_to_track_when_reading_input = (Stat)((int)current_stat_to_track_when_reading_input + 1);
		}
	}

	for (size_t i = 0; i < times.size(); i++)
	{
		races.push_back(Race { times[i], record_distances[i] });
	}

	int answer = 0;

	int i = 0;
	for (auto& race : races)
	{
		int number_of_ways_to_beat_record = 0;
		for (int hold_time = 0; hold_time < race.time; hold_time++)
		{
			int mm_per_ms = 0;

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

		if (answer <= 0)
			answer = 1;

		answer *= number_of_ways_to_beat_record;

		i++;
	}

	printf("Answer: %i", answer);
}