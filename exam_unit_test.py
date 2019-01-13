# Copyright 2016 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
from unittest import SkipTest
from exam_models import Merchant, Product, Client, Purchase, Promo, PromoPurchase

from pymodm import MongoModel, CharField, IntegerField
from pymodm.errors import InvalidModel, ValidationError


class BasicModelTestCase(unittest.TestCase):

    def test_model_insertions(self):
       # Merchant Model
        msg = 'Got 4 arguments for only 3 fields'
        with self.assertRaisesRegex(ValueError, msg):
            Merchant('Mario', 'testing only', 'image/link', 'excess')
        msg = 'Unrecognized field name'
        with self.assertRaisesRegex(ValueError, msg):
            Merchant(first_name='Paul')
        msg = 'name specified more than once in constructor for User'
        with self.assertRaisesRegex(ValueError, msg):
            Merchant('Paul', name='Allen')
		
        # Product Model
        msg = 'Got 5 arguments for only 4 fields'
        with self.assertRaisesRegex(ValueError, msg):
            Product('Mario', 2323, 'image/link', '234qweqe32','excess')
        msg = 'Unrecognized field name'
        with self.assertRaisesRegex(ValueError, msg):
            Product(first_name='Paul')
        msg = 'name specified more than once in constructor for User'
        with self.assertRaisesRegex(ValueError, msg):
            Product('Paul', name='Allen')
		
        # Client Model
        msg = 'Got 3 arguments for only 2 fields'
        with self.assertRaisesRegex(ValueError, msg):
            Client('Mario', 'test@gmail.com', 'excess')
        msg = 'Unrecognized field name'
        with self.assertRaisesRegex(ValueError, msg):
            Client(first_name='Paul')
        msg = 'name specified more than once in constructor for User'
        with self.assertRaisesRegex(ValueError, msg):
            Client('Paul', name='Allen')
		
		
        # Purchase Model
        msg = 'Got 4 arguments for only 3 fields'
        with self.assertRaisesRegex(ValueError, msg):
            Purchase('234sdewr', '345srfsdf', '2019-01-14 01:23:55', 'excess')
        msg = 'Unrecognized field name'
        with self.assertRaisesRegex(ValueError, msg):
            Purchase(first_name='client12312')
        msg = 'client_id specified more than once in constructor for User'
        with self.assertRaisesRegex(ValueError, msg):
            Purchase('client12312', client_id='client12312')
			
        # Promo Model
        msg = 'Got 5 arguments for only 4 fields'
        with self.assertRaisesRegex(ValueError, msg):
            Promo('234sdewr', 'image/link','2019-01-14 01:23:55', '2019-01-14 01:23:55', 'excess')
        msg = 'Unrecognized field name'
        with self.assertRaisesRegex(ValueError, msg):
            Promo(first_name='Paul')
        msg = 'name specified more than once in constructor for User'
        with self.assertRaisesRegex(ValueError, msg):
            Promo('Paul', name='Allen')
	
        # PromoPurchase Model
        msg = 'Got 5 arguments for only 4 fields'
        with self.assertRaisesRegex(ValueError, msg):
            PromoPurchase('234sdewr', '345srfsdf', '2019-01-14 01:23:55', 'availed', 'excess')
        msg = 'Unrecognized field name'
        with self.assertRaisesRegex(ValueError, msg):
            PromoPurchase(first_name='234sdewr')
        msg = 'name specified more than once in constructor for User'
        with self.assertRaisesRegex(ValueError, msg):
            PromoPurchase('234sdewr', client_id='234sdewr')

