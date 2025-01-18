from django import forms

from localvid.videoplayer.models import Video



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "video_file"]
