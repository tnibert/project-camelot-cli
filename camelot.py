#! /usr/bin/env python3
import requests
import argparse
import sys
import getpass

HOST='https://picpicpanda.com'

URLS = {
    'upload_photo': '/api/upload/{}',
    'update_photo_desc': '/api/update/photo/desc/{}'
}

def login(save_cookie=True):
    """
    Login, prompting user for login (if no valid cookie - to implement)
    return: session object
    """
    # todo: implement cookie saving
    print("Login")

    # prompt for input
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()
    try:
        password = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
        return

    s = requests.session()
    p = s.get(HOST)
    csrftoken = s.cookies['csrftoken']

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'username': user,
        'password': password
    }

    print(csrftoken)
    p = s.post(HOST, data=payload, headers=dict(Referer=HOST))
    print(p)
    return s

def create_album(name):
    print("create_album")

def upload_photo(fname):
    print("upload_photo")

def update_photo_desc(description):
    print("update_photo_desc")

def list_albums(user_id):
    print("list_albums")

def list_photos(album_id):
    print("list_photos")

if __name__ == '__main__':

    # munge command line args for argparse
    # hmm... this is a bit ugly
    opts = sys.argv[2:]
    sys.argv = sys.argv[:2]

    # command options
    FUNCTION_MAP = {
                    'login' : login,
                    'create_album' : create_album,
                    'upload_photo': upload_photo,
                    'photo_desc': update_photo_desc,
                    'list_albums': list_albums,
                    'list_photos': list_photos
    }

    # process command line args with argparse
    parser = argparse.ArgumentParser(description='Command line utility to interface with PicPicPanda')

    parser.add_argument('command', choices=FUNCTION_MAP.keys())

    args = parser.parse_args()

    print(args)

    # execute the appropriate command
    func = FUNCTION_MAP[args.command]
    func(*opts)
