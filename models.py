from django import models


class User(AbstractUser):
    points = models.IntegerField()
    rank = models.IntegerField()
    is_mod = models.BooleanField(default=False)

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

    def get_board(self):
        """Return the current quiz rankings& points"""
        return self.participants.filter(id_mod=False).values_list("username", "points", "rank")

    def finished(self):
        # todo


class Question(models.Model):

    headline = models.CharField()
    char_body = models.TextField(null=True, blank=True)
    image_body = models.ImageField(null=True, blank=True)
    points = models.PositiveIntegerField()
    answer = models.TextField()


class Answer(models.Model):
    char_body = models.TextField()
    user = models.ForeignKey(on_delete=models.CASCADE)
    question = models.ForeignKey(on_delete=models.CASCADE, related_name="r_answer")
    state = models.CharField(null=true, blank=True)

    def review(self):

        if self.char_body != question.answer:
            self.user.points -= self.question.points
            self.state = f"Leider falsch. - {self.question.points} Punkte"

        else:
            self.user.points += self.question.points
            self.state = f"Richtig. + {self.question.points} Punkte"

        self.user.save(update_fields=["points"])
        self.save(update_fields=["state"])