import os
import datetime
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

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

		# get top ten posts from DB

		self.render("landing_page.html")

		# history = self.request.get_all("titles")
		# if history:
		# 	output_history = ""
		# 	for title in history:
		# 		output_hidden += hidden_html % title
		# 		output_history += item_html % title
		# 	output_shopping = 

class NewPost(Handler):
	def get(self):
		self.render("new_post.html",subject = "", content = "")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		postDate = datetime.date.today()

		# Do verification

		# store in DB w/ (title=title,content=content,postDate=postDate)
		# Generate an ID

		postId = '1001'

		self.redirect("/blog/" + postId)
		
class Post(Handler):
	def get(self, url):
		postId = url

		# Query DB with Id = postId
		# Get title, content and date

		self.render("post.html", subject=path, postDate=postDate, content=content)

app = webapp2.WSGIApplication([('/blog', MainPage),
							   ('/blog/newpost', NewPost),
							   ('/blog/(\d+)', Post),
								],
								debug=True)