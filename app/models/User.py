from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        errors = []

        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 2:
            errors.append('Name must be at least 2 characters long')

        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')

        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')

        if not info['dob']:
            errors.append('MUST enter your date of birth to continue!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = 'INSERT INTO users (name, email, pw_hash, dob, created_at, updated_at) VALUES (%s,%s,%s,%s, NOW(), NOW())'
            data=[info['name'], info['email'], hashed_pw, info['dob']]
            self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }

    def get_users(self):
        query = 'SELECT * FROM users'
        return self.db.query_db(query)

    def delete(self, id):
        query='DELETE FROM dates WHERE date_id={}'.format(id)
        return self.db.query_db(query)

    def edit(self, info):
        query='UPDATE dates SET task=%s, date=%s, time=%s, status=%s WHERE date_id=%s'
        data=[info['task'], info['date'], info['time'], info['status'], info['date_id']]
        return self.db.query_db(query, data)

    def add_task(self, info):
        query = 'INSERT INTO dates (session_id, task, date, time, status) VALUES (%s,%s,%s,%s,%s)'
        data=[info['session_id'], info['task'], info['date'], info['time'], info['status']]
        self.db.query_db(query, data)

    def get_user_by_id(self, id):
        query = 'SELECT * FROM users LEFT JOIN dates ON users.id=dates.session_id WHERE dates.session_id={}'.format(id)
        print query
        return self.db.query_db(query)

    def get_date_by_id(self, id):
        query='SELECT * FROM dates WHERE date_id={}'.format(id)
        return self.db.query_db(query)

    def login_user(self, login_info):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        errors = []

        if not login_info['email']:
            errors.append('E-mail field required!')
        elif not EMAIL_REGEX.match(login_info['email']):
            errors.append('Pease enter a valid e-mail address!')

        if not login_info['password']:
            errors.append('Password field required!')
        if errors:
            return {'status': False, 'errors': errors}
        else:
            password = login_info['password']
            user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(login_info['email'])
            users = self.db.query_db(user_query)
            if users[0]:
                if self.bcrypt.check_password_hash(users[0]['pw_hash'], password):
                    return {
                    "status": True,
                    "user": users[0]
                    }
                else:
                    errors.append('Password incorrect!')
                    return {'status': False, 'errors': errors}
