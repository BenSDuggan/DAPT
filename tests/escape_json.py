# A script to export JSON files as an escaped strings so Travis.CI will work with them.
# The script needs the path to the JSON file (json_path) and save path (escaped_path).
# The script can be ran in 2 ways:
#   1) You can provide the paths directly by modifying the json_path and escape_path variables
#   2) You can provide the values as sys args json_path then escape_path

import json
import sys

json_path = ''
escaped_path = ''

# Resolve proper paths
if len(sys.argv) >= 3:
    json_path = sys.argv[1]
    escaped_path = sys.argv[2]

with open(json_path, 'r') as f:
    json_file = f.read()

json_as_string = json.loads(json_file)

escaped_json_string = json.dumps(json_as_string)

with open(escaped_path, 'w') as f:
    json.dump(escaped_json_string, f)
