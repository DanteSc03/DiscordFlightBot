# Discord Airport Flight Bot

A Discord bot that provides real-time flight arrival and departure information for airports using their IATA code, powered by the [AviationStack API](https://aviationstack.com/).

## Features
- Responds to user greetings and prompts for an IATA airport code.
- Retrieves and displays flight information including status, times, and airline details.
- Saves flight data to local files `departure_data.json` and `arrival_data.json`.

## Requirements
- A [Discord Bot Token](https://discordpy.readthedocs.io/en/stable/discord.html).
- An API key from [AviationStack](https://aviationstack.com/).
- Python 3.6+.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/DanteSc03/DiscordFlightBot.git

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Add your Discord Bot Token and AviationStack API key in the script:
    - Rename `.env.sample` to `.env` and paste in your keys.

4. Run the bot:
    ```bash 
    python bot.py

## Usage
1. Start the bot and greet it with hello in your Discord Server
2. The bot will prompt for an IATA airport code (ex: LAX, JFK, etc...)
3. Bot retrieves and displays flight information in the chat (data is also locally stored)

## License
This project is under the MIT license. Feel free to fork the repo and make suggestions with pull requests. All suggestions are welcome.
