Python多重字典嵌套用法，方便调用.

第一种方法

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
         try:
             return dict.__getitem__(self, item)
         except KeyError:
             value = self[item] = type(self)()
             return value


第2中方法



class Dict(dict):
    def __missing__(self, key):
        rv = self[key] = type(self)()
        return rv

dict1 = Dict()
dict1['hdc']['BLK_read/s'] = 0.33
print dict1
