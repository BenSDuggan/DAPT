# Example DAPT with csv

import dap
import os, sys

sheet = dap.delimited_file.Delimited_file('test.csv', ',')
ap = dap.param.Param(sheet)


while True:
    parameters = ap.next_parameters() #Get the next parameter
    if parameters == None:
        print("No more parameters to run!")
        break

    print("Request parameters: ")
    print(parameters)

    ap.successful(parameters["id"])


    try:
        ap.update_status(parameters['id'], 'clean')

        # Update sheets to mark the test is finished
        ap.successful(parameters["id"]) #Test completed successfully so we mark it as such

        # End tests
    except ValueError:
        # Test failed
        print(ValueError)
        print("Test failed")
        ap.failed(parameters["id"], str(ValueError))

