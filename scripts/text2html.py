import re

def conv_html(input_lines, input_type='p'):
    input_lines = input_lines[1:] # omit type identifier

    # code block
    if input_type == 'c':
        output_lines.append(' '*8+'<table class="entry-code">\n')
        line_number = 1
        for line in input_lines:
            line = re.sub(r'\[((.(?!\[))*)\]', r'<span class="entry-code-highlight">'+r'\1'+r'</span>', line) # highlight
            line = line.replace('emptyline', '')
            output_lines.append(
                ' '*12
                +'<tr class="entry-code-line">\n'
                +' '*16
                +'<td class="entry-code-line-number">'
                +str(line_number)
                +'</td>\n'
                +' '*16
                +'<td class="entry-code-content">'
                +line
                +'</td>\n'
                +' '*12
                +'</tr>\n'
            )
            line_number += 1
        output_lines.append(' '*8+'</table>\n')

    # paragraph
    elif input_type == 'p':
        output_lines.append(' '*8+'<div class="entry-paragraph">\n')

        # identify title
        if input_lines[0] == 'titlesection':
            output_lines.append(
                ' '*12+'<p class="entry-paragraph-title">'
                +input_lines[1]
                +'</p>\n'
            )
            input_lines = input_lines[2:] # omit title and title identifier
        
        for line in input_lines:
            line = re.sub(r'\[((.(?!\[))*)\]', r'<span class="entry-paragraph-inline-code">'+r'\1'+r'</span>', line) # inline code block
            line.replace('emptyline', '')
            output_lines.append(
                ' '*12
                +'<p class="entry-paragraph-content">\n'
                +' '*16
                +line
                +'\n'
                +' '*12
                +'</p>\n'
            )
        output_lines.append(' '*8+'</div>\n')
    

        # write file
    with open('c:/users/admin/desktop/output.txt', 'w', encoding='utf8') as output_file:
            for i in output_lines:
                output_file.write(i)

with open('c:/users/admin/desktop/input.txt', encoding='utf8') as input_file:
    output_lines = []
    all_lines = input_file.read()
    lines = all_lines.split('startsection\n')
    lines = lines[1:] # omit first (empty) item
    for content_lines in lines:
        content_lines = content_lines.split('\n')
        while '' in content_lines:
            content_lines.remove('') # omit empty (originally line break) items

        # identify section type
        if content_lines[0] == 'paragraphsection':
            conv_html(content_lines, 'p')
        elif content_lines[0] == 'codesection':
            conv_html(content_lines, 'c')
        elif content_lines[0] == 'imagesection':
            conv_html(content_lines, 'i')

