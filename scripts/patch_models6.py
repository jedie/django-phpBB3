# coding: utf-8

"""
    scripts
    ~~~~~~~

    HACK!

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

new_content = ""
with file("../django_phpBB3/models.py", "r") as f:
    in_class = False
    for line in f:
        if "class" in line:
            if "class Post(models.Model):" in line:
                in_class = True
            else:
                in_class = False

        if in_class and " = models." in line and line.strip().startswith("post_"):
            line = line.strip()
            print "_"*79
            print line
            field_name, rest = line.split(" = ", 1)
            print field_name

            new_field_name = field_name[5:]
            print new_field_name

            line = '    %s = %s db_column="%s",\n' % (new_field_name, rest, field_name)
            print line

        new_content += line


print new_content
with file("../django_phpBB3/models.py", "w") as f:
    f.write(new_content)

