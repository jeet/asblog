response.title="Ajay Maurya's Blog"

if not session.categories:
    session.categories=[r.name for r in db().select(db.category.ALL)]

def register():
    form=SQLFORM(db.person,fields=['alias', 'email','password'])
    if form.accepts(request.vars,session):
          session.authorized=form.vars.id
          session.email=form.vars.email
          session.alias=form.vars.alias
          session.flash='user registered'
          redirect(URL(r=request,f='index'))
    return dict(form=form)

def login():
    db.person.email.requires=IS_NOT_EMPTY()    
    form=SQLFORM(db.person,fields=['email','password'])
    if FORM.accepts(form,request.vars,session):
       users=db(db.person.email==form.vars.email)\
               (db.person.password==form.vars.password).select()
       if len(users):
          session.authorized=users[0].id
          session.email=users[0].email
          session.alias=users[0].alias
          session.flash='user logged in'
          redirect(URL(r=request,f='index'))
       else:
          form.errors['password']='invdalid password'
    return dict(form=form)

def logout():
    session.authorized=None
    session.email=None
    session.alias=None
    session.flash='user logged out'
    redirect(URL(r=request,f='index'))

def index():
    sorts={'new':~db.post.post_time,
           'hot':~db.post.hotness,
           'score':~db.post.score}
    try: page=int(request.args[2])
    except: page=0
    try: sort=request.args[1]
    except: sort='hot' 
    orderby=sorts[sort]
    try: category=request.args[0]
    except: category='politics'
    limitby=(50*page,50*(page+1)+1)
    post=db(db.post.category==category).select(orderby=orderby,limitby=limitby)
    return dict(category=category,post=post,sort=sort,sorts=sorts.keys(),page=page)

def bookmark():
    try: item=db(db.post.id==request.args[0]).select()[0]
    except: redirect(URL(r=request,f='index'))
    item.update_record(clicks=item.clicks+1)
    redirect(item.url)

##Commented  logged in     
def post(): 
#    if not session.authorized:
#        redirect(URL(r=request,f='login'))
    form=SQLFORM(db.post,fields=['url','title','category','content'])
    form.vars.author=session.authorized
    form.vars.author_alias=session.alias
    if form.accepts(request.vars,session):
        session.flash='news posted'
        redirect(URL(r=request,f='index',args=[form.vars.category]))
    return dict(form=form)

def report():
    try:
        db(db.post.id==request.args[0]).update(flagged=True)
        session.flash='thanks for your feedback'
    except:
        session.flash='internal error'
    redirect(request.env.http_referer)

def delete():
    if not session.authorized: redirect(request.env.http_referer)
    try:
        post=db(db.post.id==request.args[0]).select()[0]
        if post.author==session.authorized:
            db(db.post.id==request.args[0]).delete()
        session.flash='Post item deleted'
    except:
        session.flash='internal error'
    redirect(URL(r=request,f='index',args=[post.category]))

def vote():
    if not session.authorized: redirect(request.env.http_referer)
    post=db(db.post.id==request.args[1]).select()[0]
    if request.args[0]=='up':
       post.update_record(score=post.score+1)
    elif request.args[0]=='down':
       post.update_record(score=post.score-1)
    redirect(request.env.http_referer)

def permalink():
    try: comment=db(db.comment.id==request.args[0]).select()[0]
    except: redirect(request.env.http_referer)
    comments=db(db.comment.post==comment.post).select(orderby=db.comment.score)
    post=comment.post
    items=[]
    tree={}
    forms={}
    pivot=None
    for c in comments:
        if not tree.has_key(c.parente): tree[c.parente]=[c]
        else: tree[c.parente].append(c)
        if c.id==comment.id: pivot=c.parente
        if session.authorized:
           f=SQLFORM(db.comment,fields=['body'],labels={'body':''})
           f.vars.author=session.authorized          
           f.vars.author_alias=session.alias
           f.vars.post=post
           f.vars.parente=c.id
           if f.accepts(request.vars,formname=str(c.id)):
              session.flash='comment posted'
              redirect(URL(r=request,args=request.args))
           forms[c.id]=f
    tree[pivot]=[comment]
    response.view='default/comments.html'
    return dict(item=None,form=None,tree=tree,forms=forms,parent=pivot)

def vote_comment():
    if not session.authorized: redirect(request.env.http_referer)
    comment=db(db.comment.id==request.args[1]).select()[0]
    if request.args[0]=='up':
       comment.update_record(score=comment.score+1)
    elif request.args[0]=='down':
       comment.update_record(score=comment.score-1)
    redirect(request.env.http_referer)

def report_comment():
    try:
        db(db.comment.id==request.args[0]).update(flagged=True)
        session.flash='thanks for your feedback'
    except:
        session.flash='internal error'
    redirect(request.env.http_referer)

def person():
    session.flash='sorry, not yet implemented'
    redirect(request.env.http_referer)


def comments():
    try: post=int(request.args[0])
    except: redirect(URL(r=request,f='index'))
    if session.authorized:
        form=SQLFORM(db.comment,fields=['body'],labels={'body':''})
        form.vars.author=session.authorized
        form.vars.author_alias=session.alias
        form.vars.post=post
        if form.accepts(request.vars,formname='0'): 
            response.flash='comment posted'
    else: form=None
    try:
        item=db(db.post.id==post).select()[0]
        comments=db(db.comment.post==post).select(orderby=~db.comment.score)
    except: redirect(URL(r=request,f='index'))
    items=[]
    tree={}
    forms={}
    for c in comments:
        if not tree.has_key(c.parente): tree[c.parente]=[c]
        else: tree[c.parente].append(c)
        if session.authorized:
           f=SQLFORM(db.comment,fields=['body'],labels={'body':''})
           f.vars.author=session.authorized          
           f.vars.author_alias=session.alias
           f.vars.post=post
           f.vars.parente=c.id
           if f.accepts(request.vars,formname=str(c.id)):
              session.flash='comment posted'
              redirect(URL(r=request,args=request.args))
           forms[c.id]=f
    return dict(item=item,form=form,tree=tree,forms=forms,parent=0)

def edit_comment():
    if not session.authorized: redirect(request.env.http_referer)
    id=request.args[0]
    try:
        comment=db(db.comment.id==id).select()[0]
        if not comment.author==session.authorized: raise Exception
    except: redirect(URL(r=request,f='index'))
    form=SQLFORM(db.comment,comment,fields=['body'],showid=False,deletable=True,labels={'body':'Comment'})
    if form.accepts(request.vars,session):
        session.flash='comment edited'
        redirect(URL(r=request,f='comments',args=[comment.post]))
    return dict(form=form)

### todo:
"""
prevent users from voting twice: vote, vote_comment
adjust layout
allow different types of news sorting
"""
