from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .forms import PublicKeyForm
from .utils import get_file_type
from .api import get_public_file


def file_list_view(request):
  form = PublicKeyForm(request.POST or None)
  files = []

  if request.method == "POST":
    if not form.is_valid():
      return HttpResponseBadRequest("Некорректные данные формы")

    public_key = form.cleaned_data["public_key"]
    file_type = form.cleaned_data["filter"]

    cache_key = f"yandex_disk_files_{public_key}"
    files = cache.get(cache_key)

    if files is None:
      data = get_public_file(public_key)

      if data and data.get("_embedded"):
        files = data["_embedded"]["items"]
        cache.set(cache_key, files, timeout=600)
      else:
        return HttpResponseBadRequest("Не удалось получить файлы с Яндекс.Диска")

    # Фильтрация по типу файлов
    if file_type != "all" and files:
      files = [
        file for file in files if file_type == get_file_type(file["name"])
      ]

  return render(
    request,
    "./file_list.html",
    {"form": form, "files": files},
  )