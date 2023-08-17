import json as js
import os.path


class obj:
    def __init__(self, path,data=None):
        self.path = path
        self.data = data
        if os.path.exists(path):
            self.jf = self.read()
        if data:
            self.save()

    def save(self):

        with open(self.path, "w",encoding="utf-8") as dump_f:
            # 把json写入文件，ensure_ascii=False，保存中文编码
            js.dump(self.data, dump_f,ensure_ascii=False)
    def read(self):
        with open(self.path, 'r',encoding="utf-8") as load_f:
            load_dict = js.load(load_f)
            #load_dict = js.dumps(load_dict,ensure_ascii=False) # 转换编码
            return load_dict


if __name__ == '__main__':
    path = "record1.json"
    data = {"你好":"hello"}
    aa = json(path,data=data)
    aa.save()
    print(aa.jf["你好"])