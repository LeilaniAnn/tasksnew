from system.core.controller import *
import time
class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')

    def index(self):
        return self.load_view('index.html')

    def main(self): 
        user=self.models['User'].get_user_by_id(session['id'])
        today= time.strftime("%A")+","+time.strftime("%B")+","+time.strftime("%Y")
        print today
        day= time.strftime("%Y-%m-%d")
        print user
        return self.load_view('main.html', user=user, today=today, day=day)

    def add(self,sessionid):
        date_info={
            "session_id": session['id'],
            "task": request.form['task'],
            "date": request.form['date'],
            "time": request.form['time'],
            "status": 'Pending'
        }
        self.models['User'].add_task(date_info)
        return redirect ('/main')

    def delete(self, sessionid, dateid):
        self.models['User'].delete(dateid)
        return redirect ('/main')

    def edit(self, sessionid, dateid):
        update_info={
            "date": request.form['date'],
            "time": request.form['time'],
            "task": request.form['task'],
            "status": request.form['status'],
            "date_id": dateid
        }
        self.models['User'].edit(update_info)
        return redirect ('/main')

    def edit_user(self, sessionid, dateid):
        print 'turnkey'
        user=self.models['User'].get_date_by_id(dateid)
        print user
        return self.load_view('update.html', user=user[0])
        
    def create(self):
        print "User created"
        user_info = {
            "name" : request.form['name'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "dob": request.form['dob'],
            "pw_confirmation" : request.form['confirm_pass']
            }
        create_status = self.models['User'].create_user(user_info)
        print create_status
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['name']
            session['email'] = create_status['user']['email']
            session['dob']=create_status['user']['dob']
            session['password'] = create_status['user']['pw_hash']
            return redirect('/main')
        else:
            for message in create_status['errors']:
                flash(message, 'you have errors!')
            return redirect('/')

    def login(self):
        print request.form['email']
        login_info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        user_login = self.models['User'].login_user(login_info)
        if user_login['status'] == True:
            session['email'] = user_login['user']['email']
            session['id'] = user_login['user']['id']
            return redirect('/main')
        else:
            for message in user_login['errors']:
                flash(message,'errors')
            return redirect('/')
    def logout(self):
        session.clear()
        return self.load_view('index.html')