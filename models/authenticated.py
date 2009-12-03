def admin_required():
    login_required()
    person=db(db.person.id == session.authorized).select()[0]
    if not person.global_admin:
        redirect(URL(r=request,f='login'))

def login_required():
    if not session.authorized:
        redirect(URL(r=request,f='login'))

def current_user():
    try:  person=db(db.person.id == session.authorized).select()[0]
    except: person = None
