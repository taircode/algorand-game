
from algosdk import v2client
from helper import read_global_state
import argparse


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--app_id",default="latest",help="provide an app_id, otherwise app_id of most recently deployed is used.")
    args = parser.parse_args()

    #you could actually read global state from the app here, and see if it matches whose_turn

    #get the app id from args or from file
    if args.app_id=='latest':
        with open("./all_deployed.txt","r") as f:
            for line in f:
                pass
            app_id=int(line)
    else:
        app_id=int(args.app_id)

    # user declared algod connection parameters.
    # Node must have EnableDeveloperAPI set to true in its config
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address)

    # read global state of application
    global_state=read_global_state(algod_client, app_id)
    print("Global state:", global_state)