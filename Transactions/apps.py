
from django.apps import AppConfig

class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Transactions'  # اسم التطبيق الخاص بك

    def ready(self):
        import Transactions.signals  # تأكد من استيراد signals
