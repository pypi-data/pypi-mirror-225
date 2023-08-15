from django.db import models as dm
from rest import models as rm
from medialib import models as medialib
import re
import mistune
from wiki.renderers import WikiRenderer


class Page(dm.Model, rm.RestModel, rm.MetaDataModel):
    """
    Blog (a collection of articles)
    """
    class RestMeta:
        SEARCH_FIELDS = ["title", "body"]
        SEARCH_TERMS = ["title", "body"]
        CAN_DELETE = True
        GRAPHS = {
            "basic": {
                "fields": [
                    "id",
                    "path",
                    "created",
                    "modified",
                    "title",
                    "parent",
                    "order",
                    "path",
                    "slug",
                ],
            },
            "default": {
                "fields": [
                    "id",
                    "path",
                    "created",
                    "modified",
                    "title",
                    "parent",
                    "order",
                    "slug",
                    "children_paths",
                    "body",
                    ("toHTML", "html")
                ],
                "recurse_into": ["media"],
                "graphs": {
                    "media": "default",
                    "member": "basic",
                    "parent": "basic"
                }
            },
            "rendered": {
                "graphs": {
                    "self": "default",
                    "member": "basic"
                }
            },
            "list": {
                "graphs": {
                    "self": "basic",
                    "member": "basic"
                }
            },
            "toc_child": {
                "graphs": {
                    "self": "basic",
                    "parent": "basic"
                }
            },
            "toc": {
                "extra": ["children"],
                "graphs": {
                    "self": "basic",
                    "children": "toc_child"
                }
            },
        }

    created = dm.DateTimeField(auto_now_add=True, editable=False)
    modified = dm.DateTimeField(db_index=True, auto_now=True)

    member = dm.ForeignKey(
        "account.Member", related_name="+",
        blank=True, null=True, default=None,
        on_delete=dm.SET_NULL)

    group = dm.ForeignKey(
        "account.Group", related_name="+", 
        blank=True, null=True, default=None,
        on_delete=dm.SET_NULL)

    parent = dm.ForeignKey(
        "Page", related_name="children",
        default=None, null=True, blank=True,
        on_delete=dm.CASCADE)

    order = dm.IntegerField(default=0, blank=True)

    title = dm.CharField(max_length=255)
    path = dm.CharField(max_length=255, db_index=True)
    slug = dm.SlugField(db_index=True)

    body = dm.TextField(blank=True)

    is_active = dm.BooleanField(blank=True, default=True)

    @property
    def children_paths(self):
        return list(self.children.all().values_list("path", flat=True))

    def upload__file(self, fobj, name):
        if fobj is None:
            return

        request = self.getActiveRequest()
        if not self.group:
            lib = request.member.getMediaLibrary("wiki")
        else:
            lib = self.group.getMediaLibrary("wiki")
        kind = medialib.MediaItem.guessMediaKind(fobj)
        media = medialib.MediaItem(library=lib, name=fobj.name, member=request.member, kind=kind, newfile=fobj)
        media.save()
        wmedia = PageMedia(media=media, entry=self, group=self.group, member=request.member)
        wmedia.save()

    def set_remove_media(self, value):
        wmedia = PageMedia.objects.filter(pk=value).last()
        if wmedia:
            wmedia.delete()
    
    def set_slug(self, value):
        sanitized_slug = value.strip().lower().replace(' ', '_')
        sanitized_slug = re.sub(r'\W+', '', sanitized_slug)
        sanitized_slug = re.sub(r'__+', '_', sanitized_slug).strip('_')
        if self.slug != sanitized_slug:
            self.slug = sanitized_slug
            # confirm slug is unique
            qset = Page.objects.filter(parent=self.parent, slug=sanitized_slug)
            if qset.count():
                self.slug = f"{sanitized_slug}_{qset.count()+1}"

    def on_rest_pre_save(self, request):
        if not self.slug:
            self.set_slug(self.title)
        self.generatePath()

    def generatePath(self):
        paths = []
        parent = self.parent
        while parent is not None:
            paths.append(parent.slug)
            parent = parent.parent
        paths.append(self.slug)
        self.path = "/".join(paths)
        return self.path

    def toHTML(self):
        renderer = WikiRenderer()
        md_engine = mistune.create_markdown(renderer=renderer)
        md = md_engine(self.body)
        return {
            "toc": renderer.render_toc(),
            "body": md
        }


class PageMetaData(rm.MetaDataBase):
    parent = dm.ForeignKey(Page, related_name="properties", on_delete=dm.CASCADE)


class PageMedia(dm.Model, rm.RestModel):
    class RestMeta:
        GRAPHS = {
            "basic": {
                "graphs": {
                    "media": "default"
                }
            },
            "default": {
                "graphs": {
                    "media": "default"
                }
            }
        }
    created = dm.DateTimeField(auto_now_add=True, editable=False)

    member = dm.ForeignKey(
        "account.Member", related_name="+",
        blank=True, null=True, default=None,
        on_delete=dm.SET_NULL)

    group = dm.ForeignKey(
        "account.Group", related_name="+", 
        blank=True, null=True, default=None,
        on_delete=dm.SET_NULL)

    entry = dm.ForeignKey(Page, related_name="media", on_delete=dm.CASCADE)
    media = dm.ForeignKey("medialib.MediaItem", related_name="+", on_delete=dm.CASCADE)
