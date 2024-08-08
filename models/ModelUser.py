from .entities.User import User

class ModelUser:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user WHERE username = %s"""
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row is not None:
                db_user = User(row[0], row[1], row[2], row[3])
                return db_user
            return None
        except Exception as ex:
            raise Exception(ex)
