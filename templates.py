import os
import datetime
import jinja2
import webapp2

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Post(ndb.Model):
	subject = ndb.StringProperty(required = True)
	content = ndb.TextProperty(required = True)
	createdDate = ndb.DateProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def get(self):
		topTenPosts = ndb.gql(
			"SELECT * FROM Post ORDER BY createdDate DESC LIMIT 10").fetch()
		self.render("landing_page.html", posts=topTenPosts)

class NewPostHandler(Handler):
	def get(self):
		self.render("new_post.html",
					subject="",
					subjectError="",
					content="",
					contentError="")

	def post(self):
		subject = self.request.get("subject")
		subjectError = ''
		content = self.request.get("content")
		contentError = ''

		if subject and content:
			newPost = Post(subject=subject,
						   content=content)
			newPostKey = newPost.put()
			postId = newPostKey.id()
			self.redirect("/blog/" + str(postId))

		elif not subject and not content:
			subjectError = 'Subject can not be empty!'
			contentError = 'Content can not be empty!'
		elif not subject:
			subjectError = 'Subject can not be empty!'
		else:
			contentError = 'Content can not be empty!'

		self.render("new_post.html",subject=subject,subjectError=subjectError,
			content=content,contentError=contentError)

class PostHandler(Handler):
	def get(self, url):
		postId = long(url)

		postKey = ndb.Key('Post', postId)

		post = postKey.get()

		subject = post.subject
		content = post.content
		createdDate = post.createdDate

		self.render("post.html",
					subject=subject,
					createdDate=createdDate,
					content=content,
					postId=postId)

app = webapp2.WSGIApplication([('/blog', MainPage),
							   ('/blog/newpost', NewPostHandler),
							   ('/blog/(\d+)', PostHandler),
								],
								debug=True)