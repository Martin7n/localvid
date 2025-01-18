from django.urls import path

from localvid.videoplayer.views import video_list, video_upload, index, video_stream

urlpatterns = [
    path('', index, name='home'),
    path("list/", video_list, name="index_list"),
    path("add/", video_upload, name="video_upload"),
    path('<int:pk>/', video_stream, name='video_stream'),
    #(    path('admin/', admin.site.urls),
]