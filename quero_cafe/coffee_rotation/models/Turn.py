from django.db import models

from coffee_rotation.models.Cycle import Cycle
from django.contrib.auth.models import User


class Turn(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='FK_USER')
    removed_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='removed_by_id', related_name='FK_REMOVED_BY', null=True)

    date_choosed = models.DateTimeField(null=True)
    date_voluntary = models.DateTimeField(null=True)
    date_removed = models.DateTimeField(null=True)

    justification = models.TextField(null=True)

    def get_date(self):

        if self.date_removed:
            return self.date_removed

        if self.date_choosed:
            return self.date_choosed

        if self.date_voluntary:
            return self.date_voluntary

        return False

    def is_removed(self):

        if self.date_removed:
            return True

        return False

    def is_choosed(self):

        if self.date_choosed:
            return True

        return False

    def is_voluntary(self):

        if self.date_voluntary:
            return True

        return False

    def get_type(self):

        if self.is_removed():
            return 'Cancelado'

        if self.is_choosed():
            return 'Escolhido Aleatório'

        if self.is_voluntary():
            return 'Vonluntário'

        return False

    def presenter_date(self):
        return self.get_date().strftime("%d/%m/%Y %H:%M:%S")