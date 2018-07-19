import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
from rango.models import Category, Page


class Populate():
    def __init__(self, data):
        self.data = data

    def populate_category(self):
        popcategory = Category.objects.get_or_create(name=self.data[0],
                                                     views=self.data[1],
                                                     likes=self.data[2])[0]
        return popcategory

    def populate_page(self):
        poppage = Page.objects.get_or_create(category=self.data[0],
                                             title=self.data[1],
                                             url=self.data[2])[0]
        return poppage


def populate_db():
    categories = [['Python', 534, 343], ['Django', 234, 233], ['Other Frameworks', 122, 67]]

    python_pages = [
        ['Official Python Tutorial', 'http://docs.python.org/2/tutorial/'],
        ['How to Think like a Computer Scientist', 'http://www.greenteapress.com/thinkpython/'],
        ['Learn Python in 10 Minutes', 'http://www.korokithakis.net/tutorials/python/'],
    ]

    django_pages = [
        ['Official Django Tutorial', 'https://docs.djangoproject.com/en/1.5/intro/tutorial01/'],
        ['Django Rocks', 'http://www.djangorocks.com/'],
        ['How to Tango with Django', 'http://www.tangowithdjango.com/'],
    ]

    ot_pages = [
        ['Bottle', 'http://bottlepy.org/docs/dev/'],
        ['Flask', 'http://flask.pocoo.org'],
    ]

    poplist = [python_pages, django_pages, ot_pages]

    for i in range(len(categories)):
        addcat = Populate(categories[i])
        obj = addcat.populate_category()
        for x in poplist[i]:
            x.insert(0, obj)
            addpage = Populate(x)
            addpage.populate_page()


if __name__ == '__main__':
    print('populating database . . .')
    populate_db()
