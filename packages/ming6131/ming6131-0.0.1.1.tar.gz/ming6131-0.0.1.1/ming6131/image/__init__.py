from PIL import Image, ImageDraw, ImageFont
import ming6131.text

def fontPng(imagesize,text,ttf,fill,path,spacing=10):
    '''
    使text文本内容的字号与行数自适应指定的画布大小，
    返回文本居中的透明背景的PNG图片
        如果要使图片有颜色，可将以下代码中mode参数改成RGB，具体百度
        Image.new(mode='RGB', size=imagesize)
    :param imagesize: (w,h)画面宽度,画布高度
    :param text: 内容
    :param ttf: 字体
    :param fill: 文本颜色
    :param path: 图片输出文件完整路径
    :param spacing: 行间隙
    :return:
    '''

    # 默认字号范围
    fontsize = (1, 500)

    # 创建画布对象
    imageW = imagesize[0]
    imageH = imagesize[1]
    image = Image.new(mode='RGBA', size=imagesize)
    draw_table = ImageDraw.Draw(im=image)


    # 位置
    xy = (0, 0)

    rw = 1
    itext = ming6131.text.tomultiline(text, rw)

    for ftSize in range(fontsize[0], fontsize[1]):

        # 字体
        font = ImageFont.truetype(ttf, ftSize)
        # 获取字体大小
        size = draw_table.multiline_textbbox(xy=xy, text=itext, font=font, spacing=spacing)
        w = size[2]
        h = size[3]

        if w <= imageW and h <= imageH:
            finalText = itext
            finalFont = font
            fw,fh = w,h

        elif w > imageW and h <= imageH:
            rw += 1
            itext = ming6131.text.tomultiline(text, rw)
        elif w > imageW and h > imageH:
            break
        elif h > imageH:
            break
    text = finalText
    font = finalFont
    x = (imageW-fw)/2
    y = (imageH-fh)/2
    xy = (x,y)

    draw_table.multiline_text(xy=xy, text=text, fill=fill, font=font, align = "center", spacing=spacing )

    image.save(path, 'PNG')  # 保存在当前路径下，格式为PNG

fill='#008B8B'
text = u"DL10-西门子S7-1500博途PLC视频教程-1.基础-21.移动与比较指令及其应用"
ttf = "C:\Down\AaLingGanHei65J.TTF"
imagesize = (1800,300)
path = "png.png"

fontPng(imagesize,text,ttf,fill,path)





