from django.conf import settings


class MovieSession(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            # 세션에 없던 키 값을 생성하면 자동 저장
            cart = self.session[settings.CART_ID] = {}
            # 세션에 이미 있는 키 값에 대한 값을 수정하면 수동으로 저장
        self.cart = cart

    # 추가, 삭제, 비우기

    def __len__(self):
        # 요소가 몇개인지 갯수를 반환해주는 함수
        """
        id : 실제제품
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        # for문 같은 문법을 사용할 때 안에 있는 요소를 어떤 형태로 반환할 것인지 결정하는 함수
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            # 만약 제품 정보가 Decimal 이라면 세션에 저장할 때는 str로 형변환 해서 저장하고
            # 꺼내올 때는 Decimal로 형변환해서 사용해야 한다.
            self.cart[product_id] = {'quantity': 0, 'price': product.price}
        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del (self.cart[product_id])
        self.save()

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def clear(self):
        self.cart = {}
        self.save()

    # 전체 제품 가격
    def get_total_price(self):
        return sum(item['quantity'] * item['price'] for item in self.cart.values())

    # 할인된 가격
    # 전체 제품 가격 - 할인된 가격 = 최종가격
