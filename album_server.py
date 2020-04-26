from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find_artist(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {} <br>".format(artist)
        result += "Найдено альбомов: {} <br>- ".format(len(album_names))
        result += "<br>- ".join(album_names)
    return result


@route("/albums", method="POST")
def add_album():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    # проверяем данные пользователя
    # проверка корректности ввода года
    if album_data["year"].isdigit() and len(album_data["year"]) == 4:
        # проверяем наличие такого же альбома в базе
        same_album = album.find_same_album(album_data["artist"], album_data["album"])
        if same_album:
            print("уже есть")
            message = "Такой альбом уже присутствует в базе"
            result = HTTPError(409, message)
        else:
            album.save(album_data)
            result = print("Успешно")
    else:
        message = "Некорректный год {}".format(album_data["year"])
        result = HTTPError(400, message)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

# http -f POST http://localhost:8080/albums year=2011 artist=Dima genre=Rock album=First
