from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'

    def ready(self):
        import sys
        if sys.version_info >= (3, 14):
            try:
                from django.template.context import BaseContext
                
                def safe_copy(self):
                    duplicate = object.__new__(self.__class__)
                    duplicate.__dict__.update(self.__dict__)
                    duplicate.dicts = self.dicts[:]
                    return duplicate
                    
                BaseContext.__copy__ = safe_copy
            except ImportError:
                pass

