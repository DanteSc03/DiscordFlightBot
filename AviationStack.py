import requests
import json
from datetime import datetime
import discord

# API information (replace with your actual API key)
API_KEY = 'Your Secret API Key'
user_iata= input("Enter the IATA code of the airport (e.g., JFK, LAX): ").upper()
dep_BASE_URL = f'https://api.aviationstack.com/v1/flights?access_key={API_KEY}&dep_iata={user_iata}'
arr_BASE_URL = f'https://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_iata={user_iata}'

dep_api_response = requests.get(dep_BASE_URL)
arr_api_response = requests.get(arr_BASE_URL)

today = datetime.now().strftime('%Y-%m-%d')

if dep_api_response.status_code == 200 and arr_api_response.status_code == 200:
    dep_api_response_json = dep_api_response.json()
    arr_api_response_json = arr_api_response.json()

    with open('departure_data.json', 'w') as f:
        json.dump(dep_api_response_json, f, indent=4) 

    with open('arrival_data.json', 'w') as f:
        json.dump(arr_api_response_json, f, indent=4) 

    print("Data saved to data.json")


    # Handling Departures
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

                print(f"Departures from {departure_airport} ({departure_iata}) for today:")
                print(f"Flight Number: {flight_number}")
                print(f"Departure Time: {scheduled_departure_time}")
                print(f"Flight Status: {flight_status}")
                print(f"Airline: {flight_airline}")
                print(f"Arrival Airport: {arrival_airport} ({arrival_iata})")
                print(f"Scheduled arrival time: {scheduled_arrival_time}")
                print(f"Aircraft: {aircraft}")
                print('-' * 40) 
            
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

                    print(f"Arrivals to {arrival_airport} ({arrival_iata}) for today:")
                    print(f"Flight Number: {flight_number}")
                    print(f"Departure Airport: {departure_airport} ({departure_iata})")
                    print(f"Scheduled departure time: {scheduled_departure_time}")
                    print(f"Flight Status: {flight_status}")
                    print(f"Arrival Time: {scheduled_arrival_time}")
                    print(f"Airline: {flight_airline}")
                    print(f"Aircraft: {aircraft}")
                    print('-' * 40) 
                

    else:
        print("No flight data available.")
else:
    print(f"Error fetching data: {dep_api_response.status_code}")




