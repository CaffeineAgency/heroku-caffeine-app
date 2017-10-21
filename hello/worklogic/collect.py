from django.http import HttpResponse

from hello.worklogic.yandexdisk_worker import download_file, get_file_list, upload_file
from ydapi.YandexDiskException import YandexDiskException


def main():
    try:
        response = ""
        ss = get_file_list("r34")
        for post in ss:
            for image in post.images_list:
                try:
                    url = image
                    filename = download_file(url)
                    response += "{}<br><br><br>\n\n\n".format(upload_file(filename))
                except YandexDiskException as ex:
                    continue
        return HttpResponse(response)
    except ConnectionError as ex:
        return HttpResponse(ex)


if __name__ == '__main__':
    main()