import unittest
from app.models import Joke, User
class JokeTest(unittest.TestCase):
    def setUp(self):
        '''
        Set up method to run before each test cases.
        '''
        self.new_joke = Joke("Knock knock")
    def test_check_instance_variables(self):
        self.assertEquals(self.new_joke.comments,"Knock Knock")
      
    def test_save_joke(self):
        """
        To check is jokes are being saved
        """
        self.new_joke.save_joke()
        self.assertTrue(len(Joke.query.all())>0)
