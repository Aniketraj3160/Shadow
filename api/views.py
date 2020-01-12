# Create your views here.
from django.shortcuts import render
import requests
from .serializers import PostSerializer, CameraSerializer, AuthoritySerializer, JournalistSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from blog.models import Post, registerCamera, City
from users.models import *
from django.utils import timezone
from datetime import datetime as dt
from datetime import date


# def api(request):
#     response = requests.get('http://127.0.0.1:8000/api')
#     apidata = response.json()
#     out = []
#     for i in apidata:
#         for j in i:
#             out.append(i[j])
#     a = len(out)
#     k = a/5
#     list1 = []
#     list2 = []
#     list3 = []
#     list4 = []
#     list5 = []
#     list6 = []
#     for h in range(0, int(a), 6):
#         data = {'title': out[h],
#                 }
#         list1.append(data)

#     for h in range(1, int(a), 6):
#         data = {
#             'location': out[h],
#         }
#         list2.append(data)
#     for h in range(2, int(a), 6):
#         data = {
#             'content': out[h],
#         }
#         list3.append(data)
#     for h in range(3, int(a), 6):
#         data = {
#             'crimetype': out[h],
#         }
#         list4.append(data)
#     for h in range(4, int(a), 6):
#         data = {
#             'state': out[h],
#         }
#         list5.append(data)
#     for h in range(5, int(a), 6):
#         data = {
#             'city': out[h],
#         }
#         list6.append(data)

#         data = {'title': list1, 'location': list2, 'content': list3,
#                 'crimetype': list4, 'state': list5, 'city': list6}
#         data1 = {'rest': zip(list2, list4, list5, list6)}
#     return render(request, 'api.html', data1)


Authority_choices = ['Department of Consumer Affairs', 'Department of Food and Public Distribution', 'Serious Fraud Investigation Office', 'Forest Reserve Conservation Authority',
                     'Criminal Investigation Department', 'Labour Bureau', 'National Commission for Minorities', 'National Commission for Women', 'Income Tax Department']


def convert_dict(Obj):
    Authority_dict = {'Department of Consumer Affairs': 0, 'Department of Food and Public Distribution': 0,
                      'Serious Fraud Investigation Office': 0, 'Forest Reserve Conservation Authority': 0, 'Criminal Investigation Department': 0, 'Labour Bureau': 0, 'National Commission for Minorities': 0, 'National Commission for Women': 0, 'Income Tax Department': 0}

    listdict = []
    for object1 in Obj:
        dic = {"id": object1.id, "title": object1.title, "location": object1.location, "pincode": object1.pincode,
               "city": object1.city.name, "state": object1.state.name, "content": object1.content}
        listdict.append(dic)
        tags = object1.authority
        tags = tags.split(",")
        # Checking if the post is less than a year old
        date1 = object1.date_posted.strftime("%m/%d/%Y")
        date2 = dt.now().strftime("%m/%d/%Y")
        date1 = date1.split("/")
        date2 = date2.split("/")
        d0 = date(int(date1[2]), int(date1[0]), int(date1[1]))
        d1 = date(int(date2[2]), int(date2[0]), int(date2[1]))
        delta = d1 - d0
        if delta.days < 365:
            for authority in Authority_choices:
                if authority in tags:
                    Authority_dict[authority] += 1
    final_dict = {"posting": listdict, "statistics": Authority_dict}
    return(final_dict)


class post_list(APIView):
      #    queryset = Post.objects.all()
     #    serializer_class = PostSerializer

    def get(self, request, city):

        city1 = City.objects.get(name=city)
        # print(city1)
        queryset = Post.objects.filter(city=city1)
        finaldict = convert_dict(queryset)
        #serializer = PostSerializer(queryset, many=True)
        return Response(finaldict)


class camera_list(APIView):
    #     queryset = registerCamera.objects.all()
    #     serializer_class = CameraSerializer

    def get(self, request, city):
        city1 = City.objects.get(name=city)
        print(city1)
        queryset = registerCamera.objects.filter(city=city1)
        serializer = CameraSerializer(queryset, many=True)
        return Response(serializer.data)


class post_list1(APIView):
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer
    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class camera_list1(APIView):
    # queryset = registerCamera.objects.all()
    # serializer_class = CameraSerializer
    def get(self, request):
        queryset = registerCamera.objects.all()
        serializer = CameraSerializer(queryset, many=True)
        return Response(serializer.data)


class authority_list(APIView):
    # queryset = Authority.objects.all()
    # serializer_class = AuthoritySerializer
    def get(self, request):
        queryset = Authority.objects.all()
        serializer = AuthoritySerializer(queryset, many=True)
        return Response(serializer.data)


class journalist_list(APIView):
    # queryset = Journalist.objects.all()
    # serializer_class = JournalistSerializer
    def get(self, request):
        queryset = Journalist.objects.all()
        serializer = JournalistSerializer(queryset, many=True)
        return Response(serializer.data)
