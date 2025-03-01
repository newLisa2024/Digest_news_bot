import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
from modules.digest import send_weekly_digest  # NEW

def start_scheduler(bot):  # UPDATED
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            send_weekly_digest,
            trigger="cron",
            day_of_week=config.SCHEDULE_DAY_OF_WEEK,
            hour=config.SCHEDULE_HOUR,
            minute=config.SCHEDULE_MINUTE,
            args=[bot]  # NEW
        )
        scheduler.start()
        logging.info("✅ Планировщик запущен. Рассылка настроена.")
    except Exception as e:
        logging.error(f"❌ Ошибка запуска планировщика: {e}")