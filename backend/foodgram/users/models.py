from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram.settings import MAX_LENGTH_EMAIL, MAX_LENGTH_CHARFIELD


class User(AbstractUser):
    email = models.EmailField(max_length=MAX_LENGTH_EMAIL, unique=True,
                              blank=False, null=False, verbose_name='email')
    username = models.CharField(max_length=MAX_LENGTH_CHARFIELD, unique=True,
                                blank=False, null=False,
                                verbose_name='username')
    first_name = models.CharField(max_length=MAX_LENGTH_CHARFIELD, blank=False,
                                  null=False, verbose_name='first_name')
    last_name = models.CharField(max_length=MAX_LENGTH_CHARFIELD, blank=False,
                                 null=False, verbose_name='last_name')
    password = models.CharField(max_length=MAX_LENGTH_CHARFIELD, blank=False,
                                null=False, verbose_name='password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        default_related_name = 'user'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор(на когоподписаны)',
        related_name='following')
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик/Юзер(кто подписан)',
        related_name='follower')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('following',)
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'],
                name='unique subs'),
            models.CheckConstraint(
                name="non selfsubcribtion",
                check=~models.Q(following=models.F("follower")))]

    def __str__(self):
        return (f'{self.follower.username} подписан'
                f'на {self.following.username}')
