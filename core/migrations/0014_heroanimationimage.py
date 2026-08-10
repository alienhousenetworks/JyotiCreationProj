from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_hero_stats_restore_without_countries"),
    ]

    operations = [
        migrations.CreateModel(
            name="HeroAnimationImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Upload a portrait image for the hero animation",
                        upload_to="hero_animation/",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Uncheck to hide this slide from the hero animation",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Lower numbers appear first",
                    ),
                ),
            ],
            options={
                "verbose_name": "01b. Hero Animation Image",
                "verbose_name_plural": "01b. Hero Animation Images",
                "ordering": ["order", "id"],
            },
        ),
    ]
