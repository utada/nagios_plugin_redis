#!/usr/bin/env python26

import os
import sys
import socket
import argparse
import redis

class Redis_check:
  nagios_codes = dict(OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3, DEPENDENT=4)

  def nagios_return(self, code, response):
    print (code+': '+response)

  def opt_parse(self):
    parser = argparse.ArgumentParser(description="redis check nagios plugin")
    parser.add_argument('-H', dest='hostname', default='localhost', help='hostname (default: %(default)s)')
    parser.add_argument('-P', dest='port', default='6379', help='port (default: %(default)s)')
    parser.add_argument('-p', dest='password', help='password (default: %(default)s)')

    return parser.parse_args()

  def main(self):
    args = self.opt_parse()
    self.redis_connect(args)

  def redis_connect(self, args):
    try:
      redis_conn = redis.Redis(host=args.hostname, port=int(args.port), password=args.password)
      info = redis_conn.info()
    except (socket.error,
            redis.exceptions.ConnectionError), e:
      self.nagios_return('CRITICAL', str(repr(e)))
    self.nagios_return('OK', 'Connect '+args.hostname+':'+args.port+' Redis version is '+info['redis_version'])
    sys.exit(self.nagios_codes['CRITICAL'])

if __name__ == "__main__":
  Redis_check().main()

