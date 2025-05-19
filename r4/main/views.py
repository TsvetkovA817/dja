from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Product, Review
from main.serializers import ReviewSerializer, ProductListSerializer, ProductDetailsSerializer

# http://127.0.0.1:8000/products/
@api_view(['GET'])
def products_list_view(request):
    # Получаем все товары
    products = Product.objects.all()
    # результат
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

# http://127.0.0.1:8000/products/2/
class ProductDetailsView(APIView):
    def get(self, request, product_id):
        # Получаем товар по ид или 404
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data)


# доп :
# http://127.0.0.1:8000/products/reviews/2/
# http://127.0.0.1:8000/products/reviews/2/?mark=4
class ProductFilteredReviews(APIView):
    def get(self, request, product_id):
        # Получаем товар по ид или 404
        product = get_object_or_404(Product, id=product_id)

        # Получаем параметр mark из урл запроса
        mark = request.query_params.get('mark')
        # получаем отзывы на товар
        reviews = Review.objects.filter(product=product)

        # Если передана оценка в параметре mark, фильтр по оценке
        if mark is not None:
            try:
                mark = int(mark)
                # перечисление в модели MARK_CHOICES
                if mark < 1 or mark > 5:
                    return Response(
                        {"error": "bad mark, значение от 1 до 5"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                reviews = reviews.filter(mark=mark)
            except ValueError:
                return Response(
                    {"error": "оценка должна быть числом от 1 до 5"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # возвращаем результат
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
