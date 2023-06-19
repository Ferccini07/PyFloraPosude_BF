import requests
from xml.etree import ElementTree as ET

result = []
web_site = f"https://vrijeme.hr/hrvatska_n.xml"


def get_current_weather():
    # sending get request and saving the response as response object
    try:
        response = requests.get(url=web_site)
        print(response)

        tree = ET.fromstring(response.content)
        for grad in tree.findall("Grad"):
            grad_ime = grad.find("GradIme").text
            if grad_ime == "Zagreb-Maksimir":
                data = {
                    "City Name": grad_ime,
                    "Temperature": grad.find("Podatci/Temp").text,
                    "Humidity": grad.find("Podatci/Vlaga").text,
                    "Pressure": grad.find("Podatci/Tlak").text,
                    "Wind direction": grad.find("Podatci/VjetarSmjer").text,
                    "Wind speed": grad.find("Podatci/VjetarBrzina").text,
                    "Weather": grad.find("Podatci/Vrijeme").text,
                }
                for i, j in data.items():
                    value = f"{i}: {j}"
                    result.append(value)
                return result

    except:
        return ["Bad Connection"]
