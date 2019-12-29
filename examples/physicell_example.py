"""
PhysiCell Example
=================

This file shows an example workflow with PhysiCell.  This example was taken from the `AMIGOS Invasion <https://github.com/MathCancer/AMIGOS-invasion>`_ project.
"""

import xml.etree.ElementTree as ET
import sys,os,platform,zipfile,datetime, time
import dapt


def main():
    conf = dapt.config.Config('DAPT/config.json')
    sheet = dapt.sheets.Sheet(conf.config['spreedsheet-id'], 'DAPT/credentials.json')
    ap = dapt.param.Param(sheet, conf)
    boxy = dapt.box.Box(config = conf)
    boxy.connect()

    print("Starting main script")

    while True:
        # Check the sheet for any trials that didn't run successfully
        #ap.checkForDBErrors()

        parameters = ap.next_parameters() #Get the next parameter
        if parameters == None:
            print("No more parameters to run!")
            break

        print("Request parameters: ")
        print(parameters)

        try:
            if 'clean' in parameters['tasks']:
                # Reset from the previous run
                print("Cleaning up folder")
                dapt.tools.data_cleanup(conf)
                ap.update_status(parameters['id'], 'clean')

            if 'xml' in parameters['tasks']:
                # Create the parameters
                print("Creating parameters xml and autoParamSettings.txt")
                dapt.tools.create_XML(parameters, default_settings="config/PhysiCell_settings_default.xml", save_settings="config/PhysiCell_settings.xml")
                dapt.tools.create_settings_file(parameters)
                ap.update_status(parameters['id'], 'xml')

            if 'sim' in parameters['tasks']:
                # Run PhysiCell
                print("Running test")
                if platform.system() == 'Windows':
                    os.system("AMIGOS-invasion.exe")
                else:
                    os.system("./AMIGOS-invasion")
                ap.update_status(parameters['id'], 'sim')

            if 'matlab' in parameters['tasks']:
                # Run matlab scripts
                print("Run matlab scripts")
                print("^^ not implimented ^^")

            if 'imgProc' in parameters['tasks']:
                # Run image processing
                print("Run image processing")
                fileName = str(parameters['id']) + '_test_' + datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') + str('.mp4')
                print(fileName)
                os.chdir('output/')
                os.system('mogrify -format png *.svg')
                movie_run_command_str = str('ffmpeg -framerate 24 -i snapshot%08d.png -pix_fmt yuv420p -vf pad="width=ceil(iw/2)*2:height=ceil(ih/2)*2" ../')
                movie_run_command_str = movie_run_command_str + fileName
                os.system(movie_run_command_str)
                os.chdir('../')

            if 'zip' in parameters['tasks']:
                # Zip Run output
                print("Zipping SVG and outputs")
                zipName = dapt.tools.create_zip(parameters["id"])
                ap.update_status(parameters['id'], 'zip')

            if 'upload' in parameters['tasks']:
                # Upload zip to box
                print("Uploading zip to box")
                print(zipName)
                if platform.system() == 'Windows':
                    print(boxy.uploadFile(conf.config['boxFolderID'], '\\', fileName))
                    print(boxy.uploadFile(conf.config['boxFolderZipID'], '\\', zipName))
                else:
                    print(boxy.uploadFile(conf.config['boxFolderID'], '/'+fileName, fileName))
                    print(boxy.uploadFile(conf.config['boxFolderZipID'], '/'+fileName, zipName))

                ap.update_status(parameters['id'], 'upload')

            # Update sheets to mark the test is finished
            ap.successful(parameters["id"]) #Test completed successfully so we need to mark it as such
            
            # End tests
        except ValueError:
            # Test failed
            print(ValueError)
            print("Test failed")
            ap.failed(parameters["id"], ValueError)
        
if __name__ == '__main__':
    os.chdir("../")
    print("Current working directory: ", os.getcwd())

    main()