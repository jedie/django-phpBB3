# coding: utf-8

"""
    example views
    ~~~~~~~~~~~~~
    
    Note: you can use mod_rewrite, too. See example file.

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from djangobb_forum.models import Post, Topic


def redirect_phpbb2django(request):
    """
    example view for redirect old phpBB3 topic/post urls to DjangoBB urls.
    """
    if "t" in request.GET:
        key = "t"
        model_class = Topic
    elif "p" in request.GET:
        key = "p"
        model_class = Post
    else:
        raise Http404("No ID is GET parameter.")

    raw_id = request.GET[key]

    try:
        id = int(raw_id)
    except ValueError:
        raise Http404("ID is not a integer.")

    queryset = model_class.objects.only("id")
    instance = get_object_or_404(queryset, id=id)
    url = instance.get_absolute_url()

    return HttpResponsePermanentRedirect(url)
