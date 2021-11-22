from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(250)
    password = fields.CharField(100)
    username = fields.CharField(100, unique=True)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return f"User {self.id}: {self.username}"


class Token(Model):

    user = fields.ForeignKeyField('models.Users')
    token = fields.CharField(255)


class Genre(Model):

    id = fields.IntField(pk=True)
    genre_name = fields.CharField(100, blank=False, null=False)

    def __str__(self):
        return self.genre_name


class Movie(Model):

    id = fields.IntField(pk=True)
    movie_name = fields.CharField(255, blank=False, null=False)
    popularity = fields.FloatField(max_digits=10, decimal_places=2, null=True)
    imdbScore = fields.FloatField(max_digits=10, decimal_places=2, null=True)
    year_release = fields.CharField(10, blank=False, null=False)
    genre = fields.ManyToManyField('models.Genre')
    director = fields.CharField(255, blank=False, null=False)

    def __str__(self):
        return self.movie_name

    class Meta:
        unique_together = ('movie_name', 'year_release', 'director')
