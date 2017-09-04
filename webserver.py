from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
#should switch to using and searchng by id's

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>'''
                output +=  '''<h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

           

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<a href="http://localhost:8080/restaurants/new">'''
                output += '''<h4>Create a New Restaurant</h4></a>'''
                output += "<h1>All The Restaurants</h1>"
                items = session.query(Restaurant).all()
                for item in items:
                    i=item.id
                    output+= "<h2>" +item.name+"</h2>"
                    output += '''<a href='restaurants/'''+str(i)+'''/edit'>Edit</a><br>'''
                    output += '''<a href='restaurants/'''+str(i)+'''/delete'>Delete</a><br>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurantnumber = int(self.path.split('/')[-2])
                theonetoedit = session.query(Restaurant).filter_by(id=restaurantnumber).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit %s</h1>" %theonetoedit.name
                output += '''<form method='POST' enctype='multipart/form-data' '''
                output += '''action='/'''+str(restaurantnumber)+'''/edit'><h2>Enter New Name</h2>'''
                output +=  '''<input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                output += '''<a href="http://localhost:8080/restaurants"><h4>Back to Restaurant List</h4></a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurantnumber = int(self.path.split('/')[-2])
                theonetodelete = session.query(Restaurant).filter_by(id=restaurantnumber).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you ABSOLUTELY POSITIVE you want to delete %s ?????</h1>" %theonetodelete.name
                output += '''<form method='POST' enctype='multipart/form-data' '''
                output += '''action='/'''+str(restaurantnumber)+'''/delete'><h2>Bye Bye Forever</h2>'''
                output +=  '''<input type="submit" value="Submit"> </form>'''
                output += '''<a href="http://localhost:8080/restaurants"><h4>Back to Restaurant List</h4></a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' '''
                output += '''action='/restaurants/new/added'><h2>Enter Restaurant Name</h2>'''
                output +=  '''<input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                output += '''<a href="http://localhost:8080/restaurants"><h4>Back to Restaurant List</h4></a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>'''
                output += '''<h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
            

            if self.path.endswith("/restaurants/new/added"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('name')
                    
                #this is creating a new restaurant class
                myFirstRestaurant = Restaurant(name = restaurantName[0])
                #This adds it to the que
                session.add(myFirstRestaurant)
                session.commit()
                output = ""
                output += "<html><body>"
                output += " <h2> %s has been successfully added!</h2>" % restaurantName[0]
                output += '''<form method='POST' enctype='multipart/form-data' '''
                output += '''action='/menuitem/new'><h2>Add Menu Item</h2>'''
                output +=  '''<input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += '''<a href="http://localhost:8080/restaurants"><h4>Back to Restaurant List</h4></a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/edit"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('name')
               #parses the # from the path
                restaurantnumber = int(self.path.split('/')[-2])
                #snags the restaurants from db
                theonetoedit = session.query(Restaurant).filter_by(id=restaurantnumber).one()
                #stores oldname to use in page text
                oldname = theonetoedit.name
                #grabs the right one using the number (should use id???)
                theonetoedit.name = restaurantName[0]
                session.add(theonetoedit)
                session.commit() 
                output = ""
                output += "<html><body>"
                output += " <h2> %s has been successfully renamed to %s!</h2>" %(oldname,restaurantName[0])
                output += '''<a href="http://localhost:8080/restaurants"><h4>Back to Restaurant List</h4></a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/delete"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
               #parses the # from the path
                restaurantnumber = int(self.path.split('/')[-2])
                #snags the restaurants from db
                theonetodelete = session.query(Restaurant).filter_by(id=restaurantnumber).one()
                #stores oldname to use in page text
                oldname = theonetodelete.name
                session.delete(theonetodelete)
                session.commit() 
                output = ""
                output += "<html><body>"
                output += " <h2> %s has been successfully deleted!</h2>" %oldname
                output += '''<a href="http://localhost:8080/restaurants"><h4>Back to Restaurant List</h4></a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
