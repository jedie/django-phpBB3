#coding:utf-8


if __name__ == "__main__":
    import os
    import sys
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_phpBB3.test_settings"
    from django.core import management
    #management.call_command("diffsettings", interactive=False)
    management.call_command("test", "django_phpBB3", interactive=False)
    sys.exit()


from django.test import TestCase

from django_phpBB3.models import Post, Topic


class PostTest(TestCase):
    def test_clean_bbcode1(self):
        post = Post.objects.create(text=(
            'DjangoBB <!-- m --><a class="postlink" href="http://djangobb.org/">trac</a><!-- m --> page.'
        ))
        self.assertEqual(post.get_cleaned_bbcode(),
            'DjangoBB [url=http://djangobb.org/]trac[/url] page.'
        )

    def test_clean_bbcode2(self):
        post = Post.objects.create(
            text=(
                'Look at [url=https&#58;//github&#46;com/jedie/PyLucid/views&#46;py:1234abcd]/views.py[/url:1234abcd]'
            ),
            bbcode_uid="1234abcd",
            bbcode_bitfield="foo",
        )
        self.assertEqual(post.get_cleaned_bbcode(),
            'Look at [url=https://github.com/jedie/PyLucid/views.py]/views.py[/url]'
        )


class TopicTest(TestCase):
    def test_clean_title(self):
        topic = Topic.objects.create(
            title="A &quot;best practise&quot; &amp; questions."
        )
        self.assertEqual(topic.clean_title(),
            'A "best practise" & questions.'
        )
