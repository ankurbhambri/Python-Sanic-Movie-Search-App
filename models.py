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


# class Genre(Model):

#     id = fields.IntField(pk=True)
#     genre_name = fields.CharField(50)

#     def __str__(self):
#         return self.genre_name


# class Director(Model):

#     id = fields.IntField(pk=True)
#     director_name = fields.CharField(50)

#     def __str__(self):
#         return self.director_name


class Movie(Model):

    id = fields.IntField(pk=True)
    movie_name = fields.CharField(255)
    popularity = fields.FloatField(max_digits=10, decimal_places=2, null=True)
    imdbScore = fields.FloatField(max_digits=10, decimal_places=2, null=True)
    genre = fields.TextField()
    director = fields.TextField()

    def __str__(self):
        return self.movie_name


# genre = fields.ManyToManyField('models.Genre')
# director = fields.ManyToManyField('models.Director')
