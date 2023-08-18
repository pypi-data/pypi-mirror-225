
import os
import sys
import yaml
import argparse


class ServerConfig:
    # Host configuration
    host = '0.0.0.0'
    port = 9999

    # Runtime settings
    working = "."
    plugins = []

    # Optional: Define the default route hander as one of the following
    static = None
    proxy = None

    discover = True
    routes = {}


def GetConfig():
    opts = GetArgs()
    config = ServerConfig()

    # Try and load from config file (if specified)
    if opts.config and os.path.isfile(opts.config):
        ApplyYamlConfig(config, opts.config)

    # Apply and load additional config settings
    ApplyArgs(config, opts)  # <-- Apply CLI args to config
    PrintConfig(config)

    # Apply any CLI args and return the config
    return config


def GetArgs(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='Extremely simple python server that can be easily be extended.'
    )

    # Core configurations and valiables used by all server types
    parser.add_argument('-c', '--config',
                        dest='config',
                        help='Specify your `config.yaml` file.',
                        )
    parser.add_argument('--host',
                        dest='host',
                        help='Specify the host we will bind the server to',
                        default='0.0.0.0'
                        )
    parser.add_argument('-p', '--port',
                        dest='port',
                        help='serve HTTP requests on specified port (default: 9999)',
                        type=int,
                        default=9999
                        )
    parser.add_argument('-w', '--working',
                        dest='working',
                        help='Specify the working directory',
                        default=os.getenv('WORK_DIR')
                        )

    # Allow the loading of plugins
    parser.add_argument('-a', '--add',
                        dest='plugins',
                        help='List of plugins to load',
                        type=lambda s: [item for item in s.split(',')])

    # Allow the user to specify the type of server that will be created
    parser.add_argument('-s', '--static',
                        dest='static',
                        help='Static web contents to serve, if no other route defined',
                        # Default option: Serve current dir...
                        default=os.getenv('STATIC_DIR', '')
                        )
    parser.add_argument('--proxy',
                        dest='proxy',
                        help='Default route handler will reverse proxy to a URL'
                        )

    # Parse the args provided by the CLI
    args = parser.parse_args(argv)

    return args


def ApplyArgs(config, args):
    for key, val in vars(args).items():
        if val and key != "config":
            setattr(config, key, val)
    return config


def ApplyYamlConfig(config, file):
    with open(file, "r") as stream:
        configDict = yaml.safe_load(stream)
        for key in configDict.keys():
            setattr(config, key, configDict[key])


def printIf(message, value=None):
    if value:
        print(message % value)


def PrintConfig(config):
    print('---------------------------------------------------------')
    print('Starting python server...')
    print('---------------------------------------------------------')
    printIf(' + Work Dir: %s', config.working)
    printIf(' + Live Dir: %s', config.static)
    printIf(' ~ Proxy To: %s', config.proxy)
    print(' - Hostname: http://%s:%s' % (config.host, config.port))
    print('---------------------------------------------------------')
