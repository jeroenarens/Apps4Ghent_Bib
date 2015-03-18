var cursor = db.borrowing.find();
while (cursor.hasNext()) {
  var borrowing = cursor.next();
  var split = borrowing.from_date.split('/').map(function(el) { return parseInt(el); });
  var new_date = new Date(split[2], split[1]-1, split[0]);

  db.borrowing.update({_id: borrowing._id}, {$set: {from_date: new_date}});
}
