from pyteal import *
from algosdk import account, v2client, mnemonic
from algosdk.future import transaction #note want algosdk.future.transaction not algosdk.transaction - incorrectly thought it was the second one 
import base64
import argparse
from helper import get_private_key_from_mnemonic, read_global_state
#from algosdk.encoding import decode_address, encode_address

"""
This is the main function to call in order to take a turn
"""
# create new application. This function creates the application creation transaction, signs, and sends it.
def take_turn(client, private_key, app_id, location):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    #the only argument we need is the location of your move
    app_args=[location]

    #you need to pass the address that is not the transaction sender
    accounts=[other_address]

    #which app are you playing on
    index=app_id

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, index, app_args, accounts)

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

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    #app_id = transaction_response['application-index']
    with open("./deployed/application"+str(app_id)+".txt", "a") as f:
        f.write("TXID: "+str(tx_id))
        f.write("\n")
        f.write("Result confirmed in round: {}".format(transaction_response['confirmed-round']))
        f.write("\n")
        f.write("app-id: "+str(app_id))
        f.write("\n")

    return app_id

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
    parser.add_argument("--whose_turn",default="creator",choices=["creator","guest"],help="select whose turn it is, creator or guest.")
    parser.add_argument("--location",choices=["C","N","E","S","W","NE","SE","NW","SW"],help="select the location for your move.")
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
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic[args.whose_turn])

    #get the addresses of the account who is not sending the current transaction
    other_private_key = get_private_key_from_mnemonic(creator_mnemonic['guest']) if args.whose_turn == 'creator' else get_private_key_from_mnemonic(creator_mnemonic['creator'])
    other_address = account.address_from_private_key(other_private_key)

    print("--------------------------------------------")
    print("Take a turn in Tic-Tac-Toe application......")

    # create new application
    take_turn(algod_client, creator_private_key, app_id, args.location, other_address)

    # read global state of application
    global_state=read_global_state(algod_client, app_id)
    print("Global state:", global_state)
    with open("./deployed/application"+str(app_id)+".txt","a") as f:
        f.write("\n")
        f.write("Global state\n")
        lines=[str(item)+": "+str(val)+"\n" for item, val in global_state.items()]
        f.writelines(lines)
    