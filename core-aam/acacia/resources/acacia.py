import acacia_atspi
import json
from ua_parser import user_agent_parser

def main(request, response):
    ua_string = request.headers.get("User-Agent").decode("utf-8");
    root = find_browser(ua_string)
    if root.isNull():
      print("Cannot find root accessibility node for %s - did you turn on accessibility?"
            % ua_family);
      return (200, 'could not find %s' % ua_family), [('Content-Type', 'foo/bar')], '{"error": "no data"}'

    test_title = request.GET[b'title'].decode('UTF-8')
    tab = find_tab(root, test_title)
    if not tab:
      print('Cannot find tab for %s'
            % test_title);
      return (200, 'could not find %s' % test_title), [('Content-Type', 'foo/bar')], '{"error": "no data"}'

    test_id = request.GET[b'id'].decode('UTF-8')
    node = find_node(tab, test_id)
    if not node:
        print('Cannot find node for %s' % test_id)
        return (200, 'could not find %s' % test_id), [('Content-Type', 'foo/bar')], '{"error": "no data"}'

    node_dictionary = serialize_node(node);

    return ((200, 'Found'), [('Content-Type', 'text/json')], json.dumps(node_dictionary))

def find_browser(ua_string):
    ua = user_agent_parser.ParseUserAgent(ua_string)
    ua_family = ua["family"];

    print("family: " + ua_family)

    if (ua_family == "HeadlessChrome"):
        ua_family = "chrome"

    # TODO: Is there any other way to get the browser name or PID before this point?
    return acacia_atspi.findRootAtspiNodeForName(ua_family)


def find_tab(root, test_title):
    stack = [root]
    while stack:
        node = stack.pop()

        print("right about to get the role name......")
        if node.getRoleName() == 'document web':
            if (node.getName() == test_title):
                return node
            # Don't continue traversing into documents
            continue

        for i in range(node.getChildCount()):
            child = node.getChildAtIndex(i)
            stack.append(child)

    return None


def find_node(tab, test_id):
    stack = [tab]
    while stack:
        node = stack.pop()

        attributes = node.getAttributes()
        for attribute_pair in attributes:
            [attribute, value] = attribute_pair.split(':', 1)
            if attribute == 'id':
                if value == test_id:
                    return node

        for i in range(node.getChildCount()):
            child = node.getChildAtIndex(i)
            stack.append(child)

    return None

def serialize_node(node):
    node_dictionary = {}
    node_dictionary['role'] = node.getRoleName()
    node_dictionary['name'] = node.getName()
    node_dictionary['description'] = node.getDescription()
    node_dictionary['states'] = sorted(node.getStates())
    node_dictionary['interfaces'] = sorted(node.getInterfaces())
    node_dictionary['attributes'] = sorted(node.getAttributes())

    # TODO: serialize other attributes

    return node_dictionary
