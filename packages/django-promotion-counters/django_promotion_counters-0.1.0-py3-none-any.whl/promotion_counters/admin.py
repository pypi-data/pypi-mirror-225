from django import forms
from django.contrib import admin


# Register your models here.
class PromotionProgramForm(forms.ModelForm):
    target_action = forms.ChoiceField(choices=[])
    achievement_callback = forms.ChoiceField(choices=[])

    class Meta:
        model = PromotionProgram
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_action'].choices = action_registry.get_choices()
        self.fields['achievement_callback'].choices = reward_registry.get_choices()


@admin.register(PromotionProgram)
class PromotionProgramAdmin(admin.ModelAdmin):
    form = PromotionProgramForm
    list_display = (
        'title',
        'start_at', 'end_at',
        'target_value',
        'enabled', 'repeatable',
        'target_action', 'achievement_callback',
        'archived'
    )
    list_filter = ('target_action', 'achievement_callback', 'archived')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)


@admin.register(AchievementCounter)
class AchievementCounterAdmin(admin.ModelAdmin):
    list_display = ('user', 'promotion_program', 'counter', 'started_at', 'last_incremented_at', 'achieved_at')
    list_filter = ('promotion_program',)
    search_fields = ('user__email', 'promotion_program__title')
    readonly_fields = ('started_at', 'last_incremented_at', 'achieved_at')
