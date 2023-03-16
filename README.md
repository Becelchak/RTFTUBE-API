# RTFTUBE-API
Свой маленький уголок с видео

# Показ видео
   **GET** 
   
    video/<int:id>
Возвращает stream видео с указанным ID. В случае отсутствия ID, возвращает stream случайного видео
   
# Показ лайков
**GET** 

    video/<int:id>/scores
Возвращает количество лайков и дизлайков видео с указанным ID
# Показ комментариев
**GET**

    video/<int:id>/comments
Возвращает список комментариев видео с указанным ID
# Загрузка нового видео
**GET**

    video/upload/
Возвращает stream загруженного только что видео

**POST**

    video/upload/
Загружает видео по указанной url ссылке, либо в прикрепленном файле

**PUT**

    video/upload/<int:id>
Заменяет видео с указанным ID на указанное по url ссылке, либо в прикрепленном файле
