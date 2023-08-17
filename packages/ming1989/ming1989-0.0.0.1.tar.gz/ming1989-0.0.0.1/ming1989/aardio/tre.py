class tre:
    def __init__(
        self,
        ctrl,      # 控件
        json_data,         # 数据
    ):
        print(123,1)
        self.ctrl = ctrl
        self.ctrl.insertTable(json_data)


    def onnotify(self,id, code, ptr):
        print(id)


