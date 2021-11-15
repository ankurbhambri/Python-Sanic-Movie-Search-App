from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    is_admin = fields.BooleanField(default=False)

    def __str__(self):
        return f"User {self.id}: {self.name}"
