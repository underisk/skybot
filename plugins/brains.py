from util import hook

from brains.namelist.models import Player, Category
from brains.mapping.models import Location, Report
from redis import Redis
import json

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
    try:
        loc = Location.objects.get(x=coords[0], y=coords[1])
        report = loc.report_set.order_by('reported_date')[0]
    except Exception, e:
        return "No reports"
    return report


@hook.command('udblastreport')
def last_report(ignore):
    try:
        last = Report.objects.order_by('reported_date')[0]
    except Exception, e:
        return "No reports"
    return last


@hook.command('udbmark',adminonly=True)
def mark_player(mark):
    player, group = [val.strip() for val in mark.split('=')]
    try:
        group = Category.objects.get(name=group)
    except Exception, e:
        return "Invalid group"
    try:
        player = Player.objects.get(name=player)
    except Exception, e:
        return "Invalid player"    
    return "{} changed to {}".format(player, group)


@hook.command('udbtrees')
def find_trees(ignore, say=None):
    trees = [json.loads(tree) for tree in redis.smembers('trees')]
    trees = ['[{},{}]'.format(tree['x'], tree['y']) for tree in trees]
    return "{} trees {}".format(len(trees), ' '.join(trees))
        
    
    