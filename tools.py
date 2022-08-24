import logging

from django.contrib.auth.mixins import UserPassesTestMixin


logger = logging.getLogger(__name__)
lol = logger.warning


class OwnerRequirementMixin(UserPassesTestMixin):
    def test_func(self):
        lol('▬▬▬ TEST_FUNC ▬▬▬')
        # try to get the object.owner, if it fails,  get the object.tree.owner
        try:   
            owner = self.get_object().owner
        except AttributeError:
            owner = self.get_object().tree.owner
        # if the user is the owner, return True, else return False
        return self.request.user == owner

        

        





        return self.request.user == self.get_object().owner
        return self.request.user == self.get_object().tree.owner