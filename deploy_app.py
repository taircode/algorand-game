from pyteal import *
from algosdk import account, v2client
from algosdk.future import transaction #note want algosdk.future.transaction not algosdk.transaction - incorrectly thought it was the second one 
import tic_tac_toe
import base64
from algosdk.encoding import decode_address, encode_address
from helper import get_private_key_from_mnemonic, read_global_state

"""
Following the example here https://developer.algorand.org/docs/get-details/dapps/pyteal/ 
to deploy and call contract
Note you need to use v2client.algod. instead of just algod.
"""

# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

"""
This is the main function to call in order to deploy the smart contract
"""
# create new application. This function creates the application creation transaction, signs, and sends it.
def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()

    #amount you want to bet
    bet_amount=3
    #Integers in algorand are almost always uint64, sometimes its required to encode them as bytes. 
    #For example when passing them as application arguments in an ApplicationCallTransaction. 
    #When encoding an integer to pass as an application argument, the integer should be encoded as the big endian 8 byte representation of the integer value.
    encoded_bet_amount=(bet_amount).to_bytes(8,'big')

    #you have to decode the address to get the pk
    #algorand applications store "addresses" as pk's like this one
    creator_address="4NVPTGTJQLCGN7QFVH4WCZATFXE6RXGI6QZQYTC5DPW5C4O5BUCEGTC3BA"
    creator_pk = decode_address(creator_address)
    guest_address="ST5KMIXPPQTFMBIYBIYUVPPY3BIWZAPBTRGUDDHWBG2WF4P4BO6MXRVHGI"
    guest_pk = decode_address(guest_address)

    #here are the app_args
    app_args=[creator_pk,guest_pk,encoded_bet_amount]

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(sender, params, on_complete, approval_program, clear_program, global_schema, local_schema, app_args)

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
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)
    with open("./deployed/application"+str(app_id)+".txt", "w") as f:
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
creator_mnemonic = "cushion raccoon snap tragic come seat rhythm canal clarify oven pipe misery maid mutual gossip real flat snake witness achieve concert wrestle praise abstract hundred" 
# user declared algod connection parameters.
# Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

"""
Main script to create the app on the blockchain and then view its global state
"""
if __name__=='__main__':
    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address) #want v2client here or do from algosdk.v2client import algod

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 1 #had to change these to work for our tic-tac-toe example
    global_bytes = 13 #had to change these to work for our tic-tac-toe example
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # compile program to TEAL assembly
    with open("./approval.teal", "w") as f:
        approval_program_teal = tic_tac_toe.get_approval_program()
        f.write(approval_program_teal) #we don't techinically need to write it right? this is just to have a record?

    # compile program to TEAL assembly
    with open("./clear.teal", "w") as f:
        clear_state_program_teal = tic_tac_toe.get_clear_state_program()
        f.write(clear_state_program_teal) #we don't techinically need to write it right? this is just to have a record?

    # compile program to binary from teal source code
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    # compile program to binary from teal source code
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("--------------------------------------------")
    print("Deploying Tic-Tac-Toe application......")

    # create new application
    app_id = create_app(algod_client, creator_private_key, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)
    #add app_id to a running list of all apps ever deployed
    with open("./all_deployed.txt","a") as f:
        f.write("\n")
        f.write(str(app_id))

    # read global state of application
    global_state=read_global_state(algod_client, app_id)
    print("Global state:", global_state)
    with open("./deployed/application"+str(app_id)+".txt","a") as f:
        f.write("\n")
        f.write("Global state\n")
        lines=[str(item)+": "+str(val)+"\n" for item, val in global_state.items()]
        f.writelines(lines)
    