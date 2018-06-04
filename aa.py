#encoding:utf8
import re

zzz = '''
<div class="rich_media_content " id="js_content">
    <p style="max-width: 100%;min-height: 1em;box-sizing: border-box !important;word-wrap: break-word !important;">
    <span style="color:#888888;"><span style="font-size: 14px;">本文from 阿里技术</span></span></p>
    <img class=" img_loading" data-ratio="0.5077989601386482" data-s="300,640" data-type="png" data-w="1154" style="box-sizing: border-box !important; word-wrap: break-word !important; visibility: visible !important; width: 670px !important; height: 340.225px !important;" _width="auto" src="http://192.168.32.222:19999/mss?https://mmbiz.qpic.cn/mmbiz_png/Z6bicxIx5naLTsZaDKoYc18G8HicURuUBLFKVET6j4QLHJ00erL5AcnVB3WsK6DxOUBR8yIBerwzcDucrIyQGQPQ/640?wx_fmt=png"></p>
    <img class=" img_loading" data-ratio="0.5086206896551724" data-s="300,640" data-src="http://192.168.32.222:19999/mss?https://mmbiz.qpic.cn/mmbiz_png/Z6bicxIx5naLTsZaDKoYc18G8HicURuUBLw4ibnsTWCN3HQDPIibIPbtVcGKWqnCxjcspF9HypLfjORmIGmGyhicvsQ/640?wx_fmt=png" src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg=="></p>
    <p style="max-width: 100%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
    <p style="white-space: normal;"><br></p><p><br></p>
</div
>'''
print zzz

def ddd(xxx):

    print xxx
    print xxx.groups()
    print xxx.group()
    print xxx.group(0)
    print xxx.group(1)
    return xxx.group(0) + "nosrc="

def ddd2(xxx):

    text = xxx.group()
    if " data-src=" in text and " src=" in text:
        return text.replace(" src=", " nosrc=").replace(" data-src=", " src=")
    else:
        return text

print re.sub(r"<img[^>]*>", lambda sub_result: ddd2(sub_result), zzz)




