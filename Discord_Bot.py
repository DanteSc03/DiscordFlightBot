import discord
import requests
import json
from datetime import datetime

class Client(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}!')

    # This event triggers when a message is sent in the chat
    async def on_message(self,message):
        if message.author == self.user:
            return
        #Responding to user message to get airport code
        if message.content.startswith('hello'):
            await message.channel.send(f'Hello there {message.author}! For what airport (iata) code would you like to receive arrival and departure information? (ex: LAX, MAD, JFK)')
        #Handling user input, fetching data using API and then sending the data back to the user
        if len(message.content) == 3 and not message.content == 'bye' and not message.content == 'hey'and not message.content == 'hi!':
            await message.channel.send(f'You entered {message.content.upper()}! Retrieving data...')
            user_iata = message.content.upper()

            API_KEY = 'Your Secret API Key'
            dep_BASE_URL = f'https://api.aviationstack.com/v1/flights?access_key={API_KEY}&dep_iata={user_iata}'
            arr_BASE_URL = f'https://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_iata={user_iata}'

            dep_api_response = requests.get(dep_BASE_URL)
            arr_api_response = requests.get(arr_BASE_URL)

            today = datetime.now().strftime('%Y-%m-%d')

            #Saving data to JSON files
            if dep_api_response.status_code == 200 and arr_api_response.status_code == 200:
                dep_api_response_json = dep_api_response.json()
                arr_api_response_json = arr_api_response.json()

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
                        
                            flight_date = flight_info.get('flight_date', 'N/A')
                            flight_status = flight_info.get('flight_status', 'N/A')
                            flight_airline = flight_info.get('flight', {}).get('name', 'N/A')
                            departure_iata = flight_info.get('departure', {}).get('iata', 'N/A')
                            departure_airport = flight_info.get('departure', {}).get('airport', 'N/A')
                            arrival_iata = flight_info.get('arrival', {}).get('iata', 'N/A')
                            arrival_airport = flight_info.get('arrival', {}).get('airport', 'N/A')
                            scheduled_departure_time = flight_info.get('departure', {}).get('scheduled', 'N/A')
                            scheduled_arrival_time = flight_info.get('arrival', {}).get('scheduled', 'N/A')
                            flight_number = flight_info.get('flight', {}).get('iata', 'N/A')
                            aircraft = flight_info.get('aircraft', {}).get('iata', 'N/A')

                            #Time Processing
                            scheduled_arrival_time = datetime.fromisoformat(scheduled_arrival_time)
                            scheduled_departure_time = datetime.fromisoformat(scheduled_departure_time)

                            scheduled_arrival_time = scheduled_arrival_time.strftime('%H:%M')
                            scheduled_departure_time = scheduled_departure_time.strftime('%H:%M')

                            await message.channel.send(f"Departure from {departure_airport} ({departure_iata}) for today:")
                            await message.channel.send(f"Flight Number: {flight_number}")
                            await message.channel.send(f"Departure Time: {scheduled_departure_time}")
                            await message.channel.send(f"Flight Status: {flight_status}")
                            await message.channel.send(f"Airline: {flight_airline}")
                            await message.channel.send(f"Aircraft: {aircraft}")
                            await message.channel.send(f"Arrival Airport: {arrival_airport} ({arrival_iata})")
                            await message.channel.send(f"Scheduled arrival time: {scheduled_arrival_time}")
                            await message.channel.send('-' * 40) 

                # Handling Arrivals and extracting necessary data
                if 'data' in arr_api_response_json and len(arr_api_response_json['data']) > 0:

                        flight_info = arr_api_response_json['data']  

                        for flight_info in arr_api_response_json['data']:

                            arrival_iata = flight_info.get('arrival', {}).get('iata', '')

                            if arrival_iata == user_iata and not flight_info.get('flight',{}).get('codeshared',{}) and flight_info.get('flight_date') == today:
                            
                                flight_date = flight_info.get('flight_date', 'N/A')
                                flight_status = flight_info.get('flight_status', 'N/A')
                                flight_airline = flight_info.get('airline', {}).get('name', 'N/A')
                                departure_iata = flight_info.get('departure', {}).get('iata', 'N/A')
                                departure_airport = flight_info.get('departure', {}).get('airport', 'N/A')
                                arrival_iata = flight_info.get('arrival', {}).get('iata', 'N/A')
                                arrival_airport = flight_info.get('arrival', {}).get('airport', 'N/A')
                                scheduled_departure_time = flight_info.get('departure', {}).get('scheduled', 'N/A')
                                scheduled_arrival_time = flight_info.get('arrival', {}).get('scheduled', 'N/A')
                                flight_number = flight_info.get('flight', {}).get('iata', 'N/A')
                                aircraft = flight_info.get('aircraft', {}).get('iata', 'N/A')

                                #Time Processing
                                scheduled_arrival_time = datetime.fromisoformat(scheduled_arrival_time)
                                scheduled_departure_time = datetime.fromisoformat(scheduled_departure_time)

                                scheduled_arrival_time = scheduled_arrival_time.strftime('%H:%M')
                                scheduled_departure_time = scheduled_departure_time.strftime('%H:%M')

                                await message.channel.send(f"Arrival to {arrival_airport} ({arrival_iata}) for today:")
                                await message.channel.send(f"Flight Number: {flight_number}")
                                await message.channel.send(f"Departure Airport: {departure_airport} ({departure_iata})")
                                await message.channel.send(f"Scheduled departure time: {scheduled_departure_time}")
                                await message.channel.send(f"Flight Status: {flight_status}")
                                await message.channel.send(f"Arrival Time: {scheduled_arrival_time}")
                                await message.channel.send(f"Airline: {flight_airline}")
                                await message.channel.send(f"Aircraft: {aircraft}")
                                await message.channel.send('-' * 40) 

                else:
                    print("No flight data available.")
            else:
                print(f"Error fetching data: {dep_api_response.status_code}")

#Setting up the client
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('Your Discord Bot Token')
