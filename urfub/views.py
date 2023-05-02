# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
from typing import IO, Generator

MAX_UPLOAD_SIZE = 104857600

import random
import json
import sqlite3

from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import videos
from pathlib import Path
from django.urls import reverse

conn_db = sqlite3.connect('db.sqlite3', uri=True, check_same_thread=False)
cur = conn_db.cursor()

# Вывод главной страницы
def main(request):
    vid = videos.objects.reverse()[0:2]
    authors = {}
    for video in vid:
        authors[video.id] = cur.execute("SELECT username FROM auth_user WHERE id == {0}".format(video.author_id)).fetchone()[0]
        return render(request, 'main/video-main.html', context={'video' : vid, 'authors' : authors})


def findVideo(request):
    return render(request, 'main/video-find.html')

def ranged(
        file: IO[bytes],
        start:int = 0,
        end:int = None,
        blockSize:int = 8192,
) -> Generator[bytes,None,None]:
    consumed = 0

    file.seek(start)
    while True:
        dataLenght = min(blockSize, end - start - consumed) if end else blockSize
        if dataLenght <= 0:
            break
        data = file.read(dataLenght)
        if not data:
            break
        consumed += dataLenght
        yield data

    if hasattr(file,'close'):
        file.close()

def getStreamVideo(request,id:int):
    vid = videos.objects.get(id=id)
    path = Path(vid.stream.path)
    file = path.open('rb')

    fileSize = path.stat().st_size
    statusCode = 200
    contentLenght = fileSize
    contentRange = request.headers.get('range')

    if contentRange is not None:
        contentRanges = contentRange.strip().lower().split('=')[-1]
        rangeStart, rangeEnd, *_ = map(str.strip, (contentRanges + '-').split('-'))
        rangeStart = max(0, int(rangeStart)) if rangeStart else 0
        rangeEnd = min(fileSize - 1, int(rangeEnd)) if rangeEnd else fileSize - 1
        contentLenght = (rangeEnd - rangeStart) + 1
        file = ranged(file, start=rangeStart, end=rangeEnd + 1)
        statusCode = 206
        contentRange = f'bytes {rangeStart}-{rangeEnd}/{fileSize}'

    response = StreamingHttpResponse(file, status=statusCode, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Lenght'] = str(contentLenght)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = contentRange
    return response
def getVideo(request, id:int = 0) -> HttpResponse:
    if request.method == "GET":
        count_id = cur.execute("SELECT COUNT(*) FROM urfub_videos WHERE id > 0").fetchone()[0]
        if count_id == 0 or id > count_id:
            return HttpResponseNotFound("нету", status=404)
        if id == 0:
            vid_id = random.randint(1,count_id)
            vid = videos.objects.get(id=vid_id)
        else:
            vid = videos.objects.get(id=id)

        author = cur.execute("SELECT username FROM auth_user WHERE id == {0}".format(vid.author_id)).fetchone()[0]
        return render(request, "main/video.html", context={'video' : vid, 'author' : author})


def getLikes(request, id = 0):
    if request.method == "POST":
        if id == 0:
            return HttpResponse("Неправильный ID")
        video = get_object_or_404(videos,id=id)
        likes = video.likes
        dislike = video.dislike
        user = request.user
        liked_users = list(video.liked.all())
        if user not in liked_users:
            likes = likes + 1
            video.likes = likes
            video.liked.add(user)
            if user in list(video.disliked.all()):
                video.disliked.remove(user)
                dislike = dislike - 1
                video.dislike = dislike
            video.save()
        request.method = "GET"
        return HttpResponseRedirect(reverse('watchVideo', args=[str(id)]))


def getDislikes(request, id = 0):
    if request.method == "POST":
        if id == 0:
            return HttpResponse("Неправильный ID")
        video = get_object_or_404(videos, id=id)
        likes = video.likes
        dislike = video.dislike
        user = request.user
        disliked_users = list(video.disliked.all())
        if user not in disliked_users:
            dislike = dislike + 1
            video.dislike = dislike
            if user in list(video.liked.all()):
                video.liked.remove(user)
                likes = likes - 1
                video.likes = likes
            video.disliked.add(user)
            video.save()
        request.method = "GET"
        return HttpResponseRedirect(reverse('watchVideo', args=[str(id)]))

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