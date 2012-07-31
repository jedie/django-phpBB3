# coding: utf-8

"""
    example views
    ~~~~~~~~~~~~~

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from djangobb_forum.models import Post, Topic


def phpbb2django_topic(request):
    """
    example view for redirect old phpBB3 topic urls to DjangoBB topic urls
    """
    raw_topic_id = request.GET.get("t")
    if not raw_topic_id:
        raise Http404("No ID is GET parameter.")

    try:
        topic_id = int(raw_topic_id)
    except ValueError:
        raise Http404("ID is not a integer.")

    queryset = Topic.objects.only("id")
    topic = get_object_or_404(queryset, id=topic_id)
    url = topic.get_absolute_url()
    return HttpResponsePermanentRedirect(url)
