from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/create'] = 'Users#create'
routes['POST']['/login'] = 'Users#login'
routes['GET']['/main']='Users#main'
routes['POST']['/edit/<sessionid>/<dateid>']='Users#edit'
routes['/delete/<sessionid>/<dateid>']='Users#delete'
routes['POST']['/add/<sessionid>']='Users#add'
routes['/edit_user/<sessionid>/<dateid>']= 'Users#edit_user'
routes['/logout']='Users#logout'