var cursor =  db.updatedListings.find({averageRating:{$eq:'null'}})

var cursor = db.getCollection('updatedListings').find({averageRating:{$ne: 'null'}}).sort({averageRating:-1})
while (cursor.hasNext()) {
    var record = cursor.next();
    db.ratedListings.save(record);
}

db.createCollection('unratedListingsFirstHalf');
db.createCollection('unratedListingsSecondHalf');

var c1 = db.getCollection('updatedListings').find({averageRating:{$eq:'null'}}).limit(2000);

while (c1.hasNext()) {
    var record = c1.next();
    //console.log(record);
    db.getCollection('unratedListingsFirstHalf').save(record);
}

var c2 = db.getCollection('updatedListings').find({averageRating:{$eq:'null'}}).skip(2000)

while (c2.hasNext()) {
    var record = c2.next();
    db.getCollection('unratedListingsSecondHalf').save(record);
}
