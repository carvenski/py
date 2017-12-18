```
What happens when you save? [when you call save() to save one object, what functions will django call one by one ??]

When you save an object, Django performs the following steps:

1.Emit a pre-save signal. The signal django.db.models.signals.pre_save is sent, allowing any functions 
listening for that signal to take some customized action.

2.Pre-process the data. Each field on the object is asked to perform any automated data modification that 
the field may need to perform.

Most fields do no pre-processing — the field data is kept as-is. Pre-processing is only used on fields that 
have special behavior. For example, if your model has a DateField with auto_now=True, the pre-save phase will 
alter the data in the object to ensure that the date field contains the current date stamp. (Our documentation 
doesn’t yet include a list of all the fields with this “special behavior.”)

3.Prepare the data for the database. Each field is asked to provide its current value in a data type that can 
be written to the database.

Most fields require no data preparation. Simple data types, such as integers and strings, are ‘ready to write’ 
as a Python object. However, more complex data types often require some modification.

For example, DateField fields use a Python datetime object to store data. Databases don’t store datetime objects,
so the field value must be converted into an ISO-compliant date string for insertion into the database.

4.Insert the data into the database. The pre-processed, prepared data is then composed into an SQL statement for 
insertion into the database.

5.Emit a post-save signal. The signal django.db.models.signals.post_save is sent, allowing any functions listening 
for that signal to take some customized action.
```
