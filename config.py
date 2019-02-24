import yaml

with open('config.yml', 'r') as ymlfile:
    config = yaml.load(ymlfile)

craps_fig = config['craps']

