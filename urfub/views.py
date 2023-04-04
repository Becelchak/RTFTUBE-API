import random
import json
import sqlite3

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import videos
from django import forms

conn_db = sqlite3.connect('db.sqlite3', uri=True, check_same_thread=False)
cur = conn_db.cursor()

# Вывод главной страницы
def main(request):
    vid = videos.objects.all()
    return render(request, 'main/video-main.html', context={'video' : vid})


def findVideo(request):
    return render(request, 'main/video-find.html')

def getVideo(request, id = 0):
    if request.method == "GET":
        count_id = cur.execute("SELECT COUNT(*) FROM urfub_videos WHERE id > 0").fetchone()[0]
        if id > count_id:
            return HttpResponseNotFound("нету")
        if id == 0:
            vid_id = random.randint(1,count_id)
            vid = videos.objects.get(id=vid_id)
        else:
            vid = videos.objects.get(id=id)
        return render(request, "main/video.html", context={'video' : vid})



def getLikes(request, id = 0):
    response = HttpResponse
    if id == 0:
        return HttpResponse(random.choice(1))
    for video in all_video:
        if (video["id"] == id):
            return response(json.dumps(video["likeCount"], ensure_ascii=False), content_type="application/json")
    return HttpResponse("Неправильный ID")

def getComments(request,id = 0):
    response = HttpResponse
    if id == 0:
        return HttpResponse(random.choice(all_video))
    for video in all_video:
        if (video["id"] == id):
            return response(json.dumps(video["comments"] , ensure_ascii=False), content_type="application/json")
    return HttpResponse("Неправильный ID")

@csrf_exempt
def postVideo(request):
    if request.method == "GET":
        return render(request, 'main/video-upload.html')
    if request.method == "POST" :
        for video in all_video:
            if video["id"] == request.POST["id"]:
                return HttpResponse("Данное видео уже загружено")
        newVideo = {
            "id" : int(request.POST["id"]),
            "name" : request.POST["name"],
            "likeCount" : int(request.POST["likeCount"]),
            "dislikeCount": int(request.POST["dislikeCount"]),
            "comments": None
        }
        all_video.append(newVideo)
        return HttpResponse("{0} успешно загружено".format(request.POST["name"]), content_type="application/json")