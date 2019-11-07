from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Book


class TestBookCreateAPIView(APITestCase):
    TARGET_URL = '/api/v1/books/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='user@example.com',
            password='secret',
        )

    def test_create_success(self):
        """本モデルの登録APIへのPOSTリクエスト（正常系）"""
        # ログイン処理（JWT）
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # 作成するユーザーデータを定義
        params = {
            'title': 'aaaa',
            'price': 111,
        }
        # 定義したデータをpost（データの登録）
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証（作ったデータが1件登録されていることの確認）
        self.assertEqual(Book.objects.count(), 1)
        # レスポンスの内容を検証（APIレスポンスのステータスがCREATED（201）であることを確認）
        self.assertEqual(response.status_code, 201)
        book = Book.objects.get()
        expected_json_dict = {
            'id': str(book.id),
            'title': book.title,
            'price': book.price,
            'created_at': str(localtime(book.created_at)).replace(' ', 'T'),
        }
        # DBに登録されたデータと、APIのレスポンスjsonが同等であることの確認
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_unauthorized(self):
        """本モデルの登録APIへのPOSTリクエスト（異常系：認証エラー）"""
        # 作成するユーザーデータを定義
        params = {
            'title': 'aaaa',
            'price': 111,
        }
        # 定義したデータをpost（データの登録）
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証（データが登録されていないことの確認）
        self.assertEqual(Book.objects.count(), 0)
        # レスポンスの内容を検証（APIレスポンスのステータスがUNAUTHORIZED（401）であることを確認）
        self.assertEqual(response.status_code, 401)

    def test_create_bad_request(self):
        """本モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG）"""
        # ログイン処理（JWT）
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # 作成するユーザーデータを定義
        params = {
            'title': '',
            'price': 111,
        }
        # 定義したデータをpost（データの登録）
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証（データが登録されていないことの確認）
        self.assertEqual(Book.objects.count(), 0)
        # レスポンスの内容を検証（APIレスポンスのステータスがBAD_REQUEST（400）であることを確認）
        self.assertEqual(response.status_code, 400)

