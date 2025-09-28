import requests
import pyttsx3
import tkinter as tk
import time
from threading import Thread
#  API anahtarları 
weather_api_key = "senin_key"
tomtom_api_key = "senin_key"
# Kadıköy ve Beşiktaş koordinatları (lat,lon) 
origin_coords = "40.9870,29.0257"    # Kadıköy
destination_coords = "41.0436,29.0031" # Beşiktaş
# Tkinter arayüz 
root = tk.Tk()
root.title("İstanbul Hava & Trafik Asistanı")
root.geometry("620x400")
label = tk.Label(root, text="Yükleniyor...", font=("Arial", 13), justify="left")
label.pack(padx=12, pady=12)
# Ses motoru 
engine = pyttsx3.init()
# Öneri fonksiyonu
def öneri(weather, traffic):
    messages = []
    w = str(weather).lower()
    if w in ["rain", "drizzle"]:
        messages.append( "Yağmur yağıyor, yol kaygan. Lütfen hızını azalt ve farlarını aç!")
    elif w == "snow":
        messages.append( "Kar ve buzlu yol var. Hızını düşür ve lastiklerini kontrol et!")
    elif w == "fog":
        messages.append("Sisli yol, görüş mesafesi düşük. Farlarını aç ve dikkatli sür. Trafik normal!")
    else:
        messages.append("Hava normal.")

    if traffic is None or traffic < 0:
        messages.append("Trafik bilgisi alınamadı.")
    else:
        if traffic >= 70:
            messages.append(f"İstanbul trafiği çok yoğun %{traffic}, dikkatli sür!")
        elif traffic >= 40:
            messages.append(f"İstanbul trafiği orta yoğun %{traffic}.")
        else:
            messages.append(f"İstanbul trafiği akıcı %{traffic}.")

    return " ".join(messages)
# TomTom Route Flow API ile rota bazlı trafik yüzdesi
def get_route_traffic(origin, destination):
    try:
        # TomTom Route API (flow segment data ile)
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json"
        params = {
            "key": tomtom_api_key,
            "routeType": "fastest",
            "traffic": "true",
            "travelMode": "car",
        }
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            print("TomTom HTTP Hata:", resp.status_code)
            return -1
        data = resp.json()
        routes = data.get("routes", [])
        if not routes:
            return -1
        # Rota boyunca segmentler
        segments = routes[0].get("legs", [])[0].get("points", [])
        # Eğer segment bilgisi yoksa summary fallback
        summary = routes[0].get("summary", {})
        travel_time = summary.get("travelTimeInSeconds", None)
        traffic_delay = summary.get("trafficDelayInSeconds", None)
        if travel_time is None or traffic_delay is None:
            # fallback
            travel_time = 0
            traffic_delay = 0
            legs = routes[0].get("legs", [])
            for leg in legs:
                s = leg.get("summary", {})
                travel_time += s.get("travelTimeInSeconds", 0)
                traffic_delay += s.get("trafficDelayInSeconds", 0)
        if travel_time == 0:
            return -1
        traffic_percent = int((traffic_delay / travel_time) * 100)
        if traffic_percent < 0:
            traffic_percent = 0
        elif traffic_percent > 100:
            traffic_percent = 100
        return traffic_percent
    except Exception as e:
        print("TomTom API Hatası:", e)
        return -1
# Güncelleme döngüsü
def update_loop():
    while True:
        try:
            # Hava durumu İstanbul
            city = "Istanbul"
            weather_resp = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=tr",
                timeout=10
            )
            if weather_resp.status_code == 200:
                weather_data = weather_resp.json()
                weather = weather_data.get("weather", [{}])[0].get("main", "Bilinmiyor")
                temp = weather_data.get("main", {}).get("temp", "Bilinmiyor")
                humidity = weather_data.get("main", {}).get("humidity", "Bilinmiyor")
            else:
                weather, temp, humidity = "Bilinmiyor", "Bilinmiyor", "Bilinmiyor"
              
            # Trafik yüzdesi
            traffic_percent = get_route_traffic(origin_coords, destination_coords)
            display_traffic = traffic_percent if traffic_percent >= 0 else None
            # Mesaj oluştur
            msg = öneri(weather, display_traffic if display_traffic is not None else -1)
            traffic_text = f"%{display_traffic}" if display_traffic is not None else "Bilinmiyor"
            label_text = (
                f"Hava (İstanbul): {weather}\n"
                f"Sıcaklık: {temp}°C\n"
                f"Nem: {humidity}%\n\n"
                f"Kadıköy → Beşiktaş Trafik Yoğunluğu: {traffic_text}\n\n"
                f"Öneri: {msg}"
            )
            label.config(text=label_text)
            # Sesli uyarı
            engine.say(msg)
            engine.runAndWait()
        except Exception as e:
            print("Genel Hata:", e)
        time.sleep(600)  # 10 dakika bekle
# Thread ile çalıştır 
thread = Thread(target=update_loop, daemon=True)
thread.start()
root.mainloop()
