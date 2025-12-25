import requests
import json
import datetime
import random
import re

# URL Sumber Proxy (Contoh pakai Proxyscrape yang free)
URL_SUMBER = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

def get_country_simulation(ip):
    # Karena API GeoIP gratis biasanya berbayar/terbatas,
    # Kita simulasi random negara dari list populer untuk demo.
    # Kalau mau akurat, nanti integrasikan dengan library 'geoip2'
    return random.choice(["US", "ID", "SG", "DE", "FR", "BR", "CN", "RU"])

def update_proxy():
    print("⏳ Sedang mengambil proxy...")
    
    try:
        response = requests.get(URL_SUMBER, timeout=15)
        if response.status_code != 200:
            print("❌ Gagal mengambil data dari URL Sumber.")
            return

        lines = response.text.splitlines()
        proxy_list = []
        
        for line in lines:
            # Pastikan formatnya IP:PORT
            if ":" in line and not line.startswith("#"):
                parts = line.strip().split(":")
                if len(parts) >= 2:
                    ip = parts[0]
                    port = parts[1]
                    
                    # Buat data objek
                    proxy_data = {
                        "ip": ip,
                        "port": port,
                        "user": "-",        # Proxy public jarang ada user/pass
                        "password": "-",
                        "country": get_country_simulation(ip),
                        "type": "HTTP",
                        "status": "Active"
                    }
                    proxy_list.append(proxy_data)

        # Siapkan JSON Final
        final_data = {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "total": len(proxy_list),
            "proxies": proxy_list
        }

        # Simpan ke file 'proxy.json'
        with open("proxy.json", "w") as f:
            json.dump(final_data, f, indent=2)
            
        print(f"✅ Sukses! {len(proxy_list)} proxy tersimpan di proxy.json")

    except Exception as e:
        print(f"❌ Error script: {e}")

if __name__ == "__main__":
    update_proxy()
