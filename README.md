# Availiable notification service
A handy notification service that you can embed in any of your projects.

The work is based on flask + mongoDB.

# Custom config:
**name_db** - is a name mongo data base.

**address_db** - is a address deploy for mongo data base.

**port_db** - is a port deploy for mongo data base.

**token_users_my** - path to the your code, when it's execute, must return uuid from your user, it's parameter write in session cookie.

**port_app** - port deploy for flask app.

**host_app** - address deploy for flask app.

##
Custom config load from currect dirrectory:

    open('config_app.ini', 'r', encoding='utf-8')
###
Name **config-file** must be:

    config_app.ini
##
### Default config parameters:

    name_db = notify_center
    address_db = 127.0.0.1
    port_db = 58999
    token_users_my = False
    port_app = 19008
    host_app = 127.0.0.1


# Default routes:

    # host_app routes
    /api/v1/create_notify
    /api/v1/delete_notify/<string(length=32):uuid>
    /api/v1/update_notify/<string(length=32):uuid>
    
    # public routes
    /api/v1/get_one_notify/<string(length=32):uuid>
    /api/v1/get_all_notify

Each route is well designed and automated as much as possible.
In addition, you don't have to worry if you deploy the application in public access (host=0.0.0.0), as the user's uuid is automatically created from their own metadata when they use it:
- user agent
- user data query
- other parameters

And also, creating/editing/deleting global notifications (not personal notifications) is done at the same address that was specified for the application deployment itself.

Only a request from **host_app** via the above routes can cause the creation/editing/deletion of a global notification.

# First run:
1. Before you run it, be sure to do collection schema creation for mongoDB, for convenience, the auto-creation file is already written.
Simply write in the console while in the current directory:

        python create_models_in_mongo.py

2. Make sure you have installed all the required packages. To do this, navigate to the project directory and execute in the console:

        pip install -r requirements.txt

3. Great, now try to run the flask application by executing in the console while in the project directory:

        python wsgi_dot_run.py