class Person:
    name=[]
 
p1=Person()
p2=Person()
# p1.name.append(1)
# print p1.name  # [1]
# print p2.name  # [1]
# print Person.name  # [1]
p1.name = [2]
print p1.name  # [1]
print p2.name  # [1]
print Person.name  # [1]