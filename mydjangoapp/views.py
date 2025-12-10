
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as s
import time 
from mydjangoapp.generic_query import *
from .models import *
from django.shortcuts import get_object_or_404
from django.core.cache import cache
import redis 
import json
from loguru import logger




# Create your views here.
class FormResponse(APIView):
    def post(self,request, *args, **kwargs):
        data=request.data

        obj = form.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email_id=data.get("email_id"),
            phone_no=data.get("phone_no"),
            message=data.get("message"),
        )

        return Response(
            {
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "email_id": obj.email_id,
                "phone_no": obj.phone_no,
                "message": obj.message
            },
            status=s.HTTP_201_CREATED,
        )
class FormListView(APIView):
    def get(self,request, *args, **kwargs):
        cache_key="forms_list"
        data=cache.get(cache_key)
        if data is not None:
            return Response(data, status=s.HTTP_200_OK)
        
        q=form.objects.all()
        data=[]


        for obj in q:
            data.append({
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "email_id": obj.email_id,
                "phone_no": obj.phone_no,
                "message": obj.message,
            })
        time.sleep(2)
        cache.set(cache_key, data, timeout=300)
        return Response(data, status=s.HTTP_200_OK)
        
    
class FormUpdateView(APIView):   
    def put(self,request, pk, *args, **kwargs):
        obj = get_object_or_404(form, pk=pk)
        data = request.data

        obj.first_name = data.get("first_name", obj.first_name)
        obj.last_name  = data.get("last_name", obj.last_name)
        obj.email_id   = data.get("email_id", obj.email_id)
        obj.phone_no   = data.get("phone_no", obj.phone_no)
        obj.message    = data.get("message", obj.message)
        obj.save()

        return Response(
            {
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "email_id": obj.email_id,
                "phone_no": obj.phone_no,
                "message": obj.message,
            },
            status=s.HTTP_200_OK,
        )
    
    def patch(self,request, pk, *args, **kwargs):
        obj = get_object_or_404(form, pk=pk)
        data = request.data

        if "first_name" in data:
            obj.first_name = data["first_name"]
        if "last_name" in data:
            obj.last_name = data["last_name"]
        if "email_id" in data:
            obj.email_id = data["email_id"]
        if "phone_no" in data:
            obj.phone_no = data["phone_no"]
        if "message" in data:
            obj.message = data["message"]

        obj.save()

        return Response(
            {
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "email_id": obj.email_id,
                "phone_no": obj.phone_no,
                "message": obj.message,
            },
            status=s.HTTP_200_OK,
        )

class FormDeleteView(APIView):
    def delete(self,request, pk, *args, **kwargs):
            obj = get_object_or_404(form, pk=pk)
            obj.delete()
            return Response(status=s.HTTP_204_NO_CONTENT)


class McqResponse(APIView):
    def get(self,request,*args, **kwargs):
        r = redis.Redis(host="localhost", port=6379, db=0)
        userId = request.data.get('userId')
        className = request.data.get('className')
        date=str(request.data.get('date'))
        subjectName = request.data.get('subjectName')
        size=int(request.data.get('size'))
        current_page=int(request.data.get('current_page'))


        #logger.critical("params are userId==>"+str(userId))
        logger.critical(f"params are userId==>{userId}-className-{className}-date-{date}-subjectName-{subjectName}-size-{size}-currentpage-{current_page}")
        
        
        redis_key=f"MCQ_RESPONSE:{userId}"
        cached_data=r.get(redis_key)
        logger.critical(f"params are==>{cached_data}")
        if cached_data is not None:
            print("==cacheddata==")
            result_str=json.loads(cached_data)
            r.get(redis_key)
        else:
            print("==calldb=")

            result = evaluate_mcq_submission(
                classes=className,
                date=date,
                subjects=subjectName,
                userId=userId,
                size=size,
                current_page=current_page,
            )
            
            result_str = str(result)
            r.setex(redis_key,300,json.dumps(result_str))
        return Response(result_str)

class McqResponseUpdate(APIView):
    def put(self,request,*args,**kwargs):
        r = redis.Redis(host="localhost", port=6379, db=0)
        data = request.data
        _id=data["_id"]
        userId=data["userId"]
    
        correctAnswer=int(data["correctAnswer"])
        print("id==>", _id)
        print("correctanswer==>", correctAnswer)
        redis_key=f"MCQ_RESPONSE:{userId}"
        cacheddata=r.get(redis_key)
        logger.critical(f"params are==>{cacheddata}")
        if cacheddata:
            print("==cache==")
            response_dict=json.loads(cacheddata)
            r.get(redis_key)

        else:
            print("==db==")
            message,status=update_mcq_data(correctAnswer,_id,userId)
            response_dict={
                "message":message,
                "status":status
            }
           
            r.set(redis_key,json.dumps(response_dict))
        return Response(response_dict)
