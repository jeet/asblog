import time
now=time.time()

try:
    from gluon.contrib.gql import *
    db=GQLDB()
    session.connect(request,response,db=db)
except:
    db=SQLDB()

from gluon.storage import Storage

settings=Storage()
settings.mode='smart'
settings.title='Ajay Maurya'
settings.subtitle='Thoughts'
settings.author='Jeet'
settings.description=''
settings.keywords=''
settings.host_url='http://ajaymaurya.com'
settings.email_verification=False
settings.email_server='smtp.gmail.com:587'
settings.email_auth=None # or 'username:password'
settings.email_sender='you@gmail.com'
settings.administrator_emails=[]
settings.rss_procedures=[]
settings.exposed_procedures=[]
settings.xmlrpc_procedures=[]
settings.json_procedures=[]

db.define_table('person',
                SQLField('alias'),
                SQLField('email'),
                SQLField('password','password'),
                SQLField('post_time','double',default=now),
                SQLField('favorites','text',default='|'))

#db.person.alias.requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db,db.person.alias)]
#db.person.email.requires=[IS_EMAIL(), IS_NOT_IN_DB(db,db.person.email)]

db.define_table('category',
                SQLField('name'),
                SQLField('description','text'),
                SQLField('ranking','integer',default=0),
                SQLField('permalink'),
                SQLField('keywords')
        )

db.category.name.requires=[IS_MATCH('[a-z_]+'),
                           IS_NOT_IN_DB(db,db.category.name)]
db.category.description.requires=IS_NOT_EMPTY()

db.define_table('tag',
                SQLField('name'),
                SQLField('description','text'),
                SQLField('display_name'))

db.tag.name.requires=[IS_MATCH('[a-z_]+'),
                      IS_NOT_IN_DB(db,db.tag.name)]
db.tag.description.requires=IS_NOT_EMPTY()

db.define_table('post',
                SQLField('hotness','double',default=1.0),
                SQLField('clicks','integer',default=1),
                SQLField('post_time','double',default=now),
                SQLField('content','text'),
                SQLField('comments','integer',default=0),
                SQLField('category'),
                SQLField('author',db.person),
                SQLField('author_alias'),
                SQLField('url',length=128),
                SQLField('title',length=128),
                SQLField('published','boolean',default=False),
                SQLField('keywords'),
                SQLField('permalink'),
                SQLField('allow_comments','boolean',default=False)
        )

db.post.url.requires=[IS_NOT_EMPTY()]
db.post.category.requires=IS_IN_DB(db,db.category.name)
db.post.title.requires=IS_NOT_EMPTY()

db.define_table('feeback',
                SQLField('type'),
                SQLField('title'),
                SQLField('author'),
                SQLField('body','text'),
                SQLField('excerpt','text'),
                SQLField('email')
        )

db.define_table('comment',
                SQLField('score','integer',default=1),
                SQLField('post_time','double',default=now),
                SQLField('author',db.person),
                SQLField('author_alias'),
                SQLField('parente','integer',default=0),
                SQLField('post',db.post),
                SQLField('body','text'),
                SQLField('flagged','boolean',default=False))

db.comment.body.requires=IS_NOT_EMPTY()

if len(db().select(db.category.ALL))==0:
    db.category.insert(name='politics',description='')
    db.category.insert(name='programming',description='')
    db.category.insert(name='technology',description='')
    db.category.insert(name='science',description=''),
    db.category.insert(name='Ruby on Rails',description=''),
    db.category.insert(name='Python',description='')
