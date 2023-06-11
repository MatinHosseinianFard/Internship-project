from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from accounts.admin import UserAdmin
from accounts.models import *
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


class TestAll(TestCase):
    def setUp(self):
        self.client = Client()
        user = {"username": "Saeid",
                "password": "1q*b12$z",
                "phone": "09133333333",
                "address": "Iran-Tehran",
                "gender": "M",
                "age": "21",
                "description": "This is a test.",
                "first_name": "Saeid",
                "last_name": "Saeidi",
                "email": "Saeid12345@gmail.com"}
        self.user = User.objects.create(**user)
        self.user_2 = User.objects.create(**{**user, "username": "Ali"})
        self.user_3 = User.objects.create(**{**user, "username": "Mohammad"})
        self.user_4 = User.objects.create(**{**user, "username": "Sajjad"})
        
        self.charity = Charity.objects.create(user=self.user, name='charity1', reg_number='1234567891')
        self.charity_2 = Charity.objects.create(user=self.user_2, name='charity2', reg_number='1234567892')
        self.charity_3 = Charity.objects.create(user=self.user_3, name='charity3', reg_number='1234567893')
        self.charity_4 = Charity.objects.create(user=self.user_4, name='charity4', reg_number='1234567894')
        
        self.benefactor = Benefactor.objects.create(user=self.user)
        self.benefactor_2 = Benefactor.objects.create(user=self.user_2)
        self.benefactor_3 = Benefactor.objects.create(user=self.user_3)
        self.benefactor_4 = Benefactor.objects.create(user=self.user_4)
        
        Task.objects.create(title='task1', state='A', charity=self.charity)
        Task.objects.create(title='task2', state='A', charity=self.charity)
        Task.objects.create(title='task3', state='P', charity=self.charity_2, assigned_benefactor=self.benefactor)
        Task.objects.create(title='task4', state='A', charity=self.charity_2, assigned_benefactor=self.benefactor_2)
        Task.objects.create(title='task5', state='A', charity=self.charity_3)
        Task.objects.create(title='task6', state='A', charity=self.charity_3, assigned_benefactor=self.benefactor_2)
        Task.objects.create(title='task7', state='P', charity=self.charity_3, assigned_benefactor=self.benefactor_4)

    def test_related_tasks_to_charity_manager(self):
        objects = Task.objects.related_tasks_to_charity(user=self.user)
        self.assertEqual(objects.count(), 2, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان charity است را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.related_tasks_to_charity(user=self.user_2)
        self.assertEqual(objects.count(), 2, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان charity است را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.related_tasks_to_charity(user=self.user_3)
        self.assertEqual(objects.count(), 3, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان charity است را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.related_tasks_to_charity(user=self.user_4)
        self.assertEqual(objects.count(), 0, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان charity است را به درستی محاسبه نکرده‌اید.')

    def test_related_tasks_to_benefactor(self):
        task = Task.objects.first()
        task.assigned_benefactor = self.benefactor
        task.save()
        objects = Task.objects.related_tasks_to_benefactor(user=self.user)
        self.assertEqual(objects.count(), 2, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان benefactor است را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.related_tasks_to_benefactor(user=self.user_2)
        self.assertEqual(objects.count(), 2, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان benefactor است را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.related_tasks_to_benefactor(user=self.user_3)
        self.assertEqual(objects.count(), 0, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان benefactor است را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.related_tasks_to_benefactor(user=self.user_4)
        self.assertEqual(objects.count(), 1, '\nتعداد تسک‌هایی که کاربر مورد نظر به عنوان benefactor است را به درستی محاسبه نکرده‌اید.')

    def test_all_related_tasks_to_user(self):
        # task = Task.objects.first()
        # task.assigned_benefactor = self.benefactor
        # task.save()
        objects = Task.objects.all_related_tasks_to_user(user=self.user)
        self.assertEqual(objects.count(), 4, '\nتعداد تسک‌هایی که کاربر مورد نظر به هر طریقی به آن‌ها دسترسی دارد را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.all_related_tasks_to_user(user=self.user_2)
        self.assertEqual(objects.count(), 4, '\nتعداد تسک‌هایی که کاربر مورد نظر به هر طریقی به آن‌ها دسترسی دارد را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.all_related_tasks_to_user(user=self.user_3)
        self.assertEqual(objects.count(), 4, '\nتعداد تسک‌هایی که کاربر مورد نظر به هر طریقی به آن‌ها دسترسی دارد را به درستی محاسبه نکرده‌اید.')
        objects = Task.objects.all_related_tasks_to_user(user=self.user_4)
        self.assertEqual(objects.count(), 2, '\nتعداد تسک‌هایی که کاربر مورد نظر به هر طریقی به آن‌ها دسترسی دارد را به درستی محاسبه نکرده‌اید.')