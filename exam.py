#!flask/bin/python
import datetime

from bson.objectid import ObjectId
from flask import Flask, jsonify, abort
from flask import request
from exam_models import Merchant, Product, Client, Purchase, Promo, PromoPurchase
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
	
@app.route('/merchants', methods=['POST'])
def create_merchant():

    error_msg = {'field':'name' ,'message':'Already exist'}
    
    for post_m in Merchant.objects.raw({'name': request.json['name']}):
		return jsonify(error_msg),400

    merchant_post = Merchant(request.json['name'],request.json['description'], request.json['image']).save(force_insert=True)
		#https://image.flaticon.com/icons/svg/33/33750.svg
    
    merchant_out = {
        'name': request.json['name'],
        'description': request.json['description'],
        'image': request.json['image']
    }
	
    return jsonify(merchant_out), 201

@app.route('/products', methods=['POST'])
def create_product():
   
    error_msg = {'error':'You must be a Merchant to add a product'}
    merchant_id = ObjectId(request.headers['Context-Id'])
	#http://www.brighton-boxes.co.uk/wp-content/uploads/2014/04/cardboard-box-30139.jpg
    try:
        post = Merchant.objects.get({'_id': merchant_id})
    except Merchant.DoesNotExist:
        return jsonify({'message': error_msg}),404
   
    product_post = Product(request.json['name'],request.json['price'], request.json['image'], merchant_id).save()
    
    product_out = {
        'name': request.json['name'],
        'price': request.json['price'],
        'image': request.json['image'],
		'merchant_id': request.headers['Context-Id']
    }
        
    return jsonify(product_out), 201

@app.route('/clients', methods=['POST'])
def create_client():
   
    error_msg = {'field':'name' ,'message':'Already exist'}
    for post_c in Client.objects.raw({'name': request.json['name']}):
        return jsonify(error_msg),400
   
    client_post = Client(request.json['name'],request.json['email']).save()
		#https://image.flaticon.com/icons/svg/3/3729.svg
    
    client_out = {
        'name': request.json['name'],
        'email': request.json['email']
    }
	
    return jsonify(client_out), 201
		
@app.route('/clients/purchases', methods=['POST'])
def create_client_purchases():
    
    date = datetime.datetime.now()
    client_id = ObjectId(request.headers['Context-Id'])
    product_id = ObjectId(request.json['product_id'])
    error_msg_client = {'error':'Invalid Client Id'}
    error_msg_product = {"field":"product_id", 'message':'Product does not exist'}
	
    try:
        post_chk_client = Client.objects.get({'_id': client_id})
    except Client.DoesNotExist:
        return jsonify({'message': error_msg_client}),404
	
    try:
        post_chk_product = Product.objects.get({'_id': product_id})
    except Product.DoesNotExist:
        return jsonify(error_msg_product),404
	
	
    purchase_post = Purchase(client_id,product_id,date).save()
    purchase_out = {
        'client_id': request.headers['Context-Id'],
        'product_id': request.json['product_id'],
        'purchase_datetime': date
    }
	
    return jsonify(purchase_out), 201
	
@app.route('/clients/promos', methods=['POST'])
def create_client_promos():
    
    date = datetime.datetime.now()
    client_id = ObjectId(request.headers['Context-Id'])
    promo_id = ObjectId(request.json['promo_id'])
    error_msg_client = {'error':'Invalid Client Id'}
    error_msg_promo = {"field":"promo_id", 'message':'Promo does not exist'}
    error_msg_promo_expired = {'error':'Promo is expired.'}
    error_msg_promo_status = {"field":"status", 'message':'Status invalid'}
	
    try:
        post_chk_client = Client.objects.get({'_id': client_id})
    except Client.DoesNotExist:
        return jsonify({'message': error_msg_client}),404
	
    try:
        post_chk_promo = Promo.objects.get({'_id': promo_id})
    except Promo.DoesNotExist:
        return jsonify(error_msg_promo),404
	
    if(request.json['status'] == 'availed' or request.json['status'] == 'redeemed'):
        if(request.json['status'] == 'redeemed' and date > post_chk_promo.end_date):
            return jsonify({'message': error_msg_promo_expired}),400
        else:
		    purchase_post = PromoPurchase(client_id,promo_id,date,request.json['status']).save()
    else:
        return jsonify({'message': error_msg_promo_status}),400
    
    purchase_out = {
        'client_id': request.headers['Context-Id'],
        'promo_id': request.json['promo_id'],
		'status': request.json['status'],
        'datetime': date
    }
	
    return jsonify(purchase_out), 201
	
@app.route('/promos', methods=['POST'])
def create_promo():
    
    error_msg = {'error':'You must be a Merchant to add a promo'}
    merchant_id = ObjectId(request.headers['Context-Id'])
	#https://as2.ftcdn.net/jpg/00/31/77/31/500_F_31773113_hhEFhwFVn6EsplC02GNKnO6HU0zkcRLA.jpg
    try:
        post = Merchant.objects.get({'_id': merchant_id})
    except Merchant.DoesNotExist:
        return jsonify({'message': error_msg}),404
	
    promo_post = Promo(request.json['name'],request.json['image'], request.json['start_date'], request.json['end_date']).save()
    promo_out = {
        'name': request.json['name'],
        'image': request.json['image'],
        'start_date': request.json['start_date'],
		'end_date':request.json['end_date']
    }
	
    return jsonify(promo_out), 201
		
@app.route('/promos', methods=['GET'])
def get_promos():
    date = datetime.datetime.now()
    promo_list = []
    for post_p in Promo.objects.all():
        if(post_p.start_date <= date and date <= post_p.end_date ):
            promo_list.append({'name': post_p.name,'image': post_p.image,'start_date': post_p.start_date,'end_date': post_p.end_date})
    return jsonify(promo_list), 200
	
		
if __name__ == '__main__':
    app.run(debug=True)