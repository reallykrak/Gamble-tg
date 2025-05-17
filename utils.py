# utils.py
import json

# Veriyi dosyadan okur
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Veriyi dosyaya yazar
def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Kullanıcı daha önce kayıtlı değilse kayıt eder (bonus başlangıç coin, banka, istatistikler)
def register_user(user_id):
    data = load_data()
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "coin": 1000,
            "bank": 0,
            "joined": False,
            "stats": {"wins": 0, "losses": 0}
        }
        save_data(data)
