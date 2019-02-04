from django.contrib import admin

from .models import Family, Person


class PersonInLine(admin.TabularInline):
    """
    Class that specifies that the Person class can be shown inline.

    The Person class can be edited at the same time when adding a class which is
    a foreign key of Person. In the case of the Person class, this can only be the
    Family class.
    """
    model = Person


class FamilyAdmin(admin.ModelAdmin):
    inlines = [PersonInLine]

    def save_model(self, request, obj, form, change):
        """
        Overrides its super method to save the model.

        Saves the model if it is not in the database yet, otherwise adds all the
        inter-familiar forbidden neighbors of the currently saved family members.
        """
        if not obj.pk:
            super(FamilyAdmin, self).save_model(request, obj, form, change)
        else:
            obj.save_family_restrictions()

    def save_related(self, request, form, formsets, change):
        """
        Overrides its super method to save the related models, i.e., the inline models.

        Save all the inline/children models (Persons), and then save the Family.
        Note that this is always called after save_model, and thus the Family will be in
        the database at this point. Then calling save_model will add the inter-familiar
        forbidden neighbors to the Person objects.
        """
        for formset in formsets:
            self.save_formset(request, form, formset, change)
        self.save_model(request, form.instance, form, change)


# Only explicitly register the Family model, as the Person model will be registered as
# an inline of the Family model.
admin.site.register(Family, FamilyAdmin)
