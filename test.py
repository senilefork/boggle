from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
from unittest import TestCase 
from app import app, start, home_page, check_word, score

class FlaskTests(TestCase):

    app.config['TESTING'] = True

    def test_start(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>How big do you want your boggle board?</h1>', html)

    def test_home_page_redirect(self):
        with app.test_client() as client:
            res = client.get('/home?board-size=0')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')
    
    def test_home_page_redirect_followed(self):
        with app.test_client() as client:
            res = client.get('/home?board-size=0', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>How big do you want your boggle board?</h1>', html)



    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/home?board-size=5')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle!</h1>', html)

    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['A','B','C','D'],
                                           ['L','P','B','O'],
                                           ['L','O','E','G'],
                                           ['O','P','G','S']]
                res = client.get('/check-word?words=dogs')

                self.assertEqual(res.json['server'], 'ok')


    def test_score(self):
        with app.test_client() as client:
            sent = {'scores' : 5}
            res = client.post('/scores', data=sent)
            #import pdb
            #pdb.set_trace()
            print(res.data)
            self.assertEqual(res.json['scores'],'5') 

