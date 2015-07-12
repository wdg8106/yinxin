import os.path
import random
 
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
 
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
# database = tornado.Connection('localhost','yinxin',user= 'root',password = '123456')
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main.html')

class CantactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cantact.html')

class UsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('us.html')

class FirstHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('first.html')

class SecondHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('second.html')

class ThirdHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('third.html')

class ZhuangxiuHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('zhuangxiu.html')

class ApplyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('apply.html')
    def post(self):
        product = self.get_argument('product')
        name = self.get_argument('name')
        phone = self.get_argument('phone')
        print(type(product),type(name),type(phone))
        if isinstance(product,unicode):
            product = product.encode('utf-8')
        if isinstance(name,unicode):
            name = name.encode('utf-8')
        if isinstance(phone,unicode):
            phone = phone.encode('utf-8')
        # database.execute('insert into apply()')
        history = "%s\t%s\t%s\n" %(name,phone,product)
        f = open('apply.txt','a')
        f.write(history)
        f.close()
        return self.render('success.html')



        


 
class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped
 
    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines,
                choice=random.choice)
 
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler,{},'index'),
            (r'/poem', MungedPageHandler),
            (r'/first',FirstHandler,{},'first'),
            (r'/second',SecondHandler,{},'second'),
            (r'/third',ThirdHandler,{},'third'),
            (r'/zhuangxiu',ZhuangxiuHandler,{},'zhuangxiu'),
            (r'/cantact',CantactHandler,{},'cantact'),
            (r'/us',UsHandler,{},'us'),
            (r'/apply',ApplyHandler,{},'apply'),
            ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()