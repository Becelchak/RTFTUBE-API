# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
from typing import IO, Generator

MAX_UPLOAD_SIZE = 214958080

import random
import sqlite3
import pymysql
from urfub.yandex_s3_storage import *

from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import videos
from django.urls import reverse
from django.contrib import messages

import boto3


# conn_db = sqlite3.connect('db.sqlite3', uri=True, check_same_thread=False)
conn_db = pymysql.connect(database=os.environ['DB_NAME'],
                          user='root',
                          password=os.environ['DB_PASSWORD'],
                          host='127.0.0.1')
cur = conn_db.cursor()

my_session = boto3.session.Session()
s3 = my_session.client('s3',
                       endpoint_url=ENDPOINT_URL,
                       aws_access_key_id=ACCESS_KEY,
                       region_name=REGION_NAME,
                       aws_secret_access_key=SECRET_ACCESS_KEY)


# Вывод главной страницы
def main(request):
    vid = videos.objects.all()[0:3]
    authors = {}
    for video in vid:
        video.url_storage = s3.generate_presigned_url(ClientMethod='get_object',
                                                      Params={
                                                          'Bucket': BUCKET_NAME,
                                                          'Key': video.key
                                                      })
        # video.save()
        # video.url_storage = URL_ACCESS + video.key
        cur.execute("SELECT username FROM auth_user WHERE id = {0}".format(video.author_id))
        authors[video.id] = cur.fetchone()[0]

    return render(request, 'main/video-main.html', context={'video' : vid, 'authors' : authors})


def findVideo(request):
    return render(request, 'main/video-find.html')

def getIDRange(request):
    cur.execute("SELECT MIN(id) FROM urfub_videos")
    minID = cur.fetchone()[0]
    cur.execute("SELECT MAX(id) FROM urfub_videos")
    maxID = cur.fetchone()[0]
    return render(request,'main/video-find.html', context={'maxID':maxID, 'minID':minID})


# def ranged(
#         file: IO[bytes],
#         start:int = 0,
#         end:int = None,
#         blockSize:int = 8192,
# ) -> Generator[bytes,None,None]:
#     consumed = 0
#
#     file.seek(start)
#     while True:
#         dataLenght = min(blockSize, end - start - consumed) if end else blockSize
#         if dataLenght <= 0:
#             break
#         data = file.read(dataLenght)
#         if not data:
#             break
#         consumed += dataLenght
#         yield data
#
#     if hasattr(file,'close'):
#         file.close()
#
# def getStreamVideo(request,id:int):
#     vid = videos.objects.get(id=1)
#     path = Path(vid.stream.path)
#     file = path.open('rb')
#
#     fileSize = path.stat().st_size
#     statusCode = 200
#     contentLenght = fileSize
#     contentRange = request.headers.get('range')
#
#     if contentRange is not None:
#         contentRanges = contentRange.strip().lower().split('=')[-1]
#         rangeStart, rangeEnd, *_ = map(str.strip, (contentRanges + '-').split('-'))
#         rangeStart = max(0, int(rangeStart)) if rangeStart else 0
#         rangeEnd = min(fileSize - 1, int(rangeEnd)) if rangeEnd else fileSize - 1
#         contentLenght = (rangeEnd - rangeStart) + 1
#         file = ranged(file, start=rangeStart, end=rangeEnd + 1)
#         statusCode = 206
#         contentRange = f'bytes {rangeStart}-{rangeEnd}/{fileSize}'
#
#     response = StreamingHttpResponse(file, status=206, content_type='video/mp4')
#
#     response['Accept-Ranges'] = 'bytes'
#     response['Content-Lenght'] = str(contentLenght)
#     response['Cache-Control'] = 'no-cache'
#     response['Content-Range'] = contentRange
#     return response
def getVideo(request, id:int = 0) -> HttpResponse:
    if request.method == "GET":
        cur.execute("SELECT COUNT(*) FROM urfub_videos WHERE id > 0")
        count_id = cur.fetchone()[0]
        if count_id == 0 or id > count_id:
            return HttpResponseNotFound("Видео с таким ID не существует", status=404)
        if id == 0:
            vid_id = random.randint(1,count_id)
            vid = videos.objects.get(id=vid_id)
        else:
            vid = videos.objects.get(id=id)

        vid.url_storage = s3.generate_presigned_url(ClientMethod='get_object',
                                        Params={
                                            'Bucket': BUCKET_NAME,
                                            'Key': vid.key
                                        })
        cur.execute("SELECT username FROM auth_user WHERE id = {0}".format(vid.author_id))
        author = cur.fetchone()[0]
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

# def getComments(request,id = 0):
#     response = HttpResponse
#     if id == 0:
#         return HttpResponse(random.choice(all_video))
#     for video in all_video:
#         if (video["id"] == id):
#             return response(json.dumps(video["comments"] , ensure_ascii=False), content_type="application/json")
#     return HttpResponse("Неправильный ID")

@csrf_exempt
def postVideo(request):
    if request.method == "POST":
        user = request.user
        title = request.POST['videoеTitle']
        if len(request.FILES) > 0:
            stream = request.FILES["video"]
            bytes = stream.read()
            key = stream.name.replace(' ', '_')
            if stream.size > MAX_UPLOAD_SIZE:
                messages.error(request, ("Слишком большой файл"))
            else:
                request.method = "PUT"
                cur.execute("SELECT MAX(id) FROM urfub_videos")
                nextID = cur.fetchone()[0] + 1
                s3.put_object(Bucket=BUCKET_NAME,
                              Key=key,
                              Body=bytes)
                videos.objects.create(
                    id=nextID,
                    title=title,
                    key=key,
                    author=user,
                )
                messages.success(request, ("Видео {0} успешно загружено".format(title)))
        else:
            messages.error(request, ("Произошла ошибка"))
    request.method = "GET"
    return render(request, 'main/video-upload.html')