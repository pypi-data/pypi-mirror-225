def tomultiline(text, n):
    '''
    把text平均分成n+1行
    '''
    if n == 1:
        text = text.replace("\n", "")
    else:
        # 求整除后的每份字符长度
        textlen = len(text.encode('gbk'))
        x = textlen // n
        ils = []
        istr = ""
        for str in text:
            istr += str
            if len(istr.encode('gbk')) >= x:
                ils.append(istr)
                istr = ""
        if len(ils)<n:
            ils.append(istr)
        elif istr not in ils:
            ils[-1] += istr

        text = "\n".join(ils)
    return text