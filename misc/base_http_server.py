#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, cgi
import datetime

class GetHandler(BaseHTTPRequestHandler):
    """ curl -i http://192.168.199.170:8080/?foo=bar """

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return


class PostHandler(BaseHTTPRequestHandler):

    # This do_POST method simply prints out the raw data string
    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = self.data_string
        with open('/var/log/tps.log', 'a') as f:
            print data
            f.write(str(datetime.datetime.now()) + ": " + str(data.split()) + "\n")
        return

    # The following do_POST method parses form data using the cgi module
    """ curl http://192.168.199.170:8080/ -F name=dhellmann -F foo=bar  """

    """
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                        (field, field_item.filename, file_len))
                print field, field_item.filename, file_len
            else:
                # Regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))
                print field, form[field].value
        return
        """


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    #server = HTTPServer(('', 8080), GetHandler)
    server = HTTPServer(('', 8080), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

    