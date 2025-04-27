from django.urls import path

from . import views
urlpatterns =[
    path('',views.LoginView.as_view(),name='login'),

    path('logout/',views.LoginView.as_view(),name='logout'),

    path('forgot-password/',views.ForgotPasswordView.as_view(),name='forgot-password'),

    path('otp/',views.OTPView.as_view(),name='otp'),

    path('change-password/',views.ChangePasswordView.as_view(),name='change-password'),

    path('home/',views.HomeView.as_view(),name='home'),

    path('add-folder/',views.AddFolderView.as_view(),name='add-folder'),

    path('unlock-folder/<str:uuid>/',views.UnlockingView.as_view(),name='unlock-folder'),

    path('lock-folder/<str:uuid>/',views.LockView.as_view(),name='lock-folder'),

    path('delete-folder/<str:uuid>/',views.DeleteView.as_view(),name='delete-folder'),

    path('folder-with-files/<str:uuid>/',views.FolderFilesView.as_view(),name='folder-with-files'),

    path('download-folder/<str:uuid>/',views.DownloadFolderView.as_view(),name='download-folder'),

    path('register/',views.RegisterView.as_view(),name='register'),

    path('reports/',views.ReportsListView.as_view(),name='reports'),

]