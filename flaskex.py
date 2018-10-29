import os
from flask import Flask, Response, render_template, redirect
from flask_restful import reqparse,request, abort, Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import sqlite3


app = Flask(__name__)

p_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(p_dir, "notes.db"))

app.config['SQLALCHEMY_DATABASE_URI'] = db_file
api = Api(app)
db = SQLAlchemy(app)


def copy_data(note, to):
    note = to(title = note.title, note_id = note.id, content = note.content, created_date = note.created_date, modified_date = note.modified_date)
    db.session.add(note)
    return note


def find_and_abort_if_doesnt_exist(number):
    note = DB_Notes.query.filter_by(id=number).first()
    if note is None:
        abort(404, message="Note number {} doesn't exist".format(number))
    else:
        return note

parser = reqparse.RequestParser(bundle_errors=True)
#parser.add_argument('id', required=False,help='No id provided')
parser.add_argument('title', required=True, help='No title provided')
parser.add_argument('content', required=True, help='No content provided')

parserPut = reqparse.RequestParser(bundle_errors=True)
parserPut.add_argument('content', required=True, help='No content provided')


## sqlalchemy classes to be mapped to db
class DB_BaseColumns(object):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(800))

class DB_Notes(DB_BaseColumns,db.Model):
    created_date = db.Column(db.DateTime, default=db.func.now())
    modified_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class DB_NotesHistory(DB_BaseColumns,db.Model):
    note_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)

class DB_NotesDeleted(DB_BaseColumns, db.Model):
    note_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    deletion_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

## fields needed for json output
note_fields = {
    'id':   fields.Integer,
    'title':   fields.String,
    'content':   fields.String,
    'created_date':   fields.DateTime,
    'modified_date':    fields.DateTime
}

noteH_fields = dict(note_fields)
noteH_fields.update({
    'note_id':   fields.Integer,
}   )

noteD_fields = dict(noteH_fields)
noteD_fields.update({
    'deletion_date':   fields.DateTime,
}   )



class Home(Resource):
    def get(self):
        return Response(render_template('home.html', Notes = DB_Notes.query.all(), NotesHistory = DB_NotesHistory.query.all(), NotesDeleted = DB_NotesDeleted.query.all()), mimetype='text/html')

##flask classes for routing
class Note(Resource):
    @marshal_with(note_fields)
    def get(self, number):
        return find_and_abort_if_doesnt_exist(number), 200

    def delete(self, number):
        note = find_and_abort_if_doesnt_exist(number)
        copy_data(note,DB_NotesHistory)
        copy_data(note,DB_NotesDeleted)

        db.session.delete(note)
        db.session.commit()
        #return redirect("/"), 204
        return "", 204

    def put(self, number):
        args = parserPut.parse_args()
        note = find_and_abort_if_doesnt_exist(number)
        noteH = copy_data(note,DB_NotesHistory)
        note.content = args['content']
        noteH.modified_date = db.func.now()
        db.session.commit()
        return args['content'], 201

class NotesList(Resource):
    @marshal_with(note_fields)
    def get(self):
        return DB_Notes.query.all(), 200

    def post(self):
        args = parser.parse_args()
        note = DB_Notes(title = args['title'], content = args['content'])
        db.session.add(note)
        db.session.commit()
        return 201

class NotesHistory(Resource):
    @marshal_with(noteH_fields)
    def get(self, number):
        note = DB_NotesHistory.query.filter_by(note_id=number).order_by(DB_NotesHistory.modified_date.desc()).all()
        if note is None:
            abort(404, message="History of note number {} doesn't exist".format(number))
        return note, 200
        #return Response([note.title, "\n",note.content, "\n", note.created_date.strftime('%m/%d/%Y'), "\n", note.modified_date.strftime('%m/%d/%Y')])

class NotesDeleted(Resource):
    @marshal_with(noteD_fields)
    def get(self):
        note = DB_NotesDeleted.query.all()
        if note is None:
            abort(404, message="No deleted notes")
        return note, 200

##setup the Api resource routing
api.add_resource(Home, '/')
api.add_resource(Note, '/note/<int:number>')
api.add_resource(NotesHistory, '/note/<int:number>/history')
api.add_resource(NotesList, '/notes')
api.add_resource(NotesDeleted, '/deleted')


if __name__ == '__main__':
    app.run(debug=False)
