import argparse
from algosdk import v2client, account, transaction, encoding, logic
from algosdk.future import transaction

from helper import get_private_key_from_mnemonic


"""
This is the function to use for the creator and guest to place their bets into the deployed tic-tac-toe smart contract.
"""
def send_payment(algod_client, private_key, amt, rcv):
    sender = account.address_from_private_key(private_key)
    print(f"sender is {sender}")

    params = algod_client.suggested_params()
    
    txn = transaction.PaymentTxn(sender, params, rcv, amt)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    algod_client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        pmtx = transaction.wait_for_confirmation(algod_client, tx_id, 5)
        print("TXID: ", tx_id)
        print("Result confirmed in round: {}".format(pmtx['confirmed-round']))

    except Exception as err:
        print(err)
        return
        
    return pmtx


creator_mnemonic = {
    "creator":"cushion raccoon snap tragic come seat rhythm canal clarify oven pipe misery maid mutual gossip real flat snake witness achieve concert wrestle praise abstract hundred",
    "guest":"ill captain pluck horn reduce stadium logic such short empty install analyst again final ladder marine push ask clerk shrug toe zoo seat abstract fee"
}
# user declared algod connection parameters.
# Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--app_id",default="latest",help="provide an app_id, otherwise app_id of most recently deployed is used.")
    parser.add_argument("--algo_amount",default=3,help="specify how much algo you want to send.")
    args = parser.parse_args()

    algo_amount=int(args.algo_amount)

    #get the app id from args or from file
    if args.app_id=='latest':
        with open("./all_deployed.txt","r") as f:
            for line in f:
                pass
            app_id=int(line)
    else:
        app_id=int(args.app_id)

    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address) #want v2client here or do from algosdk.v2client import algod

    #get address of the application
    print(f"app_id is {app_id}")
    app_address=logic.get_application_address(app_id)
    print(f"app address is {app_address}")

    _future_fee=10**3

    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic['creator'])
    pmtx_creator = send_payment(algod_client, creator_private_key, algo_amount*(10**6)+_future_fee, app_address)

    guest_private_key = get_private_key_from_mnemonic(creator_mnemonic['guest'])
    pmtx_creator = send_payment(algod_client, guest_private_key, algo_amount*(10**6), app_address)


    