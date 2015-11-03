from django.conf.urls import *
from biger.views import archive


from django.conf.urls import *
from models import *
from views import *

urlpatterns = patterns('',
	url(r'^$',archive),
)
