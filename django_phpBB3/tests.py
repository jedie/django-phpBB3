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

    def test_clean_bbcode3(self):
        post = Post.objects.create(
            text=(
                u'test äöüß'
            ),
            bbcode_uid="1234abcd",
            bbcode_bitfield="foo",
        )
        self.assertEqual(post.get_cleaned_bbcode(),
            u'test äöüß'
        )

    def test_clean_bbcode4(self):
        post = Post.objects.create(
            text=(
                'test äöüß [url=https&#58;//github&#46;com/jedie/PyLucid/views&#46;py:1234abcd]/views.py[/url:1234abcd]'
            ),
            bbcode_uid="1234abcd",
            bbcode_bitfield="foo",
        )
        self.assertEqual(post.get_cleaned_bbcode(),
            'test äöüß [url=https://github.com/jedie/PyLucid/views.py]/views.py[/url]'
        )

    def test_clean_bbcode5(self):
        post = Post.objects.create(
            text=(
                u'test äöüß [url=https&#58;//github&#46;com/jedie/PyLucid/views&#46;py:1234abcd]/views.py[/url:1234abcd]'
            ),
            bbcode_uid="1234abcd",
            bbcode_bitfield="foo",
        )
        self.assertEqual(post.get_cleaned_bbcode(),
            u'test äöüß [url=https://github.com/jedie/PyLucid/views.py]/views.py[/url]'
        )

    def test_clean_bbcode6(self):
        post = Post.objects.create(
            text=(
                u'[quote=&quot;Marcos&quot;:1uh5mkpm]A[/quote:1uh5mkpm] test äöüß'
            ),
            bbcode_uid="1uh5mkpm",
            bbcode_bitfield="foo",
        )
        post = Post.objects.get(pk=post.pk)
        self.assertEqual(post.get_cleaned_bbcode(),
            u'[quote="Marcos"]A[/quote] test äöüß'
        )


class TopicTest(TestCase):
    def test_clean_title(self):
        topic = Topic.objects.create(
            title="A &quot;best practise&quot; &amp; questions."
        )
        self.assertEqual(topic.clean_title(),
            'A "best practise" & questions.'
        )


class UserPasswordTest(TestCase):
    def test_clean_title(self):
        from django.contrib.auth.models import User

        # Create a user with a phpBB3 password
        user = User.objects.create_user('test', 'test@domain.tld')
        self.assertEqual(user.password, '!')
        user.password = "phpBB3_md5$H$9dwN9omKahSh5YzR1R.I7/Q/pGJn5E0"
        user.save()
        self.assertEqual(user.password, "phpBB3_md5$H$9dwN9omKahSh5YzR1R.I7/Q/pGJn5E0")

        # Test a "login"
        self.assertTrue(user.check_password("12345678"))
        # Django has update the password, after "login"
        self.assertEqual(user.password[:20], "pbkdf2_sha256$10000$")
