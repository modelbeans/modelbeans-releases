"""Call an already-running local ModelBeans API. Python 3.10+, standard library."""
import json
import os
import urllib.request
from urllib.parse import urlparse


def main():
    base = os.environ['MODELBEANS_BASE_URL'].rstrip('/')
    parsed = urlparse(base)
    if parsed.scheme not in ('http', 'https') or parsed.hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise SystemExit('This example requires a local loopback API address.')
    body = json.dumps({
        'model': os.environ['MODELBEANS_MODEL'],
        'messages': [{'role': 'user', 'content': 'Reply with a short greeting.'}],
        'max_tokens': 256,
        'chat_template_kwargs': {'enable_thinking': False},
        'stream': False,
    }).encode('utf-8')
    request = urllib.request.Request(base + '/chat/completions', data=body, headers={
        'Authorization': 'Bearer ' + os.environ['MODELBEANS_API_KEY'],
        'Content-Type': 'application/json',
    })
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=300) as response:
        result = json.load(response)
    content = result['choices'][0]['message'].get('content')
    if not content:
        raise SystemExit('No text answer returned. Check the model and output budget.')
    print(content)


if __name__ == '__main__':
    main()
