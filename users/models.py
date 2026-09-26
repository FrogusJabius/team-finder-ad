import io
import random
from enum import StrEnum

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from users.managers import UserManager

from team_finder.constants import (ABOUT_MAX_LENGTH, AVATAR_COLORS,
                                   AVATAR_FONT_PATH, AVATAR_FONT_SIZE,
                                   AVATAR_SIZE, AVATAR_TEXT_COLOR,
                                   NAME_MAX_LENGTH, PHONE_MAX_LENGTH)


class AvatarColor(StrEnum):
    BLUE = '#5B8DEF'
    ORANGE = '#E8A838'
    GREEN = '#6BCB77'
    PURPLE = '#9B5DE5'
    PINK = '#F15BB5'
    CYAN = '#00BBF9'
    RED = '#FF6B6B'
    TEAL = '#4ECDC4'


AVATAR_COLORS = list(AvatarColor)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    surname = models.CharField(max_length=NAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH, blank=True, default='')
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=ABOUT_MAX_LENGTH, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self.avatar = self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        color = random.choice(AVATAR_COLORS)
        letter = self.name[0].upper() if self.name else '?'

        img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color=color)
        draw = ImageDraw.Draw(img)

        target_size = int(AVATAR_SIZE * 0.6)
        font = None

        try:
            font_size = AVATAR_FONT_SIZE
            font = ImageFont.truetype(AVATAR_FONT_PATH, font_size)
            # Корректируем размер под целевой
            bbox = draw.textbbox((0, 0), letter, font=font)
            actual_size = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
            if actual_size > 0:
                font_size = int(font_size * target_size / actual_size)
                font = ImageFont.truetype(AVATAR_FONT_PATH, font_size)
        except Exception:
            font = ImageFont.load_default(size=target_size)

        bbox = draw.textbbox((0, 0), letter, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (AVATAR_SIZE - text_w) / 2 - bbox[0]
        y = (AVATAR_SIZE - text_h) / 2 - bbox[1]
        draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        filename = f'avatar_{self.email.split("@")[0]}.png'
        return ContentFile(buffer.getvalue(), name=filename)
