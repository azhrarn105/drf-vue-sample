from django.test import TestCase
from django.utils.timezone import localtime

from shop.models import Book
from apiv1.serializers import BookSerializer


class TestBookSerializer(TestCase):
    """BookSerializer のテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（正常系）"""
        input_data = {
            'title': 'aaa',
            'price': 111,
        }
        serializer = BookSerializer(data=input_data)
        # 入力したデータがvalidationを通ったことの確認
        self.assertEqual(serializer.is_valid(), True)
    
    def test_inputinvalid_if_title_is_brank(self):
        """入力データのバリデーション（異常系：titleが空）"""
        input_data = {
            'title': '',
            'price': 111,
        }
        serializer = BookSerializer(data=input_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['title'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['title']],
            ['blank'],
        )

