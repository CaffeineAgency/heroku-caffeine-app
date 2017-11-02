from django.http import HttpResponse

from acollection.ydapi.YandexDiskException import YandexDiskException
from hello.worklogic.yandexdisk_worker import download_file, get_file_list, upload_file


def main():
    response = HttpResponse()
    try:
        ss = get_file_list("r34")
        for post in ss:
            for image in post.images_list:
                try:
                    url = image
                    filename = download_file(url)
                    response.write(f"Writing {filename}...<br>")
                    upload_file(filename)
                    response.write(f"Done: {filename}!<br><br><br>")
                except YandexDiskException as ex:
                    continue
        return HttpResponse("")
    except ConnectionError:
        return response.write("Exception!")


if __name__ == '__main__':
    main()