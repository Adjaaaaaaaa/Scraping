import schedule
import time
import subprocess
"""
Scheduler script to run the Scrapy spider daily at a specific time.

- Uses the `schedule` library to schedule the spider execution.
- Uses `subprocess` to run the spider as an external process.
"""


def run_spider():
    """
    Run the 'books' spider using Scrapy.

    This function calls `scrapy crawl books` and prints status messages.
    """
    print("⏳ Lancement du spider...")
    # Replace "books" with the spider name if different
    subprocess.run(["scrapy", "crawl", "books"])
    print("✅ Spider terminé.")


# Schedule the spider to run every day at 02:00 AM
schedule.every().day.at("02:00").do(run_spider)

print("🚀 Scheduler démarré (le spider sera lancé chaque jour à 02h00)")
# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)  # Vérifie toutes les minutes s’il est l’heure de lancer le spider.
