import datetime

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	author = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text,nullable=False)
	body = db.Column(db.Text,nullable=False)
	create_date = db.Column(db.DateTime,nullable=False)
	post_date = db.Column(db.DateTime)
	pub_date = db.Column(db.DateTime)
	status = db.Column(db.Integer) #will we have a list of status IDs in another table? How will we differentiate between draft,posted,published,etc?
	last_modified_by = db.Column(db.Integer,nullable=True)
	last_modified_date = db.Column(db.DateTime)
	

  
    def __init__():

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s: %s (%s)" % (self.name, self.path, self.owner)

	
