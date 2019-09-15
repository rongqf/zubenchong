

class apibase:
    userid = 0
    islogin = False
    response = None
    ret = 1
    desc = ''
    def __init__(self):
        #self.param = param
        if self.islogin:
            pass

        
    def exec_handle(self, param):
        data = self.handle(param)
        rst = {'ret':  self.ret,
                'desc': self.desc,
                'data': data
            }
        return rst
        
    def handle(self):
        pass


    def before(self):
        return True

    def after(self):
        pass

    
    
    
