import requests
import csv
from datetime import datetime


def load_data() -> dict:
    """
    функция загружает данные с Яндекс погоды
    :return: dict[str, str|int]
    """
    headers = {
        "X-Yandex-Weather-Key": "demo_yandex_weather_api_key_ca6d09349ba0"
    }
    query = """{
      Moscow: weatherByPoint(request: {lat: 55.72187, lon: 37.822243}) {
        ...WeatherData
      }
      Kazan: weatherByPoint(request: {lat: 55.79612732, lon: 49.10641479}) {
        ...WeatherData
      }
      Sankt_Peterburg: weatherByPoint(request: {lat: 59.93867493, lon: 30.31449318}) {
        ...WeatherData
      }
      Tula: weatherByPoint(request: {lat: 54.19312286, lon: 37.61734772}) {
        ...WeatherData
      }
      Novosibirsk: weatherByPoint(request: {lat: 55.03020477, lon: 82.92043304}) {
        ...WeatherData
      }
    }
    
    fragment WeatherData on Weather {
      forecast {
        days(limit: 7) {
          hours {
            time: time
            temperature_c: temperature
            pressure_mm: pressure
            is_rainy: prec
          }
        }
      }
    }"""
    variables = {}
    json_data = {"query": query, "variables": variables}
    response = requests.post("https://api.weather.yandex.ru/graphql/query", headers=headers, json=json_data).json()
    return response


def transform_data() -> list:
    """
    функция выполняет преобразование данных
    :return: список из словарей
    """
    data = load_data()
    result = []
    res = {}
    cities = ['Moscow', 'Kazan', 'Sankt_Peterburg', 'Tula', 'Novosibirsk']
    for city in cities:
        d = data['data'][city]['forecast']['days']
        for i in range(len(d)):
            for value in d[i].values():
                for a in range(len(value)):
                    res = value[a]
                    res['city'] = city
                    date_hour = res['time']
                    date = datetime.strptime(date_hour[:13], "%Y-%m-%dT%H")
                    dt = date.strftime('%d.%m.%Y')
                    res['date'] = dt
                    res['hour'] = date.time().hour
                    res['is_rainy'] = (lambda x: 1 if x > 0 else 0)(res['is_rainy'])
                    del res['time']
                    result.append(res)
    return result


def main() -> None:
    """
    формируем данные в csv-формате
    :return: csv-файл
    """
    with open('result.csv', 'w') as file:
        csv_file = csv.writer(file, lineterminator='\n')
        csv_file.writerow(['city', 'date', 'hour', 'temperature_c', 'pressure_mm', 'is_rainy'])
        for row in transform_data():
            csv_file.writerow([row['city'], row['date'], row['hour'], row['temperature_c'],
                               row['pressure_mm'], row['is_rainy']])


if __name__ == '__main__':
    main()








