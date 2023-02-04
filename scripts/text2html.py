import re
import shutil

entry_name = 'rant'
input_filename = 'd:/miscellaneous/personal/code/frontend/git/scripts/input.txt'
header_filename = 'd:/miscellaneous/personal/code/frontend/git/scripts/header.txt'
output_filename = 'd:/miscellaneous/personal/code/frontend/git/scripts/output.txt'
output_html = 'd:/miscellaneous/personal/code/frontend/git/entries/'+entry_name+'.html'

def conv_html(input_lines, input_type='p'):
    # omit type identifier
    input_lines = input_lines[1:] 

    # code block
    if input_type == 'c':
        output_lines.append(' '*8+'<table class="entry-code">\n')
        line_number = 1
        for line in input_lines:
            # highlight
            line = re.sub(r'\[((.(?!\[))*)\]', r'<span class="entry-code-highlight">'+r'\1'+r'</span>', line) 

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

            # omit title and title identifier
            input_lines = input_lines[2:]
        
        for line in input_lines:
            # acronyms
            line = re.sub(r'\(([A-Z]{3,})\)', r'<abbr>'+r'\1'+r'</abbr>', line)

            # hyperlinks
            line = re.sub(r'\{((.(?!\{))*)\}\{((.(?!\{))*)\}', r'<a href="\1" target=_blank>\3</a>', line)

            # spacing in parentheses
            line = re.sub(r'\(((.(?!\())*)\)', r'(<span style="display: inline-block; width: 1.5px"></span>\1<span style="display: inline-block; width: 1.5px"></span>)', line)

            # inline code block
            line = re.sub(r'\[((.(?!\[))*)\]', r'<span class="entry-paragraph-inline-code">'+r'\1'+r'</span>', line)

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

    # entry title
    elif input_type == 't':
        output_lines.append(
            ' '*8+'<div class="entry-header">\n'
            +' '*12+'<p class="entry-header-title">'
            +input_lines[0]
            +'</p>\n'
            +' '*12+'<p class="entry-header-date">'
            +input_lines[1]
            +'</p>\n'
            +' '*8+'</div>\n'
        )

with open(input_filename, encoding='utf8') as input_file:
    with open(header_filename, encoding='utf8') as header_file:
        output_lines = []

        # header
        for i in header_file.readlines():
            output_lines.append(i)
        
        # omit first (empty) item
        all_lines = input_file.read()
        lines = all_lines.split('startsection\n')
        lines = lines[1:]

        # omit empty (originally line break) items
        for content_lines in lines:
            content_lines = content_lines.split('\n')
            while '' in content_lines:
                content_lines.remove('')

            # identify section type
            if content_lines[0] == 'paragraphsection':
                conv_html(content_lines, 'p')
            elif content_lines[0] == 'codesection':
                conv_html(content_lines, 'c')
            elif content_lines[0] == 'imagesection':
                conv_html(content_lines, 'i')
            elif content_lines[0] == 'entrytitlesection':
                conv_html(content_lines, 't')
        
        # write file
        with open(output_filename, 'w', encoding='utf8') as output_file:
            for i in output_lines:
                output_file.write(i)
            output_file.write(
                ' '*4+'</main>\n'
                +'</body>'
            )
        
        shutil.copy(output_filename, output_html)

