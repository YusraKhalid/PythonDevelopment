from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from todo import views

router = routers.DefaultRouter()
router.register(r'todo', views.TodoViewSet)
router.register(r'users', views.UserViewSet)

app_name = 'todo'

urlpatterns = [
    url(r'^$', views.TodoView.as_view(), name='index'),
    url(r'^api/users/create', views.UserAndTodoCreateView.as_view(), name='create_user_todo'),
    url(r'^api/users/createalone', views.UserCreateView.as_view(), name='create_user'),
    url(r'^api/', include(router.urls)),
    url(r'add_item/$', views.TodoCreateView.as_view(), name='add_item'),
    url(r'summary/$', views.SummaryView.as_view(), name='summary'),
    url(r'(?P<pk>[0-9]+)/detail/$', views.TodoDetailView.as_view(), name='detail'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.TodoDeleteView.as_view(), name='delete'),
    url(r'(?P<pk>[0-9]+)/update/$', views.TodoUpdateView.as_view(), name='update'),
]
