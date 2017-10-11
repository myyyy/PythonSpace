def getstr(_str,fragment):
    where = []
    sl = len(_str)
    fl = len(fragment)
    sindex = 0
    while sl!=0:
        index = _str.find(fragment)
        if index !=-1:
          where.append(sindex+index)
          a= fl+index
          _str=_str[a:]
          sindex+=fl
        else:
            sl=0
    return where

if __name__ =='__main__':
    where = getstr('12322212323','123')
    print where
