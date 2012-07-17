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
import pprint

from model_data import data # generated with scripts/help_text.py
import re

# Cut Phpbb from table names:
data = dict([(k[5:],v) for k, v in data.items()])
#print data.keys()


FK_RE = re.compile(
    r'{{(.*?)}}', re.IGNORECASE | re.UNICODE | re.MULTILINE
)



new_file_content = ""
with file("../django_phpBB3/models.py", "r") as f:
    model_data = None
    for line in f:
        new_file_content += line
        line = line.strip()
        if not line:
            model_data = None
        
        if model_data and " = models." in line:
            print line
            field_name = line.split(" = ", 1)[0].strip()
            print field_name
            try:
                field_data = model_data[field_name]
            except KeyError:
                print " *** no data for field %r" % field_name
                continue
            print field_data

            mysql_type = field_data['type (MySQL)']
            
            help_text = field_data['content']
            if "{{fk|" in help_text:
                new_file_content, old_line = new_file_content.rsplit("\n",2)[:-1]
                new_file_content += "\n    # %s\n" % old_line.strip()
                
                fk_model, fk_field = FK_RE.findall(help_text)[0].split("|")[1:]
                new_file_content += (
                    '    %(c)s = models.ForeignKey("%(m)s", db_column="%(f)s", to_field="%(f)s")'
                ) % {
                    "c": field_name,
                    "m": fk_model[0].upper() + fk_model[1:],
                    "f": fk_field
                }
            elif "unsigned" in mysql_type and "IntegerField" in line:
                new_file_content, old_line = new_file_content.rsplit("\n",2)[:-1]
                new_file_content += "\n"
                #new_file_content += "    # %s\n" % old_line.strip()
                
                new_line = old_line
                if "unsigned" in mysql_type:
                    new_line = new_line.replace("IntegerField", "PositiveIntegerField")                
                if "tinyint" in mysql_type:
                    new_line = new_line.replace("IntegerField", "SmallIntegerField")
                
                new_file_content += new_line
            
            if line.endswith(")"):
                new_file_content = new_file_content.rstrip(")\n")
            if new_file_content.endswith("("):
                new_file_content += "\n"
            else:
                new_file_content += ",\n"
                
            new_file_content += "        # %s\n" % mysql_type
            
            if "default" in field_data:
                value = field_data["default"]
                if "&amp" in value: # skip: ???
                    value = None
                elif "unique" in value or "auto_increment" in value: # skip: primary key
                    value = None
                elif "not null" in value: # ???
                    value = None
                
                if value:
                    if value == "&amp;nbsp;":
                        value = '" "' # ???
                    elif value == "0.00":
                        value = 0
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            value = '"%s"' % value

                    new_file_content += '        default=%s,\n' % value
            
            if not "content" in field_data:
                print " *** no 'content' in %s" % repr(field_data)
            else:
                if help_text != "tbd":
                    help_text = help_text.replace('"', "'")
                    new_file_content += '        help_text="%s"\n' % help_text
            
            new_file_content += "    )\n"
                
        
#        print line
        if "(models.Model):" in line:
            model_name = line.split(" ",1)[1].split("(",1)[0]
            
            if not model_name in data:
                model_name2 = model_name + "s"
                if not model_name2 in data:
                    print "no data for the model %s" % model_name
                    continue
                else:
                    model_name = model_name2

            print "_"*79
            print line
            print model_name
            model_data = data[model_name]
            pprint.pprint(model_data)
            
#                
#            if model_name in table_data:
#                print " *** ", table_data[model_name]
#                new_file_content += '    """\n'
#                new_file_content += "    %s\n" % table_data[model_name]
#                new_file_content += '    """\n'

print new_file_content

with file("../django_phpBB3/models.py", "w") as f:
    f.write(new_file_content)

    
    