using System;
using System.IO;
using System.Collections.Generic;
using System.Text;

static class Program
{
	struct Game
	{
		public uint Index;
		public List<Cube_Set> Cube_Sets;
	}

	struct Cube_Set
	{
		public Dictionary<Token.Token_Type, uint> Cubes;
	}

	struct Token
	{
		public enum Token_Type
		{
			Game,
			Red,
			Green,
			Blue,
			Digit,
			Colon,
			Semicolon,
			End_Of_Line,
		}

		public Token_Type type;
		public string value;
	}

	
	static void Main()
	{
		var games = new List<Game>();

		foreach(string input in File.ReadLines("../input.txt"))
		{
			var tokens = Lex_Input(input);
			games.Add(Tokens_To_Game(tokens));
		}

		// The Elf would first like to know which games would have been possible if the
		// bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
		uint total_sum = 0;
		foreach(var game in Get_Possible_Games(games, max_red_cubes: 12, max_green_cubes: 13, max_blue_cubes: 14))
		{
			total_sum += game.Index;
		}

		System.Console.WriteLine("Total sum: " + total_sum);
	}

	static List<Token> Lex_Input(string input)
	{
		var tokens = new List<Token>();
		var sb = new StringBuilder();

		for(int i = 0; i < input.Length; ++i)
		{
			char c = input[i];

			if(char.IsWhiteSpace(c))
			{
				continue;
			}
			
			if(c == ':')
			{
				tokens.Add(new Token() { type = Token.Token_Type.Colon });
			}
			else if(c == ';')
			{
				tokens.Add(new Token() { type = Token.Token_Type.Semicolon });
			}
			else if(char.IsDigit(c))
			{
				var temp_index = i + 1;
				var temp_char = input[temp_index];
				sb.Clear();
				sb.Append(c);
				while(char.IsDigit(temp_char))
				{
					sb.Append(temp_char);
					if(temp_index + 1 >= input.Length)
					{
						break;
					}

					temp_index += 1;
					temp_char = input[temp_index];
				}

				var value = sb.ToString();
				i += value.Length - 1;
				tokens.Add(new Token() { type = Token.Token_Type.Digit, value = value });
			}
			else if(char.IsLetter(c))
			{
				var temp_index = i + 1;
				var temp_char = input[temp_index];
				sb.Clear();
				sb.Append(c);
				while(char.IsLetter(temp_char))
				{
					sb.Append(temp_char);

					if(temp_index + 1 >= input.Length)
					{
						break;
					}

					temp_index += 1;
					temp_char = input[temp_index];
				}

				var value = sb.ToString();
				i += value.Length - 1;

				Token.Token_Type type = Token.Token_Type.Game;
				if(value == "red")
				{
					type = Token.Token_Type.Red;
				}
				else if(value == "green")
				{
					type = Token.Token_Type.Green;
				}
				else if(value == "blue")
				{
					type = Token.Token_Type.Blue;
				}
				tokens.Add(new Token() { type = type });
			}
		}

		tokens.Add(new Token() { type = Token.Token_Type.End_Of_Line });

		return tokens;
	}

	static Game Tokens_To_Game(List<Token> tokens)
	{
		var game = new Game();

		game.Index = uint.Parse(tokens[1].value);
		game.Cube_Sets = new List<Cube_Set>();

		int current_token_index = 3;
		int cube_set_count = 0;

		while(true)
		{
			if(game.Cube_Sets.Count <= cube_set_count)
			{
				var cube_set = new Cube_Set();
				cube_set.Cubes = new Dictionary<Token.Token_Type, uint>()
				{
					{ Token.Token_Type.Red, 0 },
					{ Token.Token_Type.Green, 0 },
					{ Token.Token_Type.Blue, 0 }
				};
				game.Cube_Sets.Add(cube_set);
			}

			var digit = tokens[current_token_index];
			var color = tokens[current_token_index + 1];

			var decider = tokens[current_token_index + 2];

			var cube_dictionary = game.Cube_Sets[cube_set_count].Cubes;
			cube_dictionary[color.type] += uint.Parse(digit.value);

			if(decider.type == Token.Token_Type.Semicolon)
			{
				// End of set.
				cube_set_count += 1;
				current_token_index += 3;
			}
			else if(decider.type == Token.Token_Type.End_Of_Line)
			{
				// End of set, plus break.
				cube_set_count += 1;
				break;
			}
			else
			{
				current_token_index += 2;
			}
		}

		return game;
	}

	static List<Game> Get_Possible_Games(List<Game> games, uint max_red_cubes, uint max_green_cubes, uint max_blue_cubes)
	{
		var possible_games = new List<Game>();
		
		foreach(var game in games)
		{
			bool game_is_possible = true;

			foreach(var cube_set in game.Cube_Sets)
			{
				bool possible = 
					cube_set.Cubes[Token.Token_Type.Red] <= max_red_cubes &&
					cube_set.Cubes[Token.Token_Type.Green] <= max_green_cubes &&
					cube_set.Cubes[Token.Token_Type.Blue] <= max_blue_cubes
				;

				if(!possible)
				{
					game_is_possible = false;
					break;
				}
			}

			if(game_is_possible)
			{
				possible_games.Add(game);
			}
		}

		return possible_games;
	}
}