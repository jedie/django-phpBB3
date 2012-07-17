# coding: utf-8

"""
    scripts
    ~~~~~~~

    HACK!

    Parse data from:
        http://wiki.phpbb.com/index.php?title=Tables&action=edit

    and insert them into model descriptions.

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import re


OLD_RE = re.compile(
    r'(db_column=".*?")', re.IGNORECASE | re.UNICODE# | re.MULTILINE
)


new_content = ""
with file("../django_phpBB3/models.py", "r") as f:
    for line in f:
        if "ForeignKey" in line:
            line = line.strip()
            print "_"*79
            print line
            field_name, rest = line.split(" = ")

            has_id = field_name.endswith("_id")
            if has_id:
                new_field_name = field_name[:-3]
            else:
                new_field_name = field_name

            try:
                old_db_column = OLD_RE.findall(rest)[0]
            except IndexError:
                old_db_column = None

            if not has_id:
                new_db_column = 'db_column="%s"' % field_name
                if old_db_column:
                    rest = rest.replace(old_db_column, new_db_column)
                else:
                    rest += ", " + new_db_column
            else:
                if old_db_column:
                    rest = rest.replace(old_db_column, "")
                    rest = rest.replace(", ,", ",")

            line = "    %s = %s\n" % (new_field_name, rest)
            print line

        new_content += line


#print new_content
with file("../django_phpBB3/models.py", "w") as f:
    f.write(new_content)

