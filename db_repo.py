import datetime
from peewee import *

db = SqliteDatabase('customer_data.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Customer(BaseModel):
    phone_number = CharField(primary_key=True)
    created_date = DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    execute_time = TimeField(default="10:00:00")
    last_run_date = DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
    enabled = BooleanField(default=True)
    
    
if __name__ == "__main__":
    db.connect()
    db.create_tables([Customer])
