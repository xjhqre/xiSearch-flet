import random
import sys

import webview


class Api:

    def init(self):
        response = {'message': 'Hello from Python {0}'.format(sys.version)}
        return response

    def getRandomNumber(self):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(
                random.randint(0, 100000000)
            )
        }
        return response

    def sayHelloTo(self, name):
        response = {'message': 'Hello {0}!'.format(name)}
        return response

    def error(self):
        raise Exception('This is a Python exception')


if __name__ == '__main__':
    api = Api()
    webview.create_window('Todos magnificos', '../html/index.html', js_api=api, min_size=(800, 600), maximized=True)
    webview.start()
