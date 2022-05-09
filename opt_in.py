from pyteal import *
from algosdk import account, v2client, mnemonic
from algosdk.future import transaction #note want algosdk.future.transaction not algosdk.transaction - incorrectly thought it was the second one 
import base64
import argparse
from helper import get_private_key_from_mnemonic, read_global_state
#from algosdk.encoding import decode_address, encode_address

"""
This is the main function to opt-in to the application
"""
# create new application. This function creates the application creation transaction, signs, and sends it.
def opt_in(client, private_key, app_id):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    #which app are you playing on
    index=app_id

    # create unsigned transaction
    txn = transaction.ApplicationOptInTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        transaction_response = transaction.wait_for_confirmation(client, tx_id, 4)
        print("TXID: ", tx_id)
        print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))

    except Exception as err:
        print(err)
        return

# user declared account mnemonics
#you should never save mnemonic like this in production. Just using on testnet for now.
#figure out a safer way to do this for mainnet
creator_mnemonic = {
    "creator":"cushion raccoon snap tragic come seat rhythm canal clarify oven pipe misery maid mutual gossip real flat snake witness achieve concert wrestle praise abstract hundred",
    "guest":"ill captain pluck horn reduce stadium logic such short empty install analyst again final ladder marine push ask clerk shrug toe zoo seat abstract fee"
}

# user declared algod connection parameters.
# Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

"""
Main script to take a turn in an existing tic-tac-toe app
"""
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--who",default="both",choices=["both","creator","guest"],help="select who is opting in.")
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

    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address)

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic["creator"])
    guest_private_key = get_private_key_from_mnemonic(creator_mnemonic["guest"])

    print("--------------------------------------------")
    print("Opting-in to Tic-Tac-Toe application......")

    # opt_in to application
    if args.who=='both':
        opt_in(algod_client, creator_private_key, app_id)
        opt_in(algod_client, guest_private_key, app_id)
    elif args.who=='creator':
        opt_in(algod_client, creator_private_key, app_id)
    else:
        opt_in(algod_client, guest_private_key, app_id)
    

    # read global state of application
    global_state=read_global_state(algod_client, app_id)
    print("Global state:", global_state)
    
    