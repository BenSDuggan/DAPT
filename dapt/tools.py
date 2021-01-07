"""
.. _tools:

Tools
=====

A collection of tools that make DAPT easy to use, especially with `PhysiCell <http://physicell.org/>`_.  The ``sample_db`` and ``create_settings_file()`` methods are helpful with anyone using DAPT.  The rest of the methods are used specifically for PhysiCell pipelines.
"""

import xml.etree.ElementTree as ET
import sys, os, platform, zipfile, datetime, time, argparse, logging, csv
from .db.delimited_file import Delimited_file

# Start General tools

def sample_db(file_name='sample_db.csv', delimiter=','):
    """
    .. _sample-db:
    
    Create a sample `Delimited_file` database.  The sample table is shown below.  This method will create a file specified in the `file_name` attribute using the delimiter specified by `delimiter`.

    +----+------------------+------------------+----------+----+-----+---+
    | id | start-time       | end-time         | status   | a  | b   | c |
    +----+------------------+------------------+----------+----+-----+---+
    | t1 | 2019-09-06 17:23 | 2019-09-06 17:36 | finished | 2  | 4   | 6 |
    +----+------------------+------------------+----------+----+-----+---+
    | t2 |                  |                  |          | 10 | 10  |   |
    +----+------------------+------------------+----------+----+-----+---+
    | t3 |                  |                  |          | 10 | -10 |   |
    +----+------------------+------------------+----------+----+-----+---+

    Args:
        file_name (str): the file name of the file to create and use for the database.  The default value is `sample_db.csv`.
        delimiter (str): the delimiter to use for the file.  The default is a `,`.

    Returns:
        A `Delimited_file` object using the file_name specified.
    """

    with open(file_name, 'w') as f:
        writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=['id', 'start-time', 'end-time', 'status', 'a', 'b', 'c'])
        writer.writeheader()
        writer.writerow({'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':'2', 'b':'4', 'c':'6'})
        writer.writerow({'id':'t2', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'10', 'c':''})
        writer.writerow({'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'-10', 'c':''})
    
    return Delimited_file(file_name, delimiter=delimiter)

def create_settings_file(parameters, pid=None):
    """
    Creates a file where each line contains a key from the parameters and its associated key, separated by a semicolon.

    Args:
        parameters (dict): the paramaters to be saved in the file
        pid (str): the parameter id of the current parameter run.  If you don't give an id then the id in ``parameters`` will be used.
    """

    data = ""

    if not pid:
        pid = parameters["id"]

    for key in parameters:
        data += str(key) + ":" + str(parameters[key]) + "\n"

    with open(str(parameters["id"]) + "_dapt_param_settings.txt", 'w') as file:
        file.writelines(data)

# Start PhysiCell tools

def create_XML(parameters, default_settings="PhysiCell_settings_default.xml", save_settings="PhysiCell_settings.xml", off_limits=[]):
    """
    Create a PhysiCell XML settings file given a dictionary of paramaters.  This function works by having a ``default_settings`` file which contains the generic XML structure.  Each key in ``parameters` then contains the paths to each XML tag in the ``default_settings`` file.  The value of that tag is then set to the value in the associated key.  If a key in ``parameters`` does not exist in the ``default_settings`` XML file then it is ignored.  If a key in ``parameters`` also exists in ``off_limits`` then it is ignored.

    Args:
        paramaters (dict): A dictionary of paramaters where the key is the path to the xml variable and the value is the desired value in the XML file.
        default_settings (str): the path to the default xml file
        save_settings (str): the path to the output xml file
        off_limits (list): a list of keys that should not be inserted into the XML file.
    """

    parameters = dict(parameters)
    tree = ET.parse(default_settings)
    root = tree.getroot()

    for key in parameters:
        if key in off_limits:
            next

        node = root.find(key)

        if node != None:
            node.text = str(parameters[key])

    tree.write(save_settings)

def data_cleanup(config=None):
    """
    Emulating make data-cleanup-light: remove .mat, .xml, .svg, .txt, .pov.  You can optionally remove zipped files by setting ``remove-zip`` equal to ``True`` or remove ``*.mp4`` by setting ``remove-movie`` to ``True`` in the config file.

    Args:
        config (Config): A config object, optionally given.
    """

    for file in os.listdir("."):
        if file.endswith(".mat") or file.endswith(".xml") or file.endswith(".svg") or file.endswith(".txt") or file.endswith(".pov") or file.endswith(".png"):
            os.remove(file)
        elif config:
            if (config.get_value('remove-zip', recursive=True) and file.endswith('.zip')) or (config.get_value('remove-movie', recursive=True) and file.endswith('.mp4')):
                os.remove(file)

    for file in os.listdir("output/"):
        if file.endswith(".mat") or file.endswith(".xml") or file.endswith(".svg") or file.endswith(".txt") or file.endswith(".png"):
            os.remove("output/" + file)
        elif config:
            if (config.get_value('remove-zip', recursive=True) and file.endswith('.zip')) or (config.get_value('remove-movie', recursive=True) and file.endswith('.mp4')):
                os.remove("output/" + file)

def create_zip(pid):
    """
    Zip all of the important PhysiCell items.

    Args:
        pid (str): the id of the current parameter run

    Returns:
        The name of the zipped file
    """

    fileName = str(pid) + '_test_' + datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') + '.zip'
    # Create the zip
    zip = zipfile.ZipFile(fileName, 'w')

    # Add individual files
    zip.write(str(pid) + "_dapt_param_settings.txt", compress_type=zipfile.ZIP_DEFLATED)

    # Add files in output
    for folder, subfolders, files in os.walk('output/'):
        for file in files:
            if ".png" not in file:
                zip.write(os.path.join(folder, file), 'output/'+file, compress_type = zipfile.ZIP_DEFLATED)

    # Add programming files
    zip.write('config/PhysiCell_settings.xml', compress_type = zipfile.ZIP_DEFLATED)
    zip.write('main*.cpp', compress_type = zipfile.ZIP_DEFLATED)
    zip.write('Makefile', compress_type = zipfile.ZIP_DEFLATED)
    zip.write('custom_modules/*', compress_type = zipfile.ZIP_DEFLATED)

    zip.close()

    return fileName



'''
def parse():
    """


    """

    print('DEPRECATED: DO NOT USE!')

    parser = argparse.ArgumentParser(description='Distributed Automated Parameter Testing (DAPT)\nA library to assist with running parameter sets across multiple systems.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--f', metavar='config.json', default='config.json', type=str, action='store', help="The path to the config file.")
    parser.add_argument('--r', action='store_true', help="Reset the config file.  \'last-test\':None")
    parser.add_argument('--c', action='store_true', help="Create a blank config file.")
    parser.add_argument('--s', action='store_true', help="Remove keys from the config file so it can be made public.")

    args = parser.parse_args()
    if args.r:
        # Remove last-test from config file
        conf = Config(args.f)
        if conf.config['last-test']:
            conf.config['last-test'] = None
        #if conf.config['performed-by']:
        #    conf.config['performed-by'] = None
        conf.update()
        exit()
    if args.c:
        # Reset config file
        #Config.create(args.f)
        exit()
    if args.s:
        # Safe config file
        Config.safe(args.f)
        exit()
'''