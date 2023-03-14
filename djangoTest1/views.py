import random
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

all_video = [
    {
        "id" : 1,
        "name" : "Таракан Сергей флексит под татарстан супер гуд почти 10 часов",
        "likeCount" : 996,
        "dislikeCount" : 53,
        "comments" : ["Могло быть лучше","Почему не 20?","Super good"]
    },
    {
        "id" : 2,
        "name" : "Топ 10 аниме битв",
        "likeCount" : 11500,
        "dislikeCount" : 180,
        "comments" : ["Bruh","123","91zxc"]
    }
]

def main(request):
    return render(request,'main/main.html')

def getVideo(request, id = 0):
    response = HttpResponse
    if id == 0:
        return HttpResponse(random.choice(all_video))
    for video in all_video:
        if (video["id"] == id):
            return response(json.dumps(video, ensure_ascii=False), content_type="application/json")
    return HttpResponse("Неправильный ID")



def getLikes(request, id = 0):
    response = HttpResponse
    if id == 0:
        return HttpResponse(random.choice(all_video))
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