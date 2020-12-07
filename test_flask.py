from unittest import TestCase

from app import app
from models import db, User, Post

# Using test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Jeremy", last_name="Johnson", image_url="")
        # add in a test user
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        
        user2 = User(first_name="Rishi", last_name="Sunak", image_url="")
        # add in a second test user
        db.session.add(user2)
        db.session.commit()

        self.user2_id = user2.id


        post = Post(title = 'Test title', content = 'Contents provided for test purposes', user_id = user.id)
        # add and commit a test post
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id




    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    

    def test_list_users(self):
        #list all users
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jeremy', html)
            self.assertIn('Rishi', html)


    def test_show_user_details(self): 
        # user get() with user id to find user
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Jeremy Johnson</h1>', html)

    def test_show_user2_details(self): 
        # user get() with user id to find user
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user2_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Rishi Sunak</h1>', html)

    
    def test_delete_user(self):
        # delete user
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user2_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('Rishi Sunak', html)

    
    def test_add_new_user(self):
        #add new user
         with app.test_client() as client:
            d = {"first_name": "Alkesh", "last_name": "Singh", "image_url": " "}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Alkesh Singh", html)

#Part 2 of exercise: posts

    def test_post_title(self):
        # list a specific user and test for the presence of a post title 
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test title', html)

    def test_new_post_form(self):
# test for presence of new post form
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Add Post for Jeremy Johnson</h2>', html)


    def test_post_details(self):
        # list details of a post for a user and test for the presence of the post contents 
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Contents provided for test purposes', html)


    def test_add_new_post(self):
# test addition of a post
        with app.test_client() as client:
            d = {"title": "Second test title", "content": "Contents for second post", "user_id": "2"}
            resp = client.post(f"/users/{self.user2_id}/posts/new", data=d, follow_redirects=True) # this is producing a 400 error
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Rishi Sunak</h1>', html)



    def test_delete_post(self):
# test delete of a post
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)



