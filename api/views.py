# django and rest imports
from django.shortcuts import render
from django.core import mail
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

# python module imports
import threading
from datetime import datetime
from decouple import config
import logging, os

# local imports
from .serializer import Subscribe_model

# sender value
sender = settings.EMAIL_HOST_USER

# make logs of the current threads
logging.basicConfig(filename=f'logs.log', filemode='a+',
                    encoding="utf-8", level=logging.INFO)

logger_lock = threading.Lock()

class Email_Thread(threading.Thread):
    def __init__(self, email_to):
        self.email_to = email_to
        threading.Thread.__init__(self)

    def run(self):
        logger = logging.getLogger(__name__)
        try:
            with mail.get_connection() as connection:
                email_msg = mail.EmailMessage(subject="Email to Subscribers", 
                body="Congrats, This is to the mail",
                from_email= sender, 
                to= [self.email_to], 
                connection=connection
                )
                email_msg.send(fail_silently=False)
            print("Email was sent")
            with logger_lock:
                logger.info(f"Email was Successfully sent to {self.email_to} by {threading.current_thread(), threading.Thread.name} at {datetime.now()}")
        except Exception as e:
            print("Failed due to exception", e)
            with logger_lock:
                logger.warning(f"Some error was there while sending mail to {self.email_to} by {threading.current_thread(), threading.Thread.name} at {datetime.now()}, reason={e}")

class Email_View(APIView):
    def get(self,request, *args, **kwargs):
        data = self.request.query_params
        subs = []
        for l in Subscribe_model.objects.all().values_list():
            subs.append(l[1])
        print(subs)

        try:
            threads = data['threads']
            print(threads)
            try:
                int(threads)
            except:
                return Response({"Message": f"Please pass 'threads' value as integer, current value is {threads} is str." },400)
        except:
            threads = os.cpu_count()*5

        threads = int(threads)

        def main(start,end):
            for i in range(start,end):
                Email_Thread(subs[i]).start()

        def start_threads():
            values = {'s1':0, 'e1':0}
            length_of_list = len(subs)
            absolute_value = int(length_of_list / threads)
            remainder_value = length_of_list % threads

            for i in range(1, threads + 1):
                if remainder_value == 0:
                    if i == 1:
                        values[f'e1'] = values["e1"] + absolute_value
                    if i > 1: 
                        values[f"s{i}"] = values[f"e{i-1}"]
                        values[f'e{i}'] =  values[f"e{i-1}"] + absolute_value
                if i == 1 and i <= remainder_value :
                    values["s1"] = 0
                    values["e1"] = values["e1"] + absolute_value + 1
                if i != 1 and i <= remainder_value:
                    values[f"s{i}"] = values[f"e{i-1}"]
                    values[f"e{i}"] = values[f"e{i-1}"] + (absolute_value + 1)
                if i != 1 and i > remainder_value:
                    values[f"s{i}"] = values[f"e{i-1}"]
                    values[f"e{i}"] = values[f"e{i-1}"] + absolute_value

                x = threading.Thread(target=main, args=[values[f's{i}'],values[f'e{i}']], name=f"th{i}", daemon=True)
                print(f"th{i} started")
                x.start()

        start_threads()
        return Response({'Message':'Done'}, 200)

def Subscriber_View(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']

        data = Subscribe_model(name=name, email=email)
        data.save()
 
        return render(request, 'home.html', {'string':'Subscribed !!!'})
    return render(request, 'home.html')
