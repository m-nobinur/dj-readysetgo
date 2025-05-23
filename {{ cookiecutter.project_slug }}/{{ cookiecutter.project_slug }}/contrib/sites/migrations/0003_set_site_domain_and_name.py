from django.conf import settings
from django.db import migrations
from django.db import connection


def _update_or_create_site_with_sequence(site_model, connection, domain, name, apps):
    """Update or create the site with default ID and keep the DB sequence in sync."""
    Site = apps.get_model("sites", "Site")
    db_engine = connection.vendor
    if db_engine == "postgresql":
        site, created = site_model.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={
                "domain": domain,
                "name": name,
            },
        )
        if created:
            # We provided the ID explicitly when creating the Site entry, therefore the DB
            # sequence to auto-generate them wasn't used and is now out of sync. If we
            # don't do anything, we'll get a unique constraint violation the next time a
            # site is created.
            # To avoid this, we need to manually update DB sequence and make sure it's
            # greater than the maximum value.
            max_id = site_model.objects.order_by("-id").first().id
            with connection.cursor() as cursor:
                cursor.execute("SELECT last_value from django_site_id_seq")
                (current_id,) = cursor.fetchone()
                if current_id <= max_id:
                    cursor.execute(
                        "alter sequence django_site_id_seq restart with %s",
                        [max_id + 1],
                    )

    else:
        site = Site.objects.order_by("-id").first()
        site_id = site.id if site else 1


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    Site = apps.get_model("sites", "Site")
    _update_or_create_site_with_sequence(
        Site,
        schema_editor.connection,
        "djreadysetgo.com",
        "{{ cookiecutter.project_name }}",
        apps,
    )


def update_site_backward(apps, schema_editor):
    """Revert site domain and name to default."""
    Site = apps.get_model("sites", "Site")
    _update_or_create_site_with_sequence(
        Site,
        schema_editor.connection,
        "example.com",
        "example.com",
        apps,
    )


class Migration(migrations.Migration):

    dependencies = [("sites", "0002_alter_domain_unique")]

    operations = [migrations.RunPython(update_site_forward, update_site_backward)]
