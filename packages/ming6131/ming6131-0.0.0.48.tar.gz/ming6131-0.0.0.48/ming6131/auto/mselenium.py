from selenium.webdriver import Chrome, Keys
import time
class obj:
    def __init__(self,
        url,
        cdPath=None,    # 浏览器驱动
        ):
        #   ---- 创建浏览器
        self.path = cdPath
        self.url = url
        self.web = Chrome(executable_path=self.path)
        self.web.get(self.url)


    #   ---- 等待网页元素出现或消失
    def getEle(
        self,
        xpaths:str or list,             # 可以是单个,也可以是多个，循环查找 ，找到一个就算
        wait_time=10,                   # 元素等待时间 秒
        wait_dis=False,                 # 默认是等元素出现，True 是等元素消失
        eleindex=0,                     # 元素结果是多个，默认取第一个
    ):

        # 如果元素提供的是字符串，则转换成列表
        xpaths = [xpaths] if type(xpaths) == str else xpaths

        flag = 0
        for i in range(wait_time * 2):
            for xpath in xpaths:
                try:
                    ele = self.web.find_elements(by="xpath", value=xpath)[eleindex]
                except:
                    ele = None
                if ele and not wait_dis:
                    return ele     # 元素出现了
                if not ele and wait_dis:
                    return True
            time.sleep(0.5)
        if wait_dis:
            print("[等待元素消失]失败：等待超时。")
            return False
        else:
            print("[查找元素]失败：等待超时。")
            return None


    #   ---- 点击网页元素
    def eleClick(web, xpaths, x元素等待时长=10, x执行后延时=0.5,eleindex=0):
        '''

        :param web:
        :param xpaths:
        :param x元素名:
        :param x元素等待时长:
        :param x执行后延时:
        :return:
        '''

        #   ---- 获取网页元素(web,xpath,耗时限制)
        ele, txt = getEle(web, xpaths, x元素等待时长=x元素等待时长,eleindex=eleindex)
        if not ele:
            return False, txt
        try:
            ele.click()
        except:
            return False, "[点击]失败：元素不可被点击。"
        time.sleep(x执行后延时)

        return ele,None


    #   ---- 写值
    def eleSendkeys(web, xpaths, x值, x元素等待时长=10, x执行后延时=0.5, x最大字符数=0, x打字间隔=0,eleindex=0):
        # from selenium.webdriver import Chrome, Keys
        '''

        :param web:
        :param xpaths:
        :param x值: str/键名 单值输入，或按键盘
        :param x元素等待时长:
        :param x执行后延时:
        :param x最大字符数:默认0，表示不限字数
        :param x打字间隔:默认0，表示直接输入，没有间隔
        :return: 成功返回元素True 失败返回False
        '''
        #   ---- 获取网页元素
        ele, txt = getEle(web, xpaths, x元素等待时长=x元素等待时长,eleindex=eleindex)
        if not ele:
            return False, txt

        if type(x值) != str:  # 如果值不是字符串，说明是按键，输入后直接返回
            try:
                ele.send_keys(x值)
            except:
                return False, "[写值]失败：该元素不允许写值。"

        else:  # 如果值是字符串：
            # 处理文本字数
            if x最大字符数 != 0:
                item = ''
                for i in x值:
                    item += i

                    try:
                        lenitem = len(item.encode('gbk'))
                    except:
                        lenitem = len(item)*2
                    if lenitem > x最大字符数:
                        x值 = item[:-1]
                        break

            # 写值
            if x打字间隔 != 0:
                for char in x值:
                    try:
                        ele.send_keys(char)
                        time.sleep(x打字间隔)
                    except:
                        return False, "[写值]失败：该元素不允许写值。"
            else:
                try:
                    ele.send_keys(x值)
                except:
                    return False, "[写值]失败：该元素不允许写值。"

        time.sleep(x执行后延时)
        return True,None


    #   ---- 取元素文本
    def getEleText(
        self,
        xpaths:str or list,             # 可以是单个,也可以是多个，循环查找 ，找到一个就算
        wait_time=10,                   # 元素等待时间 秒
        eleindex=0,                     # 元素结果是多个，默认取第一个
        ):

        #   ---- 获取网页元素(web,xpath,耗时限制)
        ele = self.getEle(xpaths=xpaths, wait_time=wait_time,eleindex=eleindex)
        return ele.text if ele else None

    #   ---- 坐标点击
    def xyClick(web, x, y, x右键=0, x执行后延时=0.5):
        # from selenium.webdriver.common.action_chains import ActionChains
        '''

        :param web:
        :param x: 坐标x
        :param y: 坐标y
        :param x右键: 默认0，表示点击左键
        :param x执行后延时:
        :return:
        '''
        txt = None
        try:
            if x右键 == 1:
                ActionChains(web).move_by_offset(x, y).context_click().perform()  # 右键
            else:
                ActionChains(web).move_by_offset(x, y).click().perform()  # 左键
        except:
            return False, "坐标点击失败：出错了"
        try:
            ActionChains(dr).move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前
        except:
            txt = "坐标成功点击了，但鼠标回位出错。"

        time.sleep(x执行后延时)
        return True, txt







    #   ---- 发布抖音
    def faDy(web, data):

        #   ---- 获取视频文件路径
        infoShow(f">>>开始获取视频文件路径", 1)
        path = getVPath(data)
        if not path:
            # 获取到文件，发布成功会删除，否则会重新获取
            return True
        # 视频名称
        vName = re.findall(r'.*\\(.*)', path)
        infoShow(f">>>开始[发布抖音]：{vName}", 1)

        # ---- 打开链接
        infoShow(f">>>开始[打开链接]", 1)
        web.get(data["url"])

        # ---- 点击上传按钮
        infoShow(f">>>开始[点击上传按钮]", 1)
        xpaths = '//*[@class="upload-btn--9eZLd button--1pFK2"]'
        rs, txt = eleClick(web, xpaths, x执行后延时=2)
        infoShow(txt, 1, f=1)
        if not rs:
            infoShow("可能需要登录", 5, tm=30)
            return False

        # ---- 打开上传文件
        infoShow(f">>>开始[上传文件]", 1)
        rs = openFile(path)
        if not rs:
            return False

        # ---- 写标题
        infoShow(">>>开始[写标题]", 1)
        x值 = data['标题']
        xpaths = '//div[@class="outerdocbody editor-kit-outer-container"]/div'
        rs, txt = eleSendkeys(web, xpaths, x值, x执行后延时=1, x最大字符数=300, x打字间隔=0.1)
        infoShow(txt, 1, f=1)
        if not rs:
            return False
        # ele.click()

        # ---- 写话题
        infoShow(">>>开始[写话题]", 1)
        itemList = copy.deepcopy(data["话题"])
        for i in range(len(itemList)):
            # 随机返回一个值
            x值 = random.choice(itemList)
            itemList.remove(x值)
            x值 = f"#{x值}"
            x值 = x值.replace(" ","")
            rs, txt = eleSendkeys(web, xpaths, x值, x执行后延时=0.1, x打字间隔=0.1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False
            rs, txt = eleSendkeys(web, xpaths, Keys.SPACE, x执行后延时=0.1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False
            rs, txt = eleSendkeys(web, xpaths, Keys.SPACE, x执行后延时=0.1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False
            rs, txt = eleSendkeys(web, xpaths, Keys.SPACE, x执行后延时=0.1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False


        #   ---- 选中购物车
        if data["选中购物车"]:
            infoShow(">>>开始[选择商品]", 1)

            # ---- 切换至购物车
            infoShow("      >>>[点击<购物车下拉列表>]", 1)
            xpath = '//*[@class="semi-select select--2uNK1 semi-select-single"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            infoShow("      >>>[点击<切换到购物车>]", 1)
            xpath = '//div[@class="semi-select-option-list semi-select-option-list-chosen"]//*[text()="购物车"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 写入商品链接
            infoShow("      >>>[写值<商品链接>]", 1)
            xpath = '//input[@class="input-inner--1vKBt form--c83CR"]'
            x值 = data['商品链接']
            rs, txt = eleSendkeys(web, xpath, x值)
            infoShow(txt, 1, f=1)
            if not rs:
                return False
            # ---- 点击商品——”添加链接“
            infoShow("      >>>[点击<添加链接>]", 1)
            xpath = '//span[@class="cart-mybtn--1bHuN"][text()="添加链接"]'
            rs, txt = eleClick(web, xpath)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 写入商品短标题
            infoShow("      >>>[写值<商品短标题>]", 1)
            xpath = '//div[@class="semi-modal-content"]//input[@class="semi-input semi-input-default"]'
            x值 = data['商品短标题']
            rs, txt = eleSendkeys(web, xpath, x值)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 点击”完成编辑“
            infoShow("      >>>[点击<完成编辑>]", 1)
            xpath = '//button[@class="button--1SZwR modal-btn--38eCR primary--1AMXd"][text()="完成编辑"]'
            rs, txt = eleClick(web, xpath,x执行后延时=3)
            infoShow(txt, 1, f=1)
            if not rs:
                return False



        #   ---- 选择小程序
        if data["选中小程序"]:
            infoShow(">>>开始[选择小程序]", 1)

            # ---- 切换至小程序选项
            infoShow("      >>>[点击<小程序下拉列表>]", 1)
            xpath = '//*[@class="semi-select select--2uNK1 semi-select-single"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            infoShow("      >>>[点击<切换到小程序>]", 1)
            xpath = '//div[@class="semi-select-option-list semi-select-option-list-chosen"]//*[text()="小程序"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 写入小程序链接
            infoShow("      >>>[点击<小程序链接输入框>]", 1)
            xpath = '//div[@class="anchor-item--2Gboo"]//span[@class="semi-select-selection-text semi-select-selection-placeholder"]'
            rs, txt = eleClick(web, xpath, x元素等待时长=10, x执行后延时=0.5)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            infoShow("      >>>[写值<小程序链接>]", 1)
            xpath = '//*[@class="semi-input semi-input-default"]'
            x值 = data['小程序链接']
            rs, txt = eleSendkeys(web, xpath, x值)
            infoShow(txt, 1, f=1)
            if not rs:
                return False
            # ---- 选择小程序
            infoShow("      >>>[点击选择<小程序结果>]", 1)
            appName = data['小程序名']
            xpath = f'//*[contains(text(),"{appName}")]'
            rs, txt = eleClick(web, xpath)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

        #   ---- 选中视频分类
        if data["选中视频分类"]:
            infoShow(">>>开始[选择视频分类]", 1)

            # 点击视频分类
            infoShow("      >>>[选择<一级分类>]", 1)
            xpath = '//div[@class="semi-cascader-arrow"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 选择一级分类
            xpath = f'//ul[@class="semi-cascader-option-list"]//*[text()="{data["分类一"]}"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 选择二级级分类
            xpath = f'//ul[@class="semi-cascader-option-list"]//*[text()="{data["分类二"]}"]'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # ---- 写视频标签
            infoShow(">>>开始[写视频标签]", 1)
            xpath = '//div[@class="container--1IzDm"]//input[@class="semi-input semi-input-default"]'
            itemList = copy.deepcopy(data["视频标签"])
            for i in range(len(itemList)):
                # 随机返回一个值
                x值 = random.choice(itemList)
                itemList.remove(x值)
                x值 = x值.replace(" ", "")
                rs, txt = eleSendkeys(web, xpath, x值, x执行后延时=0.1, x打字间隔=0.1)
                infoShow(txt, 1, f=1)
                if not rs:
                    return False
                rs, txt = eleSendkeys(web, xpath, Keys.ENTER, x执行后延时=0.1)
                infoShow(txt, 1, f=1)
                if not rs:
                    return False
                rs, txt = eleSendkeys(web, xpath, Keys.ENTER, x执行后延时=0.1)
                infoShow(txt, 1, f=1)
                if not rs:
                    return False
                rs, txt = eleSendkeys(web, xpath, Keys.ENTER, x执行后延时=0.1)
                infoShow(txt, 1, f=1)
                if not rs:
                    return False

        #   ---- 选中合集
        if data["选中合集"]:
            infoShow(">>>开始[选择合集]", 1)

            # 点开合集下拉框
            xpath = '//div[contains(text(), "请选择合集")]/parent::span/parent::div/parent::div'
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False

            # 选择合集
            infoShow("      >>>[选择<合集>]", 1)
            xpath = f'//div[@class="semi-select-option-list semi-select-option-list-chosen"]//span[contains(text(), "{data["合集名"]}")]'
            print('data["合集名"]',data["合集名"])
            rs, txt = eleClick(web, xpath, x执行后延时=1)
            infoShow(txt, 1, f=1)
            if not rs:
                return False






        #   ---- 循环点击发布，等待选择不同步西瓜
        timeFlag = time.time()
        infoShow(">>>[等待视频上传]...", 3)
        while 1:
            # 滚动条操作至底部
            js1 = "document.documentElement.scrollTop=10000"
            web.execute_script(js1)

            if time.time() - timeFlag > data['上传等待时长']:
                infoShow("[等待视频上传]失败：超时。", 5)
                return False

            # ---- 验证是否发布成功，看发布后的第一个结果元素，如果存在，说明成功
            infoShow("验证发布结果...", 3)
            xpath = '//*[@class="info-title-text--kEYth info-title-small-desc--tW-Ce"]'
            rs, txt = getEle(web, xpath, x元素等待时长=1)
            if rs:
                infoShow(">>>>>>发布成功<<<<<<", 3)
                #   ---- 删除已发布成功的视频
                os.remove(path)
                return True

            # 点击发布
            infoShow("点击[发布]", 3)
            xpath = '//*[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]'
            eleClick(web, xpath, x元素等待时长=1)

            # 点击暂不同步
            infoShow("点击[暂不同步]", 3)
            xpath = "//*[contains(text(),'暂不同步')]"
            eleClick(web, xpath, x元素等待时长=1)
