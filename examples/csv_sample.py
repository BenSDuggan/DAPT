# Example DAPT with csv

import dap
import os, sys

sheet = dap.delimited_file.Delimited_file('test.csv', ',')
ap = dap.param.Param(sheet)


while True:
    parameters = ap.requestParameters() #Get the next parameter
    if parameters == None:
        print("No more parameters to run!")
        break

    print("Request parameters: ")
    print(parameters)

    ap.parameterSuccessful(parameters["id"])


    try:
        if 'clean' in parameters['tasks']:
            # Reset from the previous run
            print("Cleaning up folder")
            dap.tools.dataCleanup(conf.config)
            ap.updateStatus(parameters['id'], 'clean')

        # Update sheets to mark the test is finished
        ap.parameterSuccessful(parameters["id"]) #Test completed successfully so we need to mark it as such

        # End tests
    except ValueError:
        # Test failed
        print(ValueError)
        print("Test failed")
        ap.parameterFailed(parameters["id"])

