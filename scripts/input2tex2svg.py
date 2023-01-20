import os
import sys

tex_header = r'''\documentclass[varwidth=8in,12pt]{standalone}
\usepackage{amsmath}
\usepackage{siunitx}
\usepackage{tcolorbox}
\usepackage[version=4]{mhchem}
\begin{document}
\makebox[8in]{$
'''

tex_tail = r'''
$}
\end{document}
'''
if sys.argv[2] == 'long':
    tex = tex_header[:-1]+'$'+sys.argv[1]+'$'+tex_tail[1:]
elif sys.argv[2] == 'short':
    tex = tex_header+sys.argv[1]+tex_tail
with open('output.tex', 'w') as output_tex_file:
    output_tex_file.write(tex)
os.system('latexmk output.tex -pdf')
os.system('pdftocairo -svg output.pdf output.svg')
os.system('latexmk -C')
os.system('del output.tex')