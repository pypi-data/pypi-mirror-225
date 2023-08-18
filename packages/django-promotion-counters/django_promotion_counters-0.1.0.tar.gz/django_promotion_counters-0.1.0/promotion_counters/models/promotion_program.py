from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import uuid7


class PromotionProgram(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
    )
    title = models.CharField(
        _('Title'),
        max_length=255,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
    )
    start_at = models.DateTimeField(
        _('Start date'),
        blank=True,
    )
    end_at = models.DateTimeField(
        _('End date'),
        null=True,
        blank=True,
    )
    target_action = models.CharField(
        _('Target action'),
        max_length=255,
    )
    target_value = models.IntegerField(
        _('Target value'),
        default=1,
        validators=[MinValueValidator(1)],
    )
    achievement_callback = models.CharField(
        _('Achievement callback'),
        max_length=255,
    )
    archived = models.BooleanField(
        _('Archived'),
        default=False,
    )
    enabled = models.BooleanField(
        _('Enabled'),
        default=True,
    )
    repeatable = models.BooleanField(
        _('Repeatable'),
        default=False,
        help_text=_('If enabled, the achievement counter will be recreated after the achievement is reached.'),
    )

    class Meta:
        verbose_name = _('Promotion program')
        verbose_name_plural = _('Promotion programs')
        ordering = ('-created_at',)
        db_table = 'promotion_program'

    def __str__(self):
        return self.title
