import django_tables2 as tables

class PreviewTable(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap.html"
