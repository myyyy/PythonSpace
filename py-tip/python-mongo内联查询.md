```
if tag == 'parent':
    MongoIns().m_update(WT_STRUCT, {'_id': ObjectId(_id), 'parent.oid': ObjectId(parent_oid)},**{'parent.$.name':name,'parent.$.description':description})
if tag == 'child':
    child_oid = self.get_argument("child_oid")
    MongoIns().m_pull(
        WT_STRUCT, {'_id': ObjectId(_id), 'parent.oid': ObjectId(parent_oid)}, **{'parent.$.child': {"oid":ObjectId(child_oid)}})
    MongoIns().m_addToSet(WT_STRUCT, {'_id': ObjectId(_id), "parent.oid": ObjectId(parent_oid)}, **{'parent.$.child': {'oid': ObjectId(), 'name': name,'description':description}})
self.write(dict(status=True,data='编辑成功'))

```
