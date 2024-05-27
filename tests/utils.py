from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status

def make_simple_test(model_class, url, creation_attrs):
    class ViewSetTest(TestCase):
        def setUp(self):
            self.client = APIClient()

            #setup superuser
            self.superuser = User.objects.create_user(
                username='superuser', password='superuser', is_superuser=True,
            )
            self.superuser_token = Token.objects.create(user=self.superuser)

            #setup user
            self.data = {
                'username': 'testuser3',
                'email': 'testuser@example.com',
                'password': 'testpassword'
            }
            self.client.post('/rest/user/', self.data)
            self.user_token = self.client.post('/api-token-auth/', self.data).data['token']
            self.user = Token.objects.get(key=self.user_token).user

        def manage(self, user: User, token: Token, post_status: int, put_status: int, delete_status: int):
            self.client.force_authenticate(user=user, token=token)

            created_id = model_class.objects.create(**creation_attrs).id

            # POST
            response = self.client.post(url, creation_attrs) 
            self.assertEqual(response.status_code, post_status)

            object_url = f'{url}{created_id}/'

            # PUT
            response = self.client.put(object_url, creation_attrs)
            self.assertEqual(response.status_code, put_status)

            # DELETE
            response = self.client.delete(object_url)
            self.assertEqual(response.status_code, delete_status)

        def test_manage_user(self):
            self.manage(
                self.user, self.user_token,
                post_status=status.HTTP_403_FORBIDDEN,
                put_status=status.HTTP_403_FORBIDDEN,
                delete_status=status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            self.manage(
                self.superuser, self.superuser_token,
                post_status=status.HTTP_201_CREATED,
                put_status=status.HTTP_200_OK,
                delete_status=status.HTTP_204_NO_CONTENT,
            )


    return ViewSetTest

class WithAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        #setup superuser
        self.superuser = User.objects.create_user(
            username='superuser', password='superuser', is_superuser=True,
        )
        self.superuser_token = Token.objects.create(user=self.superuser)

        #setup user
        self.data = {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        self.client.post('/rest/user/', self.data)
        self.user_token = self.client.post('/api-token-auth/', self.data).data['token']
        self.user = Token.objects.get(key=self.user_token).user

def to_hyperlink(id, prefix: str):
    return f'/rest/{prefix}/{id}/'