import functools

import requests
import yaml
from flask import Flask, render_template, send_from_directory

from utils.auto_fetch import Fetcher
from utils.sponsors import load_sponsors

app = Flask(__name__)
app.template_folder = 'templates'

with open('config.yml', encoding='utf8') as f:
    conf = yaml.load(f.read(), Loader=yaml.FullLoader)

mc_show_info = conf['server']['show-info']
mc_host = conf['server']['host']
mc_port = conf['server']['port']
mc_query = conf['server']['query']
mc_name = conf['server']['name']
mc_logo = conf['server']['logo']
mc_preview_title = conf['server']['preview']['title']
mc_preview_descr = conf['server']['preview']['descr']
mc_preview_images = conf['server']['preview']['images']
fetcher = Fetcher(conf['task']['interval'])

host = conf['web']['host']
port = conf['web']['port']


@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)


@app.route('/')
def home():
    offline = False
    try:
        response = fetcher.get(
            "server_status",
            functools.partial(
                lambda: requests.get(f'https://api.mcsrvstat.us/3/{mc_host}:{mc_port}').json()
            )
        )
        offline = not response['online']
    except TimeoutError:
        offline = True
    if not offline:
        cleaned_motd = '\n'.join(response['motd']['clean'])
        player_list = []
        print("Loading players...")
        for player in response['players'].get('list', []):
            name = player['name']
            uuid = player['uuid']
            img = f'https://crafatar.com/renders/head/{uuid}'
            print(img)
            player_list.append({'name': name, 'img': img})
        sponsors = fetcher.get(
            "get_sponsors",
            functools.partial(load_sponsors)
        )
        return render_template('index.html',
                               name=mc_name,
                               host=mc_host,
                               port=mc_port,
                               show_info=mc_show_info,
                               motd=cleaned_motd,
                               current=f"{response['players']['online']}({len(response['players'].get('list', []))})",
                               maxp=response['players']['max'],
                               logo=mc_logo,
                               preview_title=mc_preview_title,
                               preview_descr=mc_preview_descr,
                               preview_images=mc_preview_images,
                               player_list=player_list,
                               sponsor_list=sponsors,
                               offline=offline)
    else:
        return render_template('index.html',
                               name=mc_name,
                               host=mc_host,
                               port=mc_port,
                               show_info=mc_show_info,
                               logo=mc_logo,
                               preview_title=mc_preview_title,
                               preview_descr=mc_preview_descr,
                               preview_images=mc_preview_images,
                               offline=offline)


if __name__ == '__main__':
    app.run(host, port)
