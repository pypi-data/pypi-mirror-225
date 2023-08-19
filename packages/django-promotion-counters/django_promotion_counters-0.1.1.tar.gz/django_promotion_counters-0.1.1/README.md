=====
Promotion Counters
=====

Django app to handle promotion and marketing
events based on it's counting and process such counters as achievements.

Quick start
-----------

1. Add "promotion_counters" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "promotion_counters",
    ]


3. Run ``python manage.py migrate`` to create
the promotion program and promotion counter models.

4. Define your promotion action like this::

    registration = Action(
        alias='registration',
        verbose_name='Регистрация по ссылке',
    )

5. Define your achievement handler like this::

    @on_achievement(action='Issue promo code')
    def registration_handler(counter: Counter):
        PromoCode.objects.create(
            user=counter.user,
            code=generate_promo_code(),
            type=PromoCode.DISCOUNT,
            value=10,
        )

6. Create promotion program using promotion action and achievement handler in admin panel.