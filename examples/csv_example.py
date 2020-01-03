import dapt
import os, sys, csv


def create_file():
    # Reset csv.  This is just used update the csv and reset it so interesting things happen.
    
    with open('test.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'startTime', 'endTime', 'status', 'a', 'b', 'c'])
        writer.writeheader()
        writer.writerow({'id':'t1', 'startTime':'2019-09-06 17:23', 'endTime':'2019-09-06 17:36', 'status':'finished', 'a':'2', 'b':'4', 'c':'6'})
        writer.writerow({'id':'t2', 'startTime':'', 'endTime':'', 'status':'', 'a':'10', 'b':'10', 'c':''})
        writer.writerow({'id':'t3', 'startTime':'', 'endTime':'', 'status':'', 'a':'10', 'b':'-10', 'c':''})


def main():
    create_file()

    db = dapt.Delimited_file('test.csv')
    ap = dapt.Param(db)
        
    while True:
        parameters = ap.next_parameters() #Get the next parameter
        if parameters == None:
            print("No more parameters to run!")
            break

        print("Request parameters: ")
        print(parameters)

        ap.successful(parameters["id"])


        try:
            ap.update_status(parameters['id'], 'Adding and inserting')

            c = int(parameters['a']) + int(parameters['b'])
            db.update_cell(db.get_row_index('id', parameters['id']), 'c', c)

            # Update sheets to mark the test is finished
            ap.successful(parameters["id"]) #Test completed successfully so we mark it as such

            # End tests
        except ValueError:
            # Test failed
            print(ValueError)
            print("Test failed")
            ap.failed(parameters["id"], str(ValueError))

if __name__ == '__main__':
    main()