import datetime
from peewee import *

db = SqliteDatabase('customer_data.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Customer(BaseModel):
    phone_number = CharField(primary_key=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    execute_time = TimeField(default=datetime.datetime(2000,1,1,10,0,0).time)
    last_run_date = DateField(default=datetime.datetime.now().date)
    enabled = BooleanField(default=True)
    
    
if __name__ == "__main__":
    db.connect()
    db.create_tables([Customer])
