#! /usr/bin/env python3
import requests
import argparse
import sys, os
import getpass
import pickle
import json
import pprint

pp = pprint.PrettyPrinter(indent=2)

#HOST='https://picpicpanda.com'
HOST='http://127.0.0.1:8000'

URLS = {
    'upload_photo': '/api/upload/{}',
    'update_photo_desc': '/api/update/photo/desc/{}',
    'list_albums': '/api/{}/getalbums',
    'list_photos': '/api/album/{}/getphotos'
}

COOKIE_FILE='.PPP_COOKIE'


def login(save_my_cookie=True):
    """
    Login, prompting user for login if no valid cookie
    return: session object
    """
    # define some local functions to this function
    def save_cookie(sess, fi=COOKIE_FILE):
        with open(fi, 'wb') as f:
            pickle.dump(sess.cookies, f)

    def load_cookie(fi=COOKIE_FILE):
        # todo: not absolutely 100% certain this is keeping us logged in, keep an eye on other requests
        session = requests.session()  # or an existing session

        with open(fi, 'rb') as f:
            session.cookies.update(pickle.load(f))

        return session

    def check_cookie_expiry(r):
        # this function has not been observed to work, but maybe we just don't have expiry
        #expires = next(x for x in r.cookies if x.name == 'WebSecu').expires
        expires = None
        for cookie in r.cookies:
            if cookie.name == 'WebSecu':
                expires = cookie.expires
        print(expires)

    print("Login")

    try:
        s = load_cookie()
    except:
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

        # cookie persistence
        if save_my_cookie and not os.path.isfile(COOKIE_FILE):
            save_cookie(s)

    return s


def create_album(name):
    print("create_album")
    s = login()


def upload_photo(fname):
    print("upload_photo")


def update_photo_desc(description):
    print("update_photo_desc")


def list_albums(user_id):
    """
    List albums for the given user
    :param user_id: primary key of user
    :return: dict of the json returned
    """
    print("list_albums")
    s = login()

    response = s.get(HOST + URLS['list_albums'].format(user_id))
    data = json.loads(response.content)
    pp.pprint(data)
    return data


def list_photos(album_id):
    print("list_photos")
    s = login()

    response = s.get(HOST + URLS['list_photos'].format(album_id))
    data = json.loads(response.content)
    pp.pprint(data)
    return data


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

    # execute the appropriate command
    func = FUNCTION_MAP[args.command]
    func(*opts)
