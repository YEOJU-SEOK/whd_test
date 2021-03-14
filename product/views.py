import json
#상품기능의 경우 관리자만 접근가능해야함
#RDF수정예정

from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta
from user.models import User
from .models import Product


class ProductView(View):
    #상품조회
    def get(self, request):
        products = Product.objects.all().order_by('expiration_date')

        if not products.exists():
            return JsonResponse({"mesage":"PRODUCT_NOT_FOUND"}, status=404)
        results = [{
            'id' : product.id,
            'name' : product.name,
            'manufacture' : product.manufacture,
            'unit_price' : product.unit_price,
            'stock' : product.stock,
            'expiration_date' : product.expiration_date
        } for product in products]
        return JsonResponse({'message':'SUCCESS', 'results': results}, status=200)

    #상품추가
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        expiration_date = data.get('expiration_date', datetime.today() + timedelta(7))
        print(expiration_date)
        
        try:
            ##샹품이 이미 존재
            if Product.objects.filter(name=data['name']).exists():
                #중복update로직
                return JsonResponse({"message":"PRODUCT_EXISTS"}, status=401)

            else:                
                Product.objects.create(
                    name = data['name'],
                    manufacture = data['manufacture'],
                    unit_price = data['unit_price'],
                    stock = data['stock'],
                    expiration_date = expiration_date
                )
              
                return JsonResponse({"message":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

#상품 업데이트
class ProductUpdateView(View):
    def patch(self, request, product_id):
        data = json.loads(request.body)
        
        try:
            if Product.objects.filter(id=product_id):
                product = Product.objects.get(id=product_id)

                product.manufacture = data.get('manufacture', product.manufacture)
                product.unit_price = data.get('unit_price', product.unit_price)
                product.stock = data.get('stock', product.stock)

                product.save()

                return JsonResponse({"message" : "SUCCESS"}, status=201)

            return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)       

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)  

#상품 삭제
class ProductDeleteView(View):       
    def delete(self, request, product_id):
        try:
            if Product.objects.filter(id=product_id).exists():
                
                Product.objects.filter(id=product_id).delete()

                return JsonResponse({"message" : "SUCCESS"},status=200)

            return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)  
