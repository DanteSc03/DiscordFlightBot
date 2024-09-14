import discord
from discord.ext import commands
import aiohttp
import json
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

class Bot(commands.Bot):
    async def on_ready(self):
        print(f'We have logged in as {self.user}!')

#Setting up the bot
intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

@bot.command()
async def flight_data(ctx, flight_code):
    if len(flight_code) == 3 and not flight_code == 'bye' and not flight_code == 'hey'and not flight_code == 'hi!':
        await ctx.send(f'You entered {flight_code.upper()}! Retrieving data...')
        user_iata = flight_code.upper()

        API_KEY = os.getenv('API_KEY')
        dep_BASE_URL = f'https://api.aviationstack.com/v1/flights?access_key={API_KEY}&dep_iata={user_iata}'
        arr_BASE_URL = f'https://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_iata={user_iata}'

        async with aiohttp.ClientSession() as session:
            async with session.get(dep_BASE_URL) as dep_api_response:
                dep_api_response_json = await dep_api_response.json()
                if dep_api_response.status != 200:
                    await ctx.send(f"Error fetching data: {dep_api_response.status}")

                    return

            async with session.get(arr_BASE_URL) as arr_api_response:
                arr_api_response_json = await arr_api_response.json()
                if arr_api_response.status != 200:
                    await ctx.send(f"Error fetching data: {arr_api_response.status}")
                    
                    return

        today = datetime.now().strftime('%Y-%m-%d')

        if dep_api_response.status_code == 200 and arr_api_response.status_code == 200:
            with open('departure_data.json', 'w') as f:
                json.dump(dep_api_response_json, f, indent=4) 

            with open('arrival_data.json', 'w') as f:
                json.dump(arr_api_response_json, f, indent=4) 

            print("Data saved to arrival_data.json and departure_data.json")


            # Handling Departures and extracting necessary data
            if 'data' in dep_api_response_json and len(dep_api_response_json['data']) > 0:
            
                flight_info = dep_api_response_json['data']  

                for flight_info in dep_api_response_json['data']:

                    departure_iata = flight_info.get('departure', {}).get('iata', '')

                    if departure_iata == user_iata and not flight_info.get('flight',{}).get('codeshared',{}) and flight_info.get('flight_date') == today:
                    
                        flight_status = flight_info.get('flight_status', 'N/A')
                        flight_airline = flight_info.get('flight', {}).get('name', 'N/A')
                        departure_iata = flight_info.get('departure', {}).get('iata', 'N/A')
                        departure_airport = flight_info.get('departure', {}).get('airport', 'N/A')
                        arrival_iata = flight_info.get('arrival', {}).get('iata', 'N/A')
                        arrival_airport = flight_info.get('arrival', {}).get('airport', 'N/A')
                        scheduled_departure_time = flight_info.get('departure', {}).get('scheduled', 'N/A')
                        scheduled_arrival_time = flight_info.get('arrival', {}).get('scheduled', 'N/A')
                        flight_number = flight_info.get('flight', {}).get('iata', 'N/A')

                        #Time Processing
                        scheduled_arrival_time = datetime.fromisoformat(scheduled_arrival_time)
                        scheduled_departure_time = datetime.fromisoformat(scheduled_departure_time)

                        scheduled_arrival_time = scheduled_arrival_time.strftime('%H:%M')
                        scheduled_departure_time = scheduled_departure_time.strftime('%H:%M')

                        await ctx.send(
                            f"Departure from {departure_airport} ({departure_iata}) for today:\n"
                            f"Airline: {flight_airline}\n"
                            f"Flight Number: {flight_number}\n"
                            f"Departure Time: {scheduled_departure_time}\n"
                            f"Flight Status: {flight_status}\n"
                            f"Scheduled Arrival Time: {scheduled_arrival_time}\n"
                            f"Arrival Airport: {arrival_airport} ({arrival_iata})\n"
                            )

            # Handling Arrivals and extracting necessary data
            if 'data' in arr_api_response_json and len(arr_api_response_json['data']) > 0:

                    flight_info = arr_api_response_json['data']  

                    for flight_info in arr_api_response_json['data']:

                        arrival_iata = flight_info.get('arrival', {}).get('iata', '')

                        if arrival_iata == user_iata and not flight_info.get('flight',{}).get('codeshared',{}) and flight_info.get('flight_date') == today:
                        
                            flight_status = flight_info.get('flight_status', 'N/A')
                            flight_airline = flight_info.get('airline', {}).get('name', 'N/A')
                            departure_iata = flight_info.get('departure', {}).get('iata', 'N/A')
                            departure_airport = flight_info.get('departure', {}).get('airport', 'N/A')
                            arrival_iata = flight_info.get('arrival', {}).get('iata', 'N/A')
                            arrival_airport = flight_info.get('arrival', {}).get('airport', 'N/A')
                            scheduled_departure_time = flight_info.get('departure', {}).get('scheduled', 'N/A')
                            scheduled_arrival_time = flight_info.get('arrival', {}).get('scheduled', 'N/A')
                            flight_number = flight_info.get('flight', {}).get('iata', 'N/A')

                            #Time Processing
                            scheduled_arrival_time = datetime.fromisoformat(scheduled_arrival_time)
                            scheduled_departure_time = datetime.fromisoformat(scheduled_departure_time)

                            scheduled_arrival_time = scheduled_arrival_time.strftime('%H:%M')
                            scheduled_departure_time = scheduled_departure_time.strftime('%H:%M')

                            await ctx.send(
                                f"Arrival to {arrival_airport} ({arrival_iata}) for today:\n"
                                f"Airline: {flight_airline}\n"
                                f"Flight Number: {flight_number}\n"
                                f"Scheduled Departure Time: {scheduled_departure_time}\n"
                                f"Departure Airport: {departure_airport} ({departure_iata})\n"
                                f"Flight Status: {flight_status}\n"
                                f"Arrival Time: {scheduled_arrival_time}\n"
                                )

            else:
                await ctx.send(f"No data found for {user_iata} for today.")
        else:
            await ctx.send("Error fetching data. Please try again later.")

bot.run(os.getenv('DISCORD_TOKEN'))
