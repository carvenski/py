PATCH_EXPLAIN = """
# ===========
# Background:

Django's ORM establishes a database connection per thread.
For the threads managed by Django (which are supposed to be used for directly
handing web requests), Django ORM cleans the established connections up under
the hood once the processing on the thread completes (= request_finished signal).

On the other hand, in the case where Django ORM models are used in an unmanaged thread,
Django does not handle the cleanup of the connections bound to the thread although the
Django framework automatically associates a new connection to the thread. 
This half-maintained resource possibly can cause some DB connection related issues.

To learn more details of this Django behavior, checking the following ticket 
is helpful for understanding this:
https://code.djangoproject.com/ticket/9878

# =========
# Solution:

First replace django orm's db engine by SQLAlchemy connection pool,
Then we need to add put-connection-back-into-pool action when user thread is finished.
To implement above two features in django in a beautiful way, I make this patch. 
If any suggestions, please contact xing.yang@intel.com. Lets make django better toghther.

# ===============
# What To Patch ?

patch threading.Thread.
  start
  run
patch django.db.backends.mysql.base.
  Database
  DatabaseWrapper.get_new_connection
  
# ===============
# Tested versions

python = 3.7
django = 3.2.15
sqlalchemy = 1.4
pymysql = 1.0
mysql = 5.7
uwsgi = 2.0
"""

import threading
from django.db import close_old_connections
from django.db.backends.mysql import base
from django.db.backends.mysql.base import DatabaseWrapper
from sqlalchemy import pool

def install():
    print(PATCH_EXPLAIN)

    # patch threading.Thread to add django.db.close_old_connections after user's Thread.run
    def patch_Thread_run(func):
        def new_run(*args, **kwargs):
            # call user's run first
            result = func(*args, **kwargs)
            # then call close conn
            close_old_connections()
            return result
        return new_run

    def patch_Thread_start(func):
        def new_start(self, *args, **kwargs):
            # patch user's run in Thread.start because 
            # some users like overide Thread.run, so patch start is more reliable
            threading._old_run = self.run
            self.run = patch_Thread_run(threading._old_run)
            return func(self, *args, **kwargs)
        return new_start

    print("=== patch threading.Thread")
    threading._old_start = threading.Thread.start
    threading.Thread.start = patch_Thread_start(threading._old_start)


    # patch django.db.backends.mysql.base to use sqlalchemy conn pool
    print("=== patch base.Database")
    base._old_Database = base.Database
    base.Database = pool.manage(
        base._old_Database, 
        poolclass=pool.QueuePool, 
        pool_size=5, max_overflow=0, timeout=5,
    )
    print("=== init sqlalchemy conn pool, size= [5]")

    def patch_get_new_connection(func):
        pool_conn_keys = {'charset', 'user', 'database', 'password', 'host', 'port', 'client_flag'}
        def new_func(self, conn_params):
            # patch conn_params because sqlalchemy pool connect serialization bug
            new_conn_params = {}
            for k in pool_conn_keys:
                new_conn_params[k] = conn_params[k]
            return func(self, new_conn_params)
        return new_func

    print("=== patch DatabaseWrapper.get_new_connection")
    DatabaseWrapper._get_new_connection = DatabaseWrapper.get_new_connection
    DatabaseWrapper.get_new_connection = patch_get_new_connection(DatabaseWrapper._get_new_connection)

    
    
