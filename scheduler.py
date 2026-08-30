import os

from apscheduler.schedulers.blocking import BlockingScheduler

from checker import check_all_products


def run_price_check():
    print("\n🔄 Starting scheduled price check...")

    receiver_email = os.getenv(
        "PRICE_TRACKER_RECEIVER_EMAIL"
    )

    if not receiver_email:
        print(
            "❌ PRICE_TRACKER_RECEIVER_EMAIL "
            "is not configured."
        )
        return

    check_all_products(
        receiver_email
    )


scheduler = BlockingScheduler()


scheduler.add_job(
    run_price_check,
    "interval",
    hours=1
)


print("================================")
print("   PRICE TRACKER SCHEDULER")
print("================================")
print()
print("✅ Scheduler started.")
print("🔄 Prices will be checked every hour.")
print("Press Ctrl+C to stop.")
print()


try:
    scheduler.start()

except KeyboardInterrupt:

    print("\n🛑 Scheduler stopped.")