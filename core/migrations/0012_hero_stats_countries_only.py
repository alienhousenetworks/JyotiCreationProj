from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_remove_product_moq"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="herosection",
            name="stats_years",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="stats_retailers",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="stats_variants",
        ),
        migrations.AlterField(
            model_name="herosection",
            name="stats_countries",
            field=models.CharField(
                default="42",
                help_text="Number of countries shown in the hero stats",
                max_length=50,
            ),
        ),
    ]
