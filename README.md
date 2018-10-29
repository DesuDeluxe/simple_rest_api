# RESTful web service for creating notes and keeping history of changes

Simple web service using Flask-Restful + flask-SQLAlchemy

## Getting Started

### Prerequisites

Using python 3, install libraries flask-restful and Flask-SQLAlchemy

```
pip install flask-restful, Flask-SQLAlchemy
```
### Setup

To create database file run command
```
python -c "from flaskex import db; db.create_all()"
```

## Usage

adding note
```
curl -H "Content-type: application/json" -X POST -d '{"title": "< NOTE TITLE >", "content": "< NOTE >"}' http://localhost:5000/notes
```

modifying note
```
curl -H "Content-type: application/json" -X PUT -d '{"content": "< NOTE EDIT >"}' http://localhost:5000/note/< NOTE ID >
```

deleting note
```
curl -H "Content-type: application/json" -X DELETE  http://localhost:5000/note/< NOTE ID >
```

getting note
```
curl -H "Content-type: application/json" -X GET  http://localhost:5000/note/< NOTE ID >
```

getting all notes
```
curl -H "Content-type: application/json" -X GET  http://localhost:5000/notes
```

getting history of note
```
curl -H "Content-type: application/json" -X GET  http://localhost:5000/note/<NOTE ID>/history
```

getting deleted notes
```
curl -H "Content-type: application/json" -X GET  http://localhost:5000/deleted
```

Opening http://localhost:5000 in a browser prints all database entries 

## Tests


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

