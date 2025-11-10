class  AdminRouter:
    """
    راوتر معدل لتوجيه الجلسات إلى SQLite
    """
    
    def db_for_read(self, model, **hints):
        # جلسات وجميع نماذج authentication تقرأ من SQLite
        if model._meta.app_label in ['auth', 'contenttypes', 'admin', 'sessions']:
            return 'admin_db'
        # النماذج الأخرى تقرأ من MySQL
        return 'default'

    def db_for_write(self, model, **hints):
        # جميع نماذج Django الأساسية تكتب في SQLite
        if model._meta.app_label in ['auth', 'contenttypes', 'admin', 'sessions']:
            return 'admin_db'
        # منع الكتابة في MySQL
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # السماح بالعلاقات بين النماذج في نفس قاعدة البيانات
        db_set = {'admin_db', 'default'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # تهجير تطبيقات Django إلى SQLite فقط
        if app_label in ['auth', 'contenttypes', 'admin', 'sessions']:
            return db == 'admin_db'
        # منع تهجير النماذج الأخرى
        return False