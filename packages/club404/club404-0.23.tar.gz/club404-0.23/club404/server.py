#!/usr/bin/env python3
import json
import signal

from urllib import parse
from functools import partial

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import HTTPError

from club404 import GetConfig
from club404.router import WebRequest, WebResponse
from club404.templates import TemplateRouter


class Request(WebRequest):
    # Wrap your request object into serializable object
    def __init__(self, ctx): super().__init__(
        verb=ctx.command,
        path=ctx.path,
        head=self.headers(ctx),
        body=self.body(ctx) if ctx.command in ["POST", "PUT"] else None,
        params=self.query(ctx),
    )

    def headers(self, ctx):
        head = {}
        for key in ctx.headers:
            head[key.lower()] = ctx.headers.get(key)
        return head

    def query(self, ctx):
        path_parts = ctx.path.split('?')
        if len(path_parts) > 1:
            return parse.parse_qs(path_parts[1])
        return {}

    def body(self, ctx):
        # Only try and parse the body for known methods (eg: POST, PUT)
        ctype = self.head['content-type'] if 'content-type' in self.head else 'application/json'
        length = int(ctx.headers.get('content-length'))
        match ctype:
            case 'application/json':
                input = ctx.rfile.read(length).decode('utf8')
                data = json.loads(input)
            case 'application/x-www-form-urlencoded':
                input = ctx.rfile.read(length).decode('utf8')
                form = parse.parse_qs(input, keep_blank_values=1)
                data = {}
                for key in form:
                    if len(form[key]) > 1:
                        data[key] = form[key]
                    elif len(form[key]) == 1:
                        data[key] = form[key][0]
            case _:
                message = 'Content type "%s" cannot be parsed into a body.' % ctype
                raise Exception(message)

        return data


class Response(WebResponse):
    __sent = False

    # Wrap your response object into serializable object
    def __init__(self, ctx, req): super().__init__(
        verb=ctx.command,
        path=ctx.path,
        head={
            'content-type': req.head['content-type']
        } if req and 'content-type' in req.head else {},
        body=None
    )

    def encoder(self): return self.__dict__

    def redirect(self, ctx, location):
        self.reply(ctx, 302, head={'Location': location})

    def respond(self, ctx, status=200, headers={}, message=""):
        if self.__sent:
            raise Exception('Status already sent')
        ctx.send_response(status, message)
        self.__sent = True

        # Finilize the headers
        for key in headers:  # Append headers
            self.head[key] = headers[key]

    def reply(self, ctx, body=None, head={}):
        for key in head:  # Append headers
            self.head[key] = head[key]

        # Send status code (if not sent)
        if not self.__sent:
            self.respond(ctx, self.status)

        # Reply with headers (if not already sent)
        for key in self.head:
            ctx.send_header(key, self.head[key])
        ctx.end_headers()

        # Send the response UTF encoded (if defined)
        if body:
            ctx.wfile.write(body.encode('utf8'))


class Handler(SimpleHTTPRequestHandler):
    # Bind your route handlers into our router's path resolvers
    def __init__(self, server, *extra_args, **kwargs):
        self.reply = server.reply
        self.config = server.config
        self.proxy = server.proxy
        super().__init__(directory=server.config.static, *extra_args, **kwargs)

    def do_DEFAULT(self, verb):
        # If no custom routes were triggered, this function will be called..
        # We will check for default actions in this order:
        #  1) config.proxy  - (URL)  Proxy the request
        #  2) config.static - (PATH) Serve static content
        #  3) Fallback: Send "Not found"
        if self.config.proxy:
            return self.do_PROXY(verb, self.config.proxy)
        elif verb == "GET" and self.config.static:
            # Serve contents from the specified static folder
            return self.do_STATIC()
        else:
            # The default action is to reply: "Not found"
            self.send_response(404, "Not Found")
            self.end_headers()

    def do_REPLY(self, verb): self.reply(verb, self.path, self)
    def do_STATIC(self): super().do_GET()
    def do_HEAD(self): self.do_GET()
    def do_GET(self): self.do_REPLY("GET")
    def do_POST(self): self.do_REPLY("POST")
    def do_PUT(self): self.do_REPLY("PUT")
    def do_PATCH(self): self.do_REPLY("PATCH")
    def do_DELETE(self): self.do_REPLY("DELETE")

    def do_PROXY(self, verb, proxy):
        # Wrap the generic proxy request and handle response to client
        def failed(status, message):
            print(' ! Error <-- [ %s ] %s' % (status, message))
            self.send_error(status, message)
        try:
            # Create a new request handler, then fetch the response via a proxied request
            res = self.proxy(proxy, Request(self))
            if not res:
                return

            # Forward the response to the client that is waiting for it
            self.send_response(res.getcode())
            for key in res.headers:
                self.send_header(key, res.headers[key])
            self.end_headers()
            self.wfile.write(res.read())
            res.close()
        except HTTPError as e:
            failed(599, 'Proxy Error: {}'.format(str(e)))
        except IOError as e:
            failed(404, 'IO Error: {}'.format(str(e)))
        except Exception as e:
            failed(503, 'error trying to proxy: {}'.format(str(e)))


class WebServer(TemplateRouter):
    app = None
    config = None

    def __init__(self, prefix='', config=GetConfig()):
        # Add HTTP handlers and route info
        routes = {} if not config.routes else config.routes
        super().__init__(prefix, routes)

        # Load and parse config
        self.config = config
        self.host = (config.host, config.port)

        # Create a new server instance that will be serving our routes
        self.app = HTTPServer(self.host, partial(Handler, self))

    def static(self, path):
        self.config.static = path

    def start(self):
        if not self.app:
            raise Exception("FATAL: App instance for server not set.")

        # Gracefully handle shutdowns
        signal.signal(signal.SIGINT, self.onExit)

        # Start the server using the target (request handler) type
        self.app.serve_forever()

    def route(self, verb, path):
        # For the app router, we can directly register the route,
        # so we override the route registration
        def decorator(action): self.register({
            verb: {path: self.format(action)}
        })
        return decorator

    def reply(self, verb, path, ctx):
        # This method is called from the `Handler` interface, each time a route is intercepted
        # See if we can match a route to the current verb
        action = self.find(verb, path)
        if not action:
            # Not found: delegate to the default route handler
            return ctx.do_DEFAULT(verb)

        # Service the incomming request with the specified handler
        req = Request(ctx)
        resp = Response(ctx, req)
        data = action(req, resp)

        # Write the body of the response
        resp.respond(ctx, resp.status, resp.head)
        if data:
            resp.reply(ctx, body=data)

        return data

    def discover(self, path="./routes"):
        print(' - Auto discovering routes in: %s' % path)

    def onExit(self, signum, frame): return exit(1)


def main():
    app = WebServer()
    app.discover()  # By default we auto discover the routes...
    app.start()


if __name__ == '__main__':
    main()
