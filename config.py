import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_sslify import SSLify

from services import bitbucket
from services import bitly
from services import dailymile
from services import deviantart
from services import digg
from services import disqus
from services import dropbox
from services import facebook
from services import fitbit
from services import fivehundredpx
from services import flickr
from services import foursquare
from services import getglue
from services import github
from services import goodreads
from services import google
from services import imgur
from services import instagram
from services import lastfm
from services import linkedin
from services import liveconnect
from services import meetup
from services import miso
from services import ohloh
from services import plurk
from services import readmill
from services import rdio
from services import smugmug
from services import soundcloud
from services import stackexchange
from services import tripit
from services import tumblr
from services import twitter
from services import vimeo
from services import wordpress
from services import yahoo

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['DEBUG'] = 'DEBUG' in os.environ
app.wsgi_app = ProxyFix(app.wsgi_app)
SSLify(app)


def init_services(*services):
    service_list = []

    for service in services:
        alias = service.alias.upper()
        key = os.environ.get('%s_KEY' % alias, '').decode('utf8')
        secret = os.environ.get('%s_SECRET' % alias, '').decode('utf8')

        if key and secret:  # Only initialize if all the pieces are in place
            service_list.append(service(key, secret))

    return service_list

services = init_services(bitbucket.Bitbucket,
                         bitly.Bitly,
                         dailymile.Dailymile,
                         deviantart.DeviantArt,
                         digg.Digg,
                         disqus.Disqus,
                         dropbox.Dropbox,
                         facebook.Facebook,
                         fitbit.FitBit,
                         fivehundredpx.FiveHundredPX,
                         flickr.Flickr,
                         foursquare.Foursquare,
                         getglue.GetGlue,
                         github.GitHub,
                         goodreads.Goodreads,
                         google.Google,
                         imgur.Imgur,
                         instagram.Instagram,
                         lastfm.LastFM,
                         linkedin.LinkedIn,
                         liveconnect.LiveConnect,
                         meetup.Meetup,
                         miso.Miso,
                         ohloh.Ohloh,
                         plurk.Plurk,
                         readmill.Readmill,
                         rdio.Rdio,
                         smugmug.SmugMug,
                         soundcloud.SoundCloud,
                         stackexchange.StackExchange,
                         tripit.TripIt,
                         tumblr.Tumblr,
                         twitter.Twitter,
                         vimeo.Vimeo,
                         wordpress.Wordpress,
                         yahoo.Yahoo,
)

alias_map = {}
for service in services:
    alias_map[service.alias] = service

domain_map = {}
for service in services:
    for domain in service.api_domains:
        domain_map[domain] = service
