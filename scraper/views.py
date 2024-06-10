from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapingJob, ScrapingTask
from .serializers import ScrapingJobSerializer
from .tasks import scrape_coin_data
from crypto_scraper.celery import app



class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        
        if not all(isinstance(coin, str) for coin in coins):
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        job = ScrapingJob.objects.create()
        app.control.purge()
        resp = {}
        for coin in coins:
            task = ScrapingTask.objects.create(job=job, coin=coin)
            resp[coin] = scrape_coin_data(task.id)
    
        
        
        return Response(resp, status=status.HTTP_201_CREATED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapingJob.objects.get(job_id=job_id)
        except ScrapingJob.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
