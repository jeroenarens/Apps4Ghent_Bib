var cursor = db.borrowing.find();
while (cursor.hasNext()) {
  var borrowing = cursor.next();
  var count = db.borrower.find({_id: borrowing.borrower}).count();

  if (count == 0) {
    var random_number = Math.floor(Math.random() * db.borrower.count());
    var random_borrower = db.borrower.find().limit(-1).skip(random_number).next()

    print("Dangling reference for borrower with id '" + borrowing.borrower + "' replaced by random id '" + random_borrower._id + "'");

    db.borrowing.update({_id: borrowing._id}, {$set: {borrower: random_borrower._id}});
  }
}
