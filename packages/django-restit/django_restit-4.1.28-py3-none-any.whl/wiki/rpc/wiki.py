from rest import decorators as rd
from rest import views as rv
from wiki import models as wiki


@rd.url('page')
@rd.url('page/<int:pk>')
# @rd.login_required
def rest_on_manage_wiki(request, pk=None):
    return wiki.Page.on_rest_request(request, pk)


@rd.url('path')
@rd.url('path/<path:path>')
# @rd.login_required
def rest_on_wiki(request, path=None):
    if path:
        entry = wiki.Page.objects.filter(path=path).last()
        if entry is None:
            return rv.restNotFound(request)
        if request.method == "GET":
            return entry.on_rest_get(request)
        elif request.method == "POST":
            return entry.on_rest_post(request)
        elif request.method == "DELETE":
            return entry.on_rest_delete(request)
    return wiki.Page.on_rest_request(request, None)
