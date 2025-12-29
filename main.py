import requests
import json
import datetime

# Menggunakan API Geonode karena menyediakan metadata lengkap (Country, Port, Protocol)
# Limit 500 proxy, diurutkan berdasarkan waktu pengecekan terakhir (terbaru)
API_URL = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"

def update_proxy():
    print("⏳ Mengambil data proxy XIX dari Geonode...")
    
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status() # Cek jika ada error koneksi
        
        data = response.json()
        raw_list = data.get("data", [])
        
        proxy_list = []
        
        for item in raw_list:
            # Ambil data real dari API
            ip = item.get("ip")
            port = item.get("port")
            country = item.get("country") # Kode negara asli (ID, US, SG, dll)
            protocols = item.get("protocols", [])
            protocol_str = protocols[0] if protocols else "http"
            
            # Format objek untuk JSON
            proxy_data = {
                "ip": ip,
                "port": str(port),  # Konversi ke string agar konsisten
                "country": country,
                "protocol": protocol_str, # Menambahkan info protokol (HTTP/SOCKS)
                "source": "XIX-Fetcher"
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
            
        print(f"✅ Sukses! {len(proxy_list)} proxy tersimpan.")
        print("   -> Data negara dan port sekarang REAL (Bukan simulasi).")

    except Exception as e:
        print(f"❌ Error script: {e}")

if __name__ == "__main__":
    update_proxy()
