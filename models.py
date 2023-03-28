from django import models


class User(AbstractUser):
    points = models.IntegerField()
    rank = models.IntegerField()

    def reset(self):
        self.points, self.rank = None
        self.save()


class Quiz(models.Model):
    questions = models.ManyToManyField(Question)
    mod = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User)
    description = models.TextField()

    @property
    def points(self):
        return sum(
            [p["points"] for p in questions.objects.values_list(points)]
        )

class Question(models.Model):

    headline = models.CharField()
    char_body = models.TextField(null=True, blank=True)
    image_body = models.ImageField(null=True, blank=True)
    points = models.PositiveIntegerField()
    answer = models.TextField()


class Answer(models.Model):
    char_body = models.TextField()
    user = models.ForeignKey(on_delete=models.CASCADE)
    question = models.ForeignKey(on_delete=models.CASCADE)
    