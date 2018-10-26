import os
from flask import Flask, Response, render_template, redirect
from flask_restful import reqparse,request, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

import sqlite3


app = Flask(__name__)

p_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(p_dir, "test.db"))

app.config['SQLALCHEMY_DATABASE_URI'] = db_file

api = Api(app)
db = SQLAlchemy(app)

NotesHistoryList = []


def find_(student_id):
    [student for student in students if student.id == student][0]


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser(bundle_errors=True)
#parser.add_argument('id', required=False,help='No id provided')
parser.add_argument('title', required=True, help='No title provided')
parser.add_argument('content', required=True, help='No content provided')


class NoteS(db.Model):
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200),primary_key=True)
    content = db.Column(db.String(800))
    created_date = db.Column(db.DateTime, default=db.func.now())
    modified_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class NotesHistory(db.Model):
    def __init__(self, ):
        pass

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(800))
    created_date = db.Column(db.DateTime, default=db.func.now())
    modified_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Home(Resource):
     # Default to 200 OK
    def get(self):
        return Response(render_template('home.html', notes = NoteS.query.all()),mimetype='text/html')

    def post(self):
        args = parser.parse_args()
        return render_template("home.html")


        # Set the response code to 201 and return custom headers  return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}


# Todo
# shows a single todo item and lets you delete a todo item
class Note(Resource):
    def get(self, title):
        #abort_if_todo_doesnt_exist(todo_id)
        note = NoteS.query.filter_by(title=title).first()
        #return TODOS[todo_id]
        return Response([note.title, "\n",note.content, "\n", note.created_date.strftime('%m/%d/%Y'), "\n", note.modified_date.strftime('%m/%d/%Y')])

    def delete(self, title):
        #abort_if_todo_doesnt_exist(todo_id)
        note = NoteS.query.filter_by(title=title).first()
        db.session.delete(note)
        db.session.commit()
        #return redirect("/"), 204
        return "", 204

    def put(self, title):
        args = parser.parse_args()

        note = NoteS.query.filter_by(title=title).first()

        NotesHistoryList.append(NotesHistory())

        note.content = args['content']
        #note = NoteS('id': args['id'], 'title': args['title'], 'content': args['content'])
        db.session.commit()
        # Set the response code to 201
        return args['content'], 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class NotesList(Resource):
    def get(self):
        return Response(render_template('home.html', notes = NoteS.query.all()),mimetype='text/html')

    def post(self):
        args = parser.parse_args()
        note = NoteS(title = args['title'], content = args['content'])
        NotesHistoryList.append(NotesHistory())
        db.session.add(note)
        db.session.commit()

        return 201


##
## Actually setup the Api resource routing here
##
api.add_resource(Home, '/')
api.add_resource(Note, '/notes/<string:title>')
api.add_resource(NotesList, '/notes')
#api.add_resource(Note, '/add')
#api.add_resource(Note, '/notes/<note_id>')


if __name__ == '__main__':
    app.run(debug=True)


#[language for language in languages if language['name'] == name]
