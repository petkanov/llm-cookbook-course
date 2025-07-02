import modal
from modal import App, Image

app = App("Location-Function")

@app.function(image = Image.debian_slim().pip_install("requests"))
def my_location():
    import requests

    location_data = requests.get('http://ip-api.com/json').json()

    city, country, ip_address = location_data['city'], location_data['country'], location_data['query']
    temperature = requests.get(f"https://wttr.in/{city}?format=%t&m").text.strip()

    response = f"Code running on IP {ip_address} ({city}, {country}) Outside is: {temperature}"
    print(response)

    return response