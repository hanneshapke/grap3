from .app import db

grocery_to_list = db.Table(
    'grocery_to_list',
    # db.Column('id', db.Integer, primary_key=True),
    db.Column('grocery_id', db.Integer, db.ForeignKey('grocery.id')),
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'))
    )


class Grocery(db.Model):
    __tablename__ = 'grocery'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def init(self, **kwargs):
        self.name = kwargs.get('name')
        return self

    def __repr__(self):
        return '<{}>'.format(self.name)


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    groceries = db.relationship(
        Grocery, secondary=grocery_to_list, backref="list")

    def __repr__(self):
        return '<List containing {}>'.format(self.groceries)
