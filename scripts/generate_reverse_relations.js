//var conn = new Mongo();
//var db = conn.getDB("apps4ghent");

// Item.item_copies
var cursor = db.item.find();
while (cursor.hasNext()) {
  var item = cursor.next();
  var item_copies = db.item_copy.find({ "item": item._id }, { "_id": 1 }).toArray();
  var item_copy_ids = item_copies.map(function(item_copy) { return item_copy._id; });

  db.item.update({ _id: item._id }, {$set: { "item_copies": item_copy_ids } });
}

// ItemCopy.borrowings
var cursor = db.item_copy.find();
while (cursor.hasNext()) {
  var item_copy = cursor.next();
  var borrowings = db.borrowing.find({ "item_copy": item_copy._id }, { "_id": 1 }).toArray();
  var borrowing_ids = borrowings.map(function(borrowing) { return borrowing._id; });

  db.item_copy.update({ _id: item_copy._id} , {$set: { "borrowings": borrowing_ids } });
}
