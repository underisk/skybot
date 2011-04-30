from util import hook

from brains.namelist.models import Player, Category
from brains.mapping.models import Location, Report
from redis import Redis
import json
import cPickle as pickle

redis = Redis(db=6)


@hook.command('udbfind')
def find_players(fuckers, msg=None, reply=None):
    fuckers = [fucker.strip() for fucker in fuckers.split(',')]
    ids = []
    for player in fuckers:
        try:
            ids.append(Player.objects.get(name=player).id)
        except Exception, e:
            reply("Could not find: {}".format(player))
        
    jerks = Player.objects.filter(id__in=ids)
    for jerk in jerks:
        reply(' - '.join([jerk.name, unicode(jerk.last_known_position())])) 


@hook.command('udbreport')
def get_report(coords):
    coords = [coord.strip() for coord in coords.split(',')]
    report = redis.get('location:{0}:{1}'.format(*coords))
    if report:
        report = json.loads(report)
        age = unicode(datetime.datetime.now() - pickle.loads(report['report_date']))
        return '[{}, {}] - Zombies: {}, Survivors: {}, Barricades: {} ({} ago)'.format(
            coords[0], coords[1], report['zombies'], report['survivor_count'], 
            report['barricades'], age)
    else:
        return "No report for [{},{}]".format(*coords)


@hook.command('udblastreport')
def last_report(ignore):
    try:
        last = Report.objects.order_by('-reported_date',zombies_only=False)[0]
    except Exception, e:
        return "No reports"
    return last


@hook.command('udbmark',adminonly=True)
def mark_player(mark):
    player, category = [val.strip() for val in mark.split('=')]
    try:
        category = Category.objects.get(name=group)
    except Exception, e:
        return "Invalid group"
    try:
        player = Player.objects.get(name=player)
    except Exception, e:
        return "Invalid player" 
    player.category = category
    player.save()
    return "{} changed to {}".format(player, category)


@hook.command('udbtrees')
def find_trees(ignore, say=None):
    trees = [json.loads(tree) for tree in redis.smembers('trees')]
    trees = ['[{},{}]'.format(tree['x'], tree['y']) for tree in trees]
    return "{} trees {}".format(len(trees), ' '.join(trees))
        
    
    