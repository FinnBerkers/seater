from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save_family_restrictions(self):
        """Add the all the inter-familiar forbidden neighbors."""
        members = Person.objects.all().filter(family=self)
        for member in members:
            member.forbidden_neighbors.add(*members)
            member.save()


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    # A relation to itself (other instances). Here we specify the
    # forbidden neighbors of this person.
    # If we add a forbidden neighbor here, this person is automatically
    # added to the forbidden neighbors of the selected neighbor (yay).
    forbidden_neighbors = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
