from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_hero_stats_countries_only"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="stats_years",
            field=models.CharField(
                default="52+",
                help_text="Years heritage value shown in hero",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="stats_retailers",
            field=models.CharField(
                default="500+",
                help_text="Retail partners value shown in hero",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="stats_variants",
            field=models.CharField(
                default="12K+",
                help_text="Design variants value shown in hero",
                max_length=50,
            ),
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="stats_countries",
        ),
    ]
