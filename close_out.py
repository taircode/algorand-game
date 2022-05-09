import argparse
from algosdk import v2client, account, transaction, encoding, logic
from algosdk.future import transaction

from helper import get_private_key_from_mnemonic


"""
This is the main function to call in order to close-out the smart contract
Don't need close-out functionality yet, but maybe in the future
"""
# create new application. This function creates the application creation transaction, signs, and sends it.
def close_out_app(client, private_key, app_id):
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

# user declared account mnemonics
#you should never save mnemonic like this in production. Just using on testnet for now.
#figure out a safer way to do this for mainnet
creator_mnemonic = "cushion raccoon snap tragic come seat rhythm canal clarify oven pipe misery maid mutual gossip real flat snake witness achieve concert wrestle praise abstract hundred" 
# user declared algod connection parameters.
# Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

"""
Main script to close-out the app on the blockchain
"""
if __name__=='__main__':
    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address) #want v2client here or do from algosdk.v2client import algod

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    print("--------------------------------------------")
    print("Deploying Tic-Tac-Toe application......")

    # create new application
    app_id = close_out_app(algod_client, creator_private_key)