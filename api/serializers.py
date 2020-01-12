from rest_framework import serializers
from blog.models import Post, registerCamera, City
from users.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response


# class PostSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Post
#         fields = ('title', 'location', 'pincode', 'city',
#                   'state', 'country', 'content', 'crimetype', 'photo1', 'photo2', 'photo3', 'photo4'
#                   )

#     def update(self, instance, validated_data):

#         instance.title = validated_data.get('title', instance.title)
#         instance.location = validated_data.get('location', instance.location)
#         instance.pincode = validated_data.get('pincode', instance.pincode)
#         instance.city = validated_data.get('city', instance.city)
#         instance.state = validated_data.get('state', instance.state)
#         instance.country = validated_data.get('country', instance.country)
#         instance.content = validated_data.get('content', instance.content)
#         instance.crimetype = validated_data.get(
#             'crimetype', instance.crimetype)
#         instance.photo1 = validated_data.get('photo1', instance.photo1)
#         instance.photo2 = validated_data.get('photo2', instance.photo2)
#         instance.photo3 = validated_data.get('photo3', instance.photo3)
#         instance.photo4 = validated_data.get('photo4', instance.photo4)
#         instance.save()

#         return instance


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'location', 'pincode', 'city',
                  'state', 'country', 'content',  'photo1', 'photo2', 'photo3', 'photo4'
                  )

    # def update(self, instance, validated_data):

    #     instance.title = validated_data.get('title', instance.title)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.pincode = validated_data.get('pincode', instance.pincode)
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.country = validated_data.get('country', instance.country)
    #     instance.content = validated_data.get('content', instance.content)
    #     # instance.crimetype = validated_data.get(
    #     #     'crimetype', instance.crimetype)
    #     instance.photo1 = validated_data.get('photo1', instance.photo1)
    #     instance.photo2 = validated_data.get('photo2', instance.photo2)
    #     instance.photo3 = validated_data.get('photo3', instance.photo3)
    #     instance.photo4 = validated_data.get('photo4', instance.photo4)
    #     instance.save()

    #     return instance


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = registerCamera
        fields = ('id', 'address', 'pincode', 'state', 'city'
                  )


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = ("user", "id",  "Email_id", "Dept_id", "Dept_name"
                  )

class JournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journalist
        fields = ("user", "id",  "Email_id", "Dept_id", "Dept_name"
                  )
