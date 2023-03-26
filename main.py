from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.service import DataService

scheduler = BlockingScheduler()
@scheduler.scheduled_job(IntervalTrigger(hours=1))
def main():
    servicio = DataService()
    servicio.dataextraction()
    servicio.dataprocess()
    servicio.datawriter()

scheduler.start()