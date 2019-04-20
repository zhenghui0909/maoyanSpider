# 'money': '\uf114\uf209.\ue612\ue612亿',
from maoyan_font import MaoyanFontParser

parser = MaoyanFontParser()
font = parser.load('http://vfile.meituan.net/colorstone/294024cb386679d8e940022d5e3b6a162088.woff')
print(font.normalize('\uf114.\uf209'))