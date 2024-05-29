import logging

from django.db import IntegrityError
from rest_framework import serializers

from utils.custom_exception import ErrorCode
from .exception import OrderException, ProductException, InsertTermContext
from .models import Product, Order, PaymentRecord
from .serializers import ProductSerializer, OrderSerializer, PaymentRecordSerializer
from ..user_center.models import ExternalUser
from .enum_config import OrderStatus, PaymentStatus, ProductStatus, PaymentMethod
from ..user_center.service import TermCourseService

logger = logging.getLogger(__name__)


class ProductService:
    def get_products(self):
        # 获取所有商品信息
        products = Product.objects.all()
        # 序列化商品信息
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def create_order(self, product_id, user_id, count=1):
        # 获取商品和用户信息
        try:
            product = Product.objects.get(id=product_id)
            if product.is_deleted or product.status != ProductStatus.OnSale.value[0]:
                logger.info(f"product: {product}")
                raise ProductException("商品不存在或者已下架", ErrorCode.ProductOff.value)
            user = ExternalUser.objects.get(id=user_id)
            total_amount = product.price * count
            # todo 添加期课学员；然后在支付成功入口生成期课内容表
            # 创建订单
            order = Order.objects.create(user=user, product=product, total_amount=total_amount,
                                         status=OrderStatus.PENDING.value)
            serializer = OrderSerializer(order)
            term_service = TermCourseService(user.id, product.course.id)
            term_service.insert_student_context()

            return serializer.data
        except Order.DoesNotExist:
            logger.error(f"订单不存在", ErrorCode.OrderNotExit.value)
            raise OrderException("订单不存在")
        except Product.DoesNotExist:
            raise ProductException("商品不存在", ErrorCode.ProductNotExit.value)
        except IntegrityError:
            raise OrderException('订单已存在，请无重复创建', ErrorCode.OrderDuplication.value)
        except InsertTermContext:
            return serializer.data
        except Exception as e:
            logger.exception(f'创建订单异常')
            raise e

    def create_payment_record(self, order_id, amount, payment_method=PaymentMethod.WECHAT.value):
        try:
            # 获取订单信息
            order = Order.objects.get(id=order_id)
            # 创建支付记录
            payment_record = PaymentRecord.objects.create(order=order, payment_method=payment_method, amount=amount,
                                                          status=PaymentStatus.PENDING.value)
            # 返回支付记录信息
            serializer = PaymentRecordSerializer(payment_record)
            # todo 调用 公众号下单
            return serializer.data
        except Order.DoesNotExist:
            raise OrderException('订单不存在', ErrorCode.OrderNotExit.value)
        except Exception as e:
            logger.exception('创建支付记录异常')
            raise e


class OrderService:
    def get_order(self, order_id):
        # 获取订单信息
        order = Order.objects.get(id=order_id)
        # 返回订单信息
        serializer = OrderSerializer(order)
        return serializer.data

    def update_order_status(self, order_id, status):
        # 获取订单信息
        order = Order.objects.get(id=order_id)
        # 更新订单状态
        order.status = status
        order.save()


class PaymentService:
    def get_payment_records(self):
        # 获取所有支付记录信息
        payment_records = PaymentRecord.objects.all()
        # 序列化支付记录信息
        serializer = PaymentRecordSerializer(payment_records, many=True)
        return serializer.data

    def create_payment_record(self, order_id, payment_method, amount):
        # 获取订单信息
        order = Order.objects.get(id=order_id)
        # 创建支付记录
        payment_record = PaymentRecord.objects.create(order=order, payment_method=payment_method, amount=amount)
        # 返回支付记录信息
        serializer = PaymentRecordSerializer(payment_record)
        return serializer.data


