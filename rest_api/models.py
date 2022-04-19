from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userProfile")
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    status = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.user.username} : {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Message(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='текст сообщения')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def get_user(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.content


class Post(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, on_delete=models.CASCADE, related_name= 'posts')
    content = models.TextField(verbose_name='текст сообщения')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def created_at(self):
        return format(self.created.strftime('%H:%M:%S %d.%m.%Y'))

    def get_user(self):
        return f'{self.user.user.first_name} {self.user.user.last_name}'

    def __str__(self):
        return self.content



# # подписка\отписка пользователя 
# class Followers(models.Model):
#     user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
#     another_user = models.ManyToManyField(UserProfile, related_name='another_user')

#     def __str__(self):
#         return self.user.user.first_name