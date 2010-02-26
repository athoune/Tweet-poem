Tweet can be poem too

Install
=======

Download source http://github.com/athoune/Tweet-poem/archives/master

Unzip it

In Terminal, go into the folder::

  python setup.py build
  sudo python setup.py install

If you are using python 2.5 (default in Unbuntu LTS and Leopard)::

  sudo python ez_setup simplejson

Usage
=====

You can now use the command line tool::

  tweetpoem

You are asked for tweeter login and password

Test
====

http://poem.garambrogne.net

Server
======

You can use it as a web server. The server use Tornado (you need to install it http://www.tornadoweb.org/) and Redis.
Launch one web server per core, and use nginx or lighttpd for loadbalance.

Start it::

  cd src/tweetpoem
  python server.py 8888

In an other terminal::

  cd src/tweetpoem
  python pusher.py