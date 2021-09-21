import redis
from django.conf import settings
from .models import Product

# connecting to redis
q = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender(object):
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def product_bought(self, products):
        products_ids = [p.id for p in products]
        for products_id in products_ids:
            for with_id in products_ids:
                # get the other products bought with each product
                if products_id != with_id:
                    # increment score for product purchased together
                    q.zincrby(self.get_product_key(products_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only one product
            suggestions = q.zrange(self.get_product_key(product_ids[0]), 0, -1,
                                   desc=True)[:max_results]
        else:
            # generate a temp key
            flat_ids = ''.join([str(id) for id in product_ids])
            temp_key = f'temp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            key = [self.get_product_key(id) for id in product_ids]
            q.zunionstore(temp_key, key)
            # remove ids for the products the recommendation is for
            q.zrem(temp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = q.zrange(temp_key, 0, -1,
                                   desc=True)[:max_results]
            # remove the temporary key
            q.delete(temp_key)
        suggested_product_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_product = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_product.sort(key=lambda y: suggested_product_ids.index(y.id))
        return suggested_product

    def clear_purchaces(self):
        for id in Product.objects.values_list('id', flat=True):
            q.delete(self.get_product_key(id))
