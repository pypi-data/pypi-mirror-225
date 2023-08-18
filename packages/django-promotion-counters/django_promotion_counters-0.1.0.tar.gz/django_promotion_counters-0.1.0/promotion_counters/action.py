import logging
from typing import Callable

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

User = get_user_model()


class ActionRegistry(dict):
    def register_action(self, action) -> None:
        self[action.alias] = action

    def get_choices(self):
        return [(alias, action.verbose_name)
                for alias, action in self.items()]


class RewardRegistry(dict):
    def register_callback(self, callback: Callable) -> None:
        self[self._get_qual_name(callback)] = callback

    @staticmethod
    def _get_qual_name(callback: Callable) -> str:
        return f'{callback.__module__}.{callback.__qualname__}'

    def get_callback(self, alias: str) -> Callable:
        return self[alias]

    def get_choices(self):
        return [
            (alias, callback.verbose_name)
            for alias, callback in self.items()
        ]

    def resolve_callback(self, achievement_callback: str) -> Callable:
        return self[achievement_callback]


action_registry = ActionRegistry()
reward_registry = RewardRegistry()


class Action:
    def __init__(self, alias: str, verbose_name: str, *args, **kwargs):
        self.alias = alias
        self.verbose_name = verbose_name
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def send(self, user: User):
        # Find active programs for this action
        active_programs_ids = PromotionProgram.objects.filter(
            Q(enabled=True) & Q(archived=False) &
            Q(start_at__lte=timezone.now()) & (
                    Q(end_at__gte=timezone.now()) | Q(end_at__isnull=True)
            )
        ).filter(
            target_action=self.alias,
        ).values_list('id', flat=True)

        # Find not achieved counters for specified user and filtered programs from previous step
        active_user_achievement_counters = AchievementCounter.objects.filter(
            promotion_program_id__in=active_programs_ids,
            user=user,
            achieved_at=None,
        )

        # Create counters for active programs if not exists
        programs_counters_to_create = active_programs_ids.difference(
            active_user_achievement_counters.values_list('promotion_program_id', flat=True)
        )
        AchievementCounter.objects.bulk_create([
            AchievementCounter(
                user=user,
                promotion_program_id=program_id,
            )
            for program_id in programs_counters_to_create
        ])

        # Increment counters for active programs
        active_user_achievement_counters.select_for_update().update(
            counter=models.F('counter') + 1,
            last_incremented_at=timezone.now(),
        )

        # Find achieved counters for specified user and filtered programs from previous step
        achieved_counter = AchievementCounter.objects.annotate(
            target_value=models.F('promotion_program__target_value'),
        ).filter(
            promotion_program_id__in=active_programs_ids,
            user=user,
            counter__gte=models.F('target_value'),
            achieved_at=None,
        ).select_related(
            'promotion_program'
        ).select_for_update()

        # Call achievement callback for achieved counters
        for counter in achieved_counter:
            achieve_callback = reward_registry.resolve_callback(
                counter.promotion_program.achievement_callback
            )
            try:
                achieve_callback(counter)
            except Exception as ex:
                logging.exception(ex)

            counter.achieved_at = timezone.now()
            counter.save()

        # Recreate counter for active programs if it is repeatable
        AchievementCounter.objects.bulk_create([
            AchievementCounter(
                user=user,
                promotion_program_id=counter.promotion_program_id,
            )
            for counter in achieved_counter
            if counter.promotion_program.repeatable
        ])
