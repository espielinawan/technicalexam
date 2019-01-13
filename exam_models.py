from pymodm import MongoModel, EmbeddedMongoModel, fields
from pymodm.connection import connect
from pymongo.write_concern import WriteConcern

# Establish a connection to the database.
connect("mongodb://localhost:27017/snaaap_exam", alias="my-exam")


class Merchant(MongoModel):
    name = fields.CharField(required=True, blank=False)
    description = fields.CharField(required=True)
    image = fields.CharField()
	
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-exam'

class Product(MongoModel):
    name = fields.CharField(required=True, blank=False)
    price = fields.FloatField(required=True)
    image = fields.CharField()
    merchant_id = fields.CharField(required=True)
	
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-exam'
		
class Client(MongoModel):
    name = fields.CharField(required=True, blank=False)
    email = fields.CharField(required=True)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-exam'
		
		
class Purchase(MongoModel):
    client_id = fields.CharField(required=True, blank=False)
    product_id = fields.CharField(required=True, blank=False)
    purchase_datetime = fields.DateTimeField(required=True)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-exam'
		
class Promo(MongoModel):
    name = fields.CharField(required=True, blank=False)
    image = fields.CharField()
    start_date = fields.DateTimeField(required=True)
    end_date = fields.DateTimeField(required=True)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-exam'
		
class PromoPurchase(MongoModel):
    client_id = fields.CharField(required=True, blank=False)
    promo_id = fields.CharField(required=True, blank=False)
    datetime = fields.DateTimeField(required=True)
    status = fields.CharField(required=True, blank=False)
    
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-exam'
		
				
		