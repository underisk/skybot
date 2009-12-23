"dotnetpad.py: by sklnd, because gobiner wouldn't shut up"

import urllib
import httplib
import socket
import json

from util import hook


def dotnetpad(lang, code):
    "Posts a provided snippet of code in a provided langugage to dotnetpad.net"

    code = code.encode('utf8')
    params = urllib.urlencode({'language': lang, 'code': code})

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    try:
        conn = httplib.HTTPConnection("dotnetpad.net:80")
        conn.request("POST", "/Skybot", params, headers)
        response = conn.getresponse()
    except httplib.HTTPException:
        conn.close()
        return 'error: dotnetpad is broken somehow'
    except socket.error:
        return 'error: unable to connect to dotnetpad'

    try:
        result = json.loads(response.read())
    except ValueError:
        conn.close()
        return 'error: dotnetpad is broken somehow'

    conn.close()

    if result['Errors']:
        return 'First error: %s' % (result['Errors'][0]['ErrorText'])
    elif result['Output']:
        return result['Output'].lstrip()
    else:
        return 'No output'


@hook.command
def fs(inp):
    ".fs -- post a F# code snippet to dotnetpad.net and print the results"

    if not inp:
        return fs.__doc__

    return dotnetpad('fsharp', inp)


@hook.command
def cs(snippet):
    ".cs -- post a C# code snippet to dotnetpad.net and print the results"

    if not snippet:
        return cs.__doc__
    
    file_template = ('using System; '
                     'using System.Linq; '
                     'using System.Collections.Generic; '
                     'using System.Text; '
                     '%(class)s')

    class_template = ('public class Default '
                      '{ '
                      '    %(main)s '
                      '}')

    main_template = ('public static void Main(String[] args) '
                     '{ '
                     '    %(snippet)s '
                     '}')

    # There are probably better ways to do the following, but I'm feeling lazy
    # if no main is found in the snippet, then we use the template with Main in it
    if 'public static void Main' not in snippet:
        code = main_template % { 'snippet': snippet }
        code = class_template % { 'main': code }
        code = file_template % { 'class' : code }

    # if Main is found, check for class and see if we need to use the classed template
    elif 'class' not in snippet:
        code = class_template % { 'main': snippet }
        code = file_template % { 'class' : code }

        return 'Error using dotnetpad'
    # if we found class, then use the barebones template
    else:
        code = file_template % { 'class' : snippet }

    return dotnetpad('csharp', code)
