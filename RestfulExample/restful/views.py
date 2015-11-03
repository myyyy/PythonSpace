# coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from restful.models import Teacher
from restful.serializers import TeacherSerializers


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def teacher_list(request, num):

    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        teacher = Teacher.objects.get(name=num)
        ser = TeacherSerializers(teacher)
        return JSONResponse(ser.data)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TeacherSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

