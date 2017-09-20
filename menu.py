class Dict(dict):
    def __missing__(self, key):
        rv = self[key] = type(self)()
        return rv
    
def category_list():
    queryset=category.objects.all()
    f_arr=[]
    row_data=Dict()
    row_pid={}
    for row in queryset:
        row_data[row.id]['pid']=row.pid
        row_data[row.id]['name']=row.name
        row_data[row.id]['css']=row.css
        row_data[row.id]['display']=row.display
        row_data[row.id]['id']=row.id
        if row.pid == 0:
            f_arr.append(row.id)
        else:
            row_pid.setdefault(row.pid, []).append(row_data[row.id])
    res={}
    for pid in f_arr:
        row=Dict()
        if row_pid.has_key(pid):
            row_data[pid]['child']=row_pid[pid]
        else:
            row_data[pid]['child']=[]
        res.setdefault('response', []).append(row_data[pid])

	return res

生成后的json数据


{
    "response": [
        {
            "name": "Python", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 6, 
                    "pid": 2, 
                    "name": "Django开发", 
                    "css": null, 
                    "display": 1
                }, 
                {
                    "id": 26, 
                    "pid": 2, 
                    "name": "爬虫学习", 
                    "css": null, 
                    "display": 1
                }, 
                {
                    "id": 28, 
                    "pid": 2, 
                    "name": "Python开发", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 2, 
            "css": "yui"
        }, 
        {
            "name": "Linux", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 38, 
                    "pid": 4, 
                    "name": "flexpaper", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 4, 
            "css": "js"
        }, 
        {
            "name": "前端学习", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 32, 
                    "pid": 30, 
                    "name": "html前端学习", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 30, 
            "css": "design"
        }, 
        {
            "name": "php", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 36, 
                    "pid": 34, 
                    "name": "phpcms开发", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 34, 
            "css": "yui"
        }, 
        {
            "name": "windows", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 42, 
                    "pid": 40, 
                    "name": "Windows", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 40, 
            "css": null
        }, 
        {
            "name": "微信开发", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 46, 
                    "pid": 44, 
                    "name": "微信小程序", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 44, 
            "css": "design"
        }, 
        {
            "name": "分销常用脚本", 
            "pid": 0, 
            "display": 1, 
            "child": [
                {
                    "id": 50, 
                    "pid": 48, 
                    "name": "SIMWOOD", 
                    "css": null, 
                    "display": 1
                }
            ], 
            "id": 48, 
            "css": null
        }
    ]
}
