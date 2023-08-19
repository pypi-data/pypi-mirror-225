from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from promotion_counters.models.utils import uuid7

User = get_user_model()


class AchievementCounter(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    counter = models.IntegerField(
        _('Counter'),
        default=0,
        validators=[MinValueValidator(0)],
    )
    promotion_program = models.ForeignKey(
        'PromotionProgram',
        verbose_name=_('Promotion program'),
        on_delete=models.RESTRICT,
    )
    started_at = models.DateTimeField(
        _('Started at'),
        auto_now_add=True,
    )
    last_incremented_at = models.DateTimeField(
        _('Last incremented at'),
        default=now,
    )
    achieved_at = models.DateTimeField(
        _('Achieved at'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Achievement counter')
        verbose_name_plural = _('Achievement counters')
        ordering = ('-id',)
        db_table = 'achievement_counter'
        constraints = [
            models.UniqueConstraint(
                name='unique_unfinished_counter_for_program',
                fields=['user', 'promotion_program'],
                condition=models.Q(achieved_at__isnull=True),
            ),
            models.CheckConstraint(
                name='counter_gte_zero',
                check=models.Q(counter__gte=0),
            )
        ]

    def __str__(self):
        return f"{self.promotion_program.title} - {self.user.email}: {self.counter}"
