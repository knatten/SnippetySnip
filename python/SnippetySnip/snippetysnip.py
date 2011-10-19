import re

def get_snippet(file_name, snippet_name):
    snippet_begin = "snippetysnip_begin:%s" % snippet_name
    snippet_end = "snippetysnip_end"
    snippet = ""

    in_snippet = False
    found_tag = False
    try:
        file = open(file_name, 'r')
    except IOError as e:
        return "ERROR: Couldn't open file: %s\n" % e
    for line in file:
        if snippet_begin in line:
            in_snippet = True
            found_tag = True
            continue
        if snippet_end in line:
            in_snippet = False
        if in_snippet:
            snippet += line

    if not found_tag:
        return "ERROR: Didn't find %s\n" % snippet_begin
    if in_snippet:
        return "ERROR: Didn't find snippetysnip_end after %s\n" % snippet_begin
    return snippet


def find_end_line(lines, file_name, snippet_name):
    snippet_end = "snippetysnip_end:%s:%s" % (file_name, snippet_name)
    for line_no in range(0, len(lines)):
        if snippet_end in lines[line_no]:
            return line_no
    return -1

snippetstring_with_args = '(.*snippetysnip:[^:]*:[^:]*)(:\(.*\))(.*)'

def get_arguments(string):
    arguments_string = re.search(snippetstring_with_args, string)
    extracted_arguments = {}
    if arguments_string:
        args = arguments_string.group(2)
        for arg in ('before', 'after'):
            for quote in ('"', "'"):
                arg_match = re.search(arg+' *= *%s([^%s]*)%s' % (quote, quote, quote), args)
                if arg_match:
                    extracted_arguments[arg] = arg_match.group(1)
    return extracted_arguments

def remove_arguments(string):
    match = re.search(snippetstring_with_args, string)
    if match:
        return match.group(1) + match.group(3)
    else:
        return string

def insert_snippets(old_buffer, snippet_getter=get_snippet):
    snippet_begin = "snippetysnip:([^:]*):([^:]*)[\s:]" 
    new_buffer = []
    line_no = 0
    while line_no < len(old_buffer):
        line = old_buffer[line_no]
        new_buffer.append(line)
        match = re.search(snippet_begin, line)
        if match:
            arguments = get_arguments(line)
            file_name, snippet_name = match.groups()
            if arguments.has_key('before'):
                new_buffer.append(arguments['before'])
            new_buffer.extend(snippet_getter(file_name, snippet_name).split("\n")[:-1])
            if arguments.has_key('after'):
                new_buffer.append(arguments['after'])
            new_buffer.append(remove_arguments(line).replace("snippetysnip", "snippetysnip_end"))
            end_line = find_end_line(old_buffer[line_no:], file_name, snippet_name)
            if end_line != -1:
                line_no += end_line 
        line_no += 1
    return new_buffer
