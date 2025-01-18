from django.contrib import messages
from django.shortcuts import render, redirect
from localvid.videoplayer.forms import VideoForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Video
import os

# Create your views here.


def index(request):

    context = {
        "user": request.user,
    }

    return render(request, "videos/home.html", context)

def video_list(request):
    videos = Video.objects.all()
    context = {"videos": videos}

    return render(request, 'videos/video_list.html', context)


def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('index_list')
    else:
        form = VideoForm()

    return render(request, 'videos/video_upload.html', {'form': form})


def video_stream(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video_path = video.video_file.path


    file = open(video_path, 'rb')
    file_size = os.path.getsize(video_path)

    if 'Range' in request.headers:
        byte_range = request.headers['Range']
        start_byte, end_byte = parse_range(byte_range, file_size)
        file.seek(start_byte)
        chunk = file.read(end_byte - start_byte + 1)

        content_range = f"bytes {start_byte}-{end_byte}/{file_size}"
        response = HttpResponse(chunk, status=206, content_type='video/mp4')
        response['Content-Range'] = content_range
        response['Content-Length'] = len(chunk)
    else:
        chunk = file.read(1024 * 1024)
        response = HttpResponse(chunk, content_type='video/mp4')
        response['Content-Length'] = file_size

    file.close()

    return response

def parse_range(byte_range, file_size):

    byte_range = byte_range.strip().split('=')[1]  # Get the part after '='
    byte_range = byte_range.split('-')  # Split into start and end byte
    start_byte = int(byte_range[0])
    end_byte = int(byte_range[1]) if byte_range[1] else file_size - 1

    if start_byte >= file_size:
        start_byte = file_size - 1
    if end_byte >= file_size:
        end_byte = file_size - 1

    return start_byte, end_byte
