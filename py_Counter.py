计数统计相信大家都不陌生，简单地说就是统计某一项出现的次数。实际应用中很多需

求都需要用到这个模型，如检测样本中某一值出现的次数、日志分析某一消息出现的频率、

分析文件中相同字符串出现的概率等。这种类似的需求有很多种实现方法

>>> from collections import Counter
>>> some_data = ['a','2',2,4,5,'2','b',4,7,'a',5,'d','a','z']
>>> print Counter(some_data)
Counter({'a': 3, 4: 2, 5: 2, '2': 2, 2: 1, 'b': 1, 7: 1, 'z': 1 , 'd': 1})
Counter 类是自Python2.7 起增加的，属于字典类的子类，是一个容器对象，主要用来统

计散列对象，支持集合操作+、-、&、|，其中& 和| 操作分别返回两个Counter 对象各元素

的最小值和最大值。它提供了3 种不同的方式来初始化：

Counter("success") #可迭代对象
Counter(s=3,c=2,e=1,u=1) # 关键字参数
Counter({"s":3,"c":2,"u":1,"e":1}) # 字典
可以使用elements() 方法来获取Counter 中的key 值。

>>> list(Counter(some_data).elements())
['a', 'a', 'a', 2, 'b', 4, 4, 5, 5, 7, '2', '2', 'z', 'd']
利用most_common() 方法可以找出前N 个出现频率最高的元素以及它们对应的次数。

>>> Counter(some_data).most_common(2)
[('a', 3), (4, 2)]
当访问不存在的元素时，默认返回为0 而不是抛出KeyError 异常。

>>> (Counter(some_data))['y']
0
update() 方法用于被统计对象元素的更新，原有Counter 计数器对象与新增元素的统计

计数值相加而不是直接替换它们。

subtract() 方法用于实现计数器对象中元素统计值相减，输入和输出的统计值允许为0 或

者负数。

>>> c = Counter("success") #Counter({'s': 3, 'c': 2, 'e': 1, 'u': 1})
>>> c.update("successfully") #'s': 3, 'c': 2, 'l': 2, 'u': 2, 'e': 1, 'f': 1, 'y': 1
>>> c #s 的值为变为6，为上面s 中对应值的和
Counter({'s': 6, 'c': 4, 'u': 3, 'e': 2, 'l': 2, 'f': 1, 'y': 1})
>>> c.subtract("successfully")
>>> c
Counter({'s': 3, 'c': 2, 'e': 1, 'u': 1, 'f': 0, 'l': 0, 'y': 0})
