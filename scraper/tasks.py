from celery import shared_task
from .coinmarketcap import CoinMarketCap
from .models import ScrapingTask
import json

@shared_task
def scrape_coin_data(task_id):
    task = ScrapingTask.objects.get(id=task_id)
    data = CoinMarketCap.fetch_coin_data(task.coin)

    if data:
        task.status = 'completed'
        task.result = json.dumps(data)
        task.save()
        return data
    else:
        task.status = 'failed'
    task.save()
