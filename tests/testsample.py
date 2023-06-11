from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from accounts.admin import UserAdmin
from accounts.models import User
from charities.models import Benefactor, Charity, Task


class AccountsAppTest(TestCase):
    def setUp(self):
        self.extra_info = {
            'phone': '09369871234',
            'address': 'Tehran',
            'gender': 'M',
            'age': 28,
            'description': 'lorem ipsum description',
        }
        self.base_user_data = {
            'username': 'Mohammad_Jafari',
            'password': 'my_strong_password',
        }

    def test_valid_user1(self):
        try:
            u = User(**self.base_user_data)
            self.assertIsNone(u.full_clean(), '\nبرای مدل User فیلدهای username و password را به‌درستی تعریف نکرده‌اید.')
        except TypeError:
            raise self.fail('user with only username & password should be valid')

    def test_not_valid_gender(self):
        self.extra_info.update(gender='G')
        u = User(**self.base_user_data, **self.extra_info)
        with self.assertRaises(ValidationError):
            u.full_clean()
            u.save()


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Mohammad', password='9')
        cls.benefactor = Benefactor.objects.create(user=cls.user)
        cls.charity = Charity.objects.create(user=cls.user, name='charity', reg_number='5678901234')

    def setUp(self):
        self.task_info = {
            'title': 'charity title',
            'charity': self.charity,
            'age_limit_to': 45,
            'gender_limit': 'F',
        }

    def test_valid_task(self):
        task = Task.objects.create(**self.task_info)
        task.refresh_from_db()
        self.assertIsNone(task.assigned_benefactor, '\nبرای فیلد assigned_benefactor مقدار null را برابر True قرار نداده‌اید.')



class UserAdminTest(TestCase):
    def test_credentials_section(self):
        title = UserAdmin.fieldsets[0][0]
        self.assertIsNone(title)
        fields = list(UserAdmin.fieldsets[0][1].get('fields'))
        expected_fields = ['username', 'password']
        self.assertListEqual(fields, expected_fields)



class AboutUsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_works_fine(self):
        response = self.client.get('/about-us/')
        self.assertEqual(200, response.status_code, '\nدرخواست مورد نظر به درستی ارسال نمی‌شود و پاسخ درستی را دریافت نمی‌کند.')
        self.assertContains(response, "نیکوکاران و اعضای خیریه‌ها", msg_prefix='\nصفحه‌ی about_us.html باید شامل عبارت "نیکوکاران و اعضای خیریه‌ها" باشد.')
