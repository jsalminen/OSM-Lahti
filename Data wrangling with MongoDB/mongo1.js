cursor = db.lahti.aggregate([{'$group': {'_id': '$created.user', 'count': {'$sum': 1}}},
	{'$sort': {'count': -1}}])
while(cursor.hasNext()){
	printjson(cursor.next());
}