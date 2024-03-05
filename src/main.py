import webview

from src.utils.js_api import js_api

if __name__ == '__main__':
    webview.create_window('Todos magnificos', 'html/index.html', js_api=js_api, min_size=(800, 600), maximized=True)
    webview.start(debug=True)
