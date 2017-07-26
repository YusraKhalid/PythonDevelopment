from django.conf.urls import url

from . import views

app_name = "training"
urlpatterns = [
    url(r'^trainee/(?P<trainee_id>[0-9]+)/$',
        views.TraineeDetails.as_view(), name="trainee_details"),
    url(r'^trainer/(?P<trainer_id>[0-9]+)/$',
        views.TrainerDetails.as_view(), name="trainer_details"),
    url(r'^assignment/(?P<assignment_id>[0-9]+)/$',
        views.AssignmentDetails.as_view(), name="assignment_details"),
    url(r'^technology/(?P<technology_id>[0-9]+)/$',
        views.TechnologyDetails.as_view(), name="technology_details"),
    url(r'^validate_username/$', views.ValidateUserName.as_view(),
        name="validate_username"),
    url(r'^search/$', views.Search.as_view(), name="search"),
    url(r'^update_image/$', views.UpdateImage.as_view(), name="update_image"),
    url(r'^trainer_signup/$',
        views.TrainerSignUp.as_view(), name="trainer_signup"),
    url(r'^trainee_signup/$',
        views.TraineeSignUp.as_view(), name="trainee_signup"),
    url(r'^profile/$', views.Profile.as_view(), name="profile"),
    url(r'^logout/$', views.Logout.as_view(), name="logout"),
    url(r'^login/$|^$', views.Login.as_view(), name="login"),
]
