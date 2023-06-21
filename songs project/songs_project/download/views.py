import http
from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube
from wsgiref.util import FileWrapper
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
import base64
import json
from json import dumps

# Create your views here.


#
@csrf_exempt
def download_song(request):
    if request.method == "POST":
        body = json.loads(request.body)
        link = body["link"]
        yt = YouTube(link)
        # yt.streams.filter(only_audio=True)
        # stream = yt.streams.get_by_itag(22)

        audio = yt.streams.get_audio_only()
        audio.download()
        # return HttpResponse("Success")

        # now we have the path to the downloaded file
        path = Path(audio.default_filename)

        with open(path, "rb") as downloaded_file:
            text = base64.b64encode(downloaded_file.read())
            base64_string = text.decode("utf-8")
            raw_data = {"base": base64_string}
            json_data = dumps(raw_data, indent=2)

        return HttpResponse(json_data)

        # file = FileWrapper(open(path, 'rb'))
        # response = HttpResponse(file, content_type='audio/mp4')
        # response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
        # return response
