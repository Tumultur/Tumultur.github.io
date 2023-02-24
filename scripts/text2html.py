import re
import shutil
import os

entry_name = 'kindle'
cjk = True
cjk_range = r'\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30fa\u30fc-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff'
cjk_quotation_styling = '<span style="font-family: \'PingFang SC\', \'Microsoft Yahei\'">'
cjk_quotations = r'[。，；：、《（“‘》）”’]'
latin_quotation_styling = '<span class="quotation-mark">'
apostrophe_styling = '<span class="apostrophe">'

script_dir = 'd:/miscellaneous/personal/code/frontend/git/scripts/'
entries_dir = 'd:/miscellaneous/personal/code/frontend/git/entries/'

input_filename = script_dir+'input.txt'
original_text_dir = entries_dir+'original/'
output_html = entries_dir+entry_name+'.html'

if cjk == False:
    header_filename = script_dir+'header.txt'
else:
    header_filename = script_dir+'cjk_header.txt'

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
            # apostrophe
            line = re.sub(r"(?<!')([a-zA-Z])([a-zA-Z]*)'([a-zA-Z]+)", r'\1\2'+apostrophe_styling+r'’</span>'+r'\3', line)
            line = re.sub(r'<apos>', r'<span'+apostrophe_styling+r'’</span>', line)
            
            # CJK & Latin spacing
            line = re.sub(r'(['+cjk_range+r']) ([a-zA-Z0-9 ]+) (['+cjk_range+r'])', r'\1&#x2006;\2&#x2006;\3', line)
            line = re.sub(r'(['+cjk_range+r']) ([a-zA-Z0-9 ]+)([。、，；])', r'\1&#x2006;\2\3', line)
            # line = re.sub(r'(['+cjk_range+r']) (<a.*/a>) (['+cjk_range+r'])', r'\1&#x2006;\2&#x2006;\3', line)

            # CJK quotation marks font, no longer useful as stylesheet will do
            # if cjk == True:
            #     line = re.sub(r'“((.(?!“))*)”', cjk_quotation_styling+r'“</span>'+r'\1'+cjk_quotation_styling+r'”</span>', line)
            #     line = re.sub(r'‘((.(?!‘))*)’', cjk_quotation_styling+r'‘</span>'+r'\1'+cjk_quotation_styling+r'’</span>', line)

            # specify font for quotation marks around latin text
            # disabled, instead use different quotation marks styling for CJK and latin articles
            # line = re.sub(r'(?<!class=)"([a-zA-Z ]*)"', latin_quotation_styling+r'“</span>'+r'\1'+latin_quotation_styling+r'”</span>', line)
            # line = re.sub(r"(?<!class=)'([a-zA-Z ]*)'", latin_quotation_styling+r'‘</span>'+r'\1'+latin_quotation_styling+r'’</span>', line)

            # shits above are mostly useless if Word instead of VSCode is used for writing text

            # CJK punctuation spacing, does not work properly in the case of more than 2 consecutive punctuations 
            # line = re.sub(r'([”）’])([。、，；（])', r'<span style="margin-right: -9px">\1</span>\2', line)
            # line = re.sub(r'([。、，；：（])([‘“（’”）])', r'\1<span style="margin-left: -9px">\2</span>', line)
            # line = re.sub(r'^([‘“（])', r'<span style="margin-left: -18px">\1</span>', line)

            # ultimate solution: reduce spacing for all characters in a series of consecutive punctuations, except the last one
            while True:
                subbed_line = re.sub(r'('+cjk_quotations+r')('+cjk_quotations+r')', r'<span style="margin-right: -9px">\1</span>\2', line)
                if subbed_line == line:
                    break
                line = subbed_line

            # acronyms
            # format: (CAPITAL)
            line = re.sub(r'\(([A-Z]+)\)', r'<abbr>'+r'\1'+r'</abbr>', line)

            # hyperlinks
            # format: {link}{alternative}
            line = re.sub(r' \{((.(?!\{))*)\}\{((.(?!\{))*)\} ', r'&#x2006;<a href="\1" target=_blank>\3</a>&#x2006;', line)

            # spacing in parentheses
            line = re.sub(r'\(((.(?!\())*)\)', r'(<span style="display: inline-block; width: 1.5px"></span>\1<span style="display: inline-block; width: 1.5px"></span>)', line)

            # inline code block
            # format: [code]
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

    # image
    elif input_type == 'i':
        output_lines.append(
            ' '*8+'<div class="entry-image-content">\n'
            +' '*12+'<img src="'
            +input_lines[0]
            +'">\n'
            +' '*8+'</div>\n'
        )

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
        with open(output_html, 'w', encoding='utf8') as output_file:
            for i in output_lines:
                output_file.write(i)
            output_file.write(
                ' '*4+'</main>\n'
                +'</body>'
            )
        shutil.copy(input_filename, original_text_dir+entry_name+'.txt')

