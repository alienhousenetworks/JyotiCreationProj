from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_page_section_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="moq",
        ),
        migrations.AlterField(
            model_name="b2benquirycta",
            name="guarantees",
            field=models.TextField(
                default="Response within 4 hours\nDedicated account manager\nFree sample packs\nGlobal shipping included",
                help_text="One guarantee per line",
            ),
        ),
    ]
