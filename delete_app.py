import argparse
import base64
from algosdk import account, v2client, mnemonic
from algosdk.future import transaction

"""
Main script to delete an app on the algorand (testnet) blockchain and then view its global state
"""


# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn) :
    private_key = mnemonic.to_private_key(mn)
    return private_key

# user declared account mnemonics
#you should never save mnemonic like this in production. Just using on testnet for now.
#figure out a safer way to do this for mainnet
creator_mnemonic = "cushion raccoon snap tragic come seat rhythm canal clarify oven pipe misery maid mutual gossip real flat snake witness achieve concert wrestle praise abstract hundred" 
# user declared algod connection parameters.
# Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

"""
This is the main function to call in order to delete the smart contract
"""
# create new application. This function creates the application creation transaction, signs, and sends it.
def delete_app(client, private_key, app_id):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    #application id to delete
    index=app_id

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(sender, params, index)

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
    print(transaction_response)

if __name__=='__main__':

    #parser = argparse
    #parser.add_argument()
    #parser.parse_args()

    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address) #want v2client here or do from algosdk.v2client import algod

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    #app-id to be deleted
    #app_id=86872612 #first one deployed
    #app_id=86875673 #second one deployed
    app_id=86875859 #third one deployed

    print("--------------------------------------------")
    print("Deleting Tic-Tac-Toe application with id "+str(app_id))

    # delete application
    delete_app(algod_client, creator_private_key, app_id)

    #print("--------------------------------------------")
    #print("Reading global state of Tic-Tac-Toe application......")

    # read global state of application
    #print("Global state:", read_global_state(algod_client, app_id))