import requests
import yaml


def load_sponsors() -> list:
    print("Loading sponsors...")
    with open("./sponsors.yml", "r",encoding='utf-8') as f:
        data = yaml.safe_load(f)

    with requests.Session() as session:

        for e in data['sponsors']:
            if 'player_name' not in e:
                e['player_name'] = 'Unknown'
            e['image'] = get_img(session, e['player_name'])
            print(e)
    return sorted(data['sponsors'],key=lambda x: x['amount'],reverse=True)


def get_img(session, player_name) -> str:
    if player_name == 'Unknown':
        return 'https://crafatar.com/renders/head/aaaaaaaa-cf6b-4485-bef9-3957e7b7f509'
    else:
        with session.get(f'https://playerdb.co/api/player/minecraft/{player_name}') as data:
            data = data.json()
            if data['success']:
                uuid = data['data']['player']['id']
                img = f'https://crafatar.com/renders/head/{uuid}'
            else:
                img = 'https://crafatar.com/renders/head/aaaaaaaa-cf6b-4485-bef9-3957e7b7f509'
            return img


if __name__ == '__main__':
    load_sponsors()