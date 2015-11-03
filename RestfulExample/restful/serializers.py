# coding=utf-8

from restful.models import Teacher
from rest_framework import serializers


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        file = ('name', 'email', 'password')

    # name = serializers.CharField(max_length=100)
    # email = serializers.EmailField(max_length=50)
    # password = serializers.CharField(max_length=50)

    def restore_object(self, attributes, instance=None):
        if instance:
            instance.name = attributes['name']
            instance.email = attributes['email']
            instance.password = attributes['password']

            return instance

        return Teacher(**attributes)
