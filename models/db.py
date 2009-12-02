import time
now=time.time()

try:
    from gluon.contrib.gql import *
    db=GQLDB()
    session.connect(request,response,db=db)
except:
    db=SQLDB()

db.define_table('person',
    SQLField('alias'),
    SQLField('email'),
    SQLField('password','password'),
    SQLField('post_time','double',default=now),
    SQLField('favorites','text',default='|'))

db.person.alias.requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db,db.person.alias)]
db.person.email.requires=[IS_EMAIL(), IS_NOT_IN_DB(db,db.person.email)]

db.define_table('category',
   SQLField('name'),
   SQLField('description','text'))

db.category.name.requires=[IS_MATCH('[a-z_]+'),
                           IS_NOT_IN_DB(db,db.category.name)]
db.category.description.requires=IS_NOT_EMPTY()

db.define_table('news',
   SQLField('hotness','double',default=1.0),
   SQLField('clicks','integer',default=1),
   SQLField('score','integer',default=1),
   SQLField('post_time','double',default=now),
   SQLField('comments','integer',default=0),
   SQLField('category'),
   SQLField('author',db.person),
   SQLField('author_alias'),
   SQLField('url',length=128),
   SQLField('title',length=128),
   SQLField('flagged','boolean',default=False))

db.news.url.requires=[IS_NOT_EMPTY()]
db.news.category.requires=IS_IN_DB(db,db.category.name)
db.news.title.requires=IS_NOT_EMPTY()

db.define_table('comment',
   SQLField('score','integer',default=1),
   SQLField('post_time','double',default=now),
   SQLField('author',db.person),
   SQLField('author_alias'),
   SQLField('parente','integer',default=0),
   SQLField('news',db.news),
   SQLField('body','text'),
   SQLField('flagged','boolean',default=False))

db.comment.body.requires=IS_NOT_EMPTY()

if len(db().select(db.category.ALL))==0:
   db.category.insert(name='politics',description='')
   db.category.insert(name='programming',description='')
   db.category.insert(name='technology',description='')
   db.category.insert(name='science',description='')
