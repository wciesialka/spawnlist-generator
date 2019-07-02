def __s(v,t=0):
    s = "".join(["\t" for i in range(t)]) + str(v) + "\n"
    return s

def __dtkv(dic,dicname,level):
    kv = __s(f"\"{dicname}\"",level-1)
    kv += __s("{",level-1)
    
    for key in dic:
        value = dic[key]
        if type(value) is dict:
            kv += __dtkv(value,key,level+1)
        else:
            kv += __s(f"\"{key}\"\t\"{value}\"",level)

    kv += __s("}",level-1)

    return kv

def DictToKeyValues(dic):
    return __dtkv(dic,"TableToKeyValues",1)