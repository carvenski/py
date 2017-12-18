 
 
 # 在__init__中:
 super(CurrentClassName, self).__init__(self, *args, **kw)
 
 # 在__new__中:
 super(CurrentClassName, cls).__init__(cls, *args, **kw)
 
 
 
