from thursdays.tests import *

class TestThursdayController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='thursday', action='index'))
        # Test response...
