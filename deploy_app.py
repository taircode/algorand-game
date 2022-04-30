from pyteal import *
from algosdk import account, v2client, mnemonic
from algosdk.future import transaction #note want algosdk.future.transaction not algosdk.transaction - incorrectly thought it was the second one 
import tic_tac_toe
import base64

"""
Following the example here https://developer.algorand.org/docs/get-details/dapps/pyteal/ 
to deploy and call contract
Note you need to use v2client.algod. instead of just algod.
"""

# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn) :
    private_key = mnemonic.to_private_key(mn)
    return private_key

# helper function that formats global state for printing
def format_state(state):
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        formatted_key = base64.b64decode(key).decode('utf-8')
        if value['type'] == 1:
            # byte string
            if formatted_key == 'guest' or formatted_key == 'whose_turn' or formatted_key == 'creator':
                formatted_value = value['bytes']
            else:
                formatted_value = base64.b64decode(value['bytes']).decode('utf-8')
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value['uint']
    return formatted

# helper function to read app global state
def read_global_state(client, app_id):
    app = client.application_info(app_id)
    #app_params = app['params'] #what are all of the params?
    global_state = app['params']['global-state'] if "global-state" in app['params'] else []
    return format_state(global_state)

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

    app_args=["ST5KMIXPPQTFMBIYBIYUVPPY3BIWZAPBTRGUDDHWBG2WF4P4BO6MXRVHGI"]

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

"""
After the app is created, this function calls a Noop transaction that specifies who the creator is challenging.
"""
def assign_challenger():
    pass

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
    global_ints = 0 #had to change these to work for our tic-tac-toe example
    global_bytes = 12 #had to change these to work for our tic-tac-toe example
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
    with open("./deployed/all_deployed.txt","a") as f:
        f.write(str(app_id))

    # read global state of application
    global_state=read_global_state(algod_client, app_id)
    print("Global state:", global_state)
    with open("./deployed/application"+str(app_id)+".txt","a") as f:
        f.write("\n")
        f.write("Global state\n")
        lines=[str(item)+": "+str(val)+"\n" for item, val in global_state.items()]
        f.writelines(lines)
    