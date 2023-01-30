import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_snakes, get_single_snake, get_snakes_by_species, create_snake
from views import get_all_species, get_single_species
from views import get_all_owners, get_single_owner

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        response = {}

        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed


            if resource == "snakes":
                if id is not None:
                    snake = get_single_snake(id)
                    
                    if snake.get('species_id') == 2:
                        self._set_headers(405)
                        response = {"message": "Snakes of the Aonyx Cinerea species always live in colonies and are never found solo in the wild."}
                    else:
                        response = snake
                        self._set_headers(200)

                else:
                    response = get_all_snakes()
                    self._set_headers(200)


            elif resource == "species":
                if id is not None:
                    response = get_single_species(id)
                    self._set_headers(200)
                else:
                    response = get_all_species()
                    self._set_headers(200)
            elif resource == "owners":
                if id is not None:
                    response = get_single_owner(id)
                    self._set_headers(200)
                else:
                    response = get_all_owners()
                    self._set_headers(200)
            else:
                self._set_headers(404)
                response = {"message": "Resource not found"}

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            if query.get('species') and resource == 'snakes':
                self._set_headers(200)
                response = get_snakes_by_species(query['species'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        self._set_headers(404)
        response = {"error": "PUT requests are not supported for this endpoint"}
        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        self._set_headers(404)
        response = {"error": "DELETE requests are not supported for this endpoint"}
        self.wfile.write(json.dumps(response).encode())


    def do_POST(self):
        "docustring"
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_item = None

        if resource == "snakes":

            if "name" in post_body and "owner_id" in post_body and "species_id" in post_body and "gender" in post_body and "color" in post_body:
                self._set_headers(201)
                new_item = create_snake(post_body)

            else:
                self._set_headers(400)

                new_item = {
                    "message": f'{"Name is required"}' if "name" not in post_body else "" f'{"Owner ID is required"}' if "owner_id" not in post_body else "" f'{"Species ID is required"}' if "species_id" not in post_body else "" f'{"Gender is required"}' if "gender" not in post_body else "" f'{"Color is required"}' if "color" not in post_body else ""
                }
        else:
            self._set_headers(404)
            new_item = {"message": "Resource not found"}
        self.wfile.write(json.dumps(new_item).encode())
    
    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'snakes', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
