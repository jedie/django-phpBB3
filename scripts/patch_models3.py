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
    for line in f:
        if "primary_key=True" in line:
            line = line.strip()
            print "_"*79
            print line
            field_name, rest = line.split(" = ",1)
#            print field_name

            line = '    id = %s db_column="%s",\n' % (rest, field_name)
            print line

        new_content += line


print new_content
with file("../django_phpBB3/models.py", "w") as f:
    f.write(new_content)

