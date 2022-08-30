import logging

from django.contrib.auth.mixins import UserPassesTestMixin


logger = logging.getLogger(__name__)
lol = logger.warning


class OwnerRequirementMixin(UserPassesTestMixin):
    """ Returns True if the request.user is the owner of the tree. """
    
    def test_func(self):
        try:   
            owner = self.get_object().owner
        except AttributeError:
            owner = self.get_object().tree.owner
        return self.request.user == owner
