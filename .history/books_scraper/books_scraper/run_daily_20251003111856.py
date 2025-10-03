import schedule
import time
import subprocess

def run_spider():
    print("⏳ Lancement du spider...")
    # Remplace "books" par le nom de ton spider
    subprocess.run(["scrapy", "crawl", "books"])
    print("✅ Spider terminé.")

# Planifie une exécution chaque jour à 02h00
schedule.every().day.at("02:00").do(run_spider)

print("🚀 Scheduler démarré (le spider sera lancé chaque jour à 02h00)")
while True:
    schedule.run_pending()
    time.sleep(60)  # Vérifie toutes les minutes 
