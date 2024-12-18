from product.models import OrderProduct, Order


class OrderTotalSum:

    def __init__(self, order: Order, total_sum: float):
       self.order = order 
       self.total_sum = total_sum

    def __check_if_object_is_part_of_class(self, obj):
         return isinstance(obj, OrderTotalSum):
        
    
    def __eq__(self, obj):
       is_part = self.__check_if_object_is_part_of_class(obj)
       return is_part and (self.total_sum == obj.total_sum)
    
    def __lt__(self, obj):
        is_part = self.__check_if_object_is_part_of_class(obj)
        return is_part and (self.total_sum < obj.total_sum)

    def __gt__(self, obj):
        is_part = self.__check_if_object_is_part_of_class(obj)
        return is_part and (self.total_sum > obj.total_sum)

