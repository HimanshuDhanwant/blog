import webapp2  #for web applications
import os       # accessing the files within the computer
import jinja2   #for templates
import time     #for current time

from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__) ,'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class Blog(db.Model):
    title=db.StringProperty(required=True)
    blog=db.TextProperty(required=True)
    created=db.DateProperty(auto_now_add=True)

class blogPage(Handler):
    def write_form(self):
        blogs=db.GqlQuery("select * from Blog order by created desc")
        self.render("blogPage.html",blogs=blogs)

    def get(self):
        self.write_form()

    def post(self):
        self.write_form()

class MainPage(Handler):
    def write_form(self,tit="",art="",error=""):
        # arts=db.GqlQuery("select * from Art order by created desc")
        self.render("index.html",title=tit,art=art,error=error)
    def get(self):
        self.write_form()
        # self.render("index.html")

    def post(self):
        title=self.request.get("title")
        blog=self.request.get("blog")
        if title and blog:
            b=Blog(title=title, blog=blog)
            b.put()
            self.redirect("/blogPage")
            # self.write("Thanks ")
        else:
            erro="Title and Art both are required!!"
            self.write_form(title,art,erro)

app = webapp2.WSGIApplication([('/', MainPage),('/blogPage', blogPage)], debug=True)
