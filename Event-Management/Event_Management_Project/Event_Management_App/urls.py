from django.urls import path, include
from . import views

urlpatterns=[

    path('events/', views.EventListView.as_view(), name='Events'),
    path('perdorues/signup/', views.PerdoruesSignUpView.as_view(), name='Perdorues Sign Up'),
    path('event/create/', views.EventCreatedByManager.as_view(), name='Event Form'),
    path('event/<int:pk>/', views.ManagerCheckPerdoruesRegistered.as_view(), name='Event Check'),
    path('perdorues/joins/event', views.PerdoruesJoinsEventsView.as_view(), name='Event Check'),
    path('perdorues/login/', views.LogInPerdoruesView.as_view(), name='Perdorues Log In'),
    path('perdorues/update/<int:pk>', views.PerdoruesUpdater.as_view(), name='Perdorues Update'),

]
