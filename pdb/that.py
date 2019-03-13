#### use 'import that' equals to 'import pdb'+'pdb.set_trace()' to make breakpoint in any .py file when Debug Python,,

if __name__ == "that":
  import pdb
  pdb.set_trace()
  
## usage :  
## 1: copy that.py to  /python/lib/
## 2: add 'import that' in your breakpoint
