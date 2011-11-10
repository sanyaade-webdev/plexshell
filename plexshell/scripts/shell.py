from plexshell import PlexShell
from socket import error as SocketError
import argparse
import os


def shell_loop(args, stdin):
    should_exit = False
    while not should_exit:
        try:
            client = PlexShell(args.host, args.port, stdin = stdin)
            client.cmdloop()
            should_exit = True
        except KeyboardInterrupt:
            should_exit = True
        except SocketError, e:
            print e


def main():
    parser = argparse.ArgumentParser(
        description = "A interactive command line PMS client")
    parser.add_argument(
        "-H", "--host",
        metavar = "hostname",
        nargs = "?",
        default = "localhost")
    parser.add_argument(
        "-p", "--port",
        metavar = "portno",
        nargs = "?",
        type = int,
        default = 32400)
    parser.add_argument(
        "script",
        metavar = "scriptpath",
        nargs = "?",
        default = None)
    args = parser.parse_args()
    stdin = None
    if args.script:
        if not os.path.isfile(args.script):
            print "Script does not exist: %s" % args.script
            exit(1)
        stdin = open(args.script)
    shell_loop(args, stdin)


if __name__ == "__main__":
    main()
