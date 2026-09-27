from django.db import migrations


def seed_demo_products(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    Product.objects.using(schema_editor.connection.alias).bulk_create(
        [Product(name=f"Product {letter}") for letter in "ABCDEF"]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_demo_products, migrations.RunPython.noop),
    ]
