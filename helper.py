from algosdk import mnemonic
from algosdk.encoding import decode_address, encode_address
import base64

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
            if formatted_key=='winner':
                decoded_bytes = base64.b64decode(value['bytes'])
                if decoded_bytes==b'pending' or decoded_bytes==b'tie':
                    formatted_value=decoded_bytes.decode('utf-8')
                else:
                    #formatted_value is a decoded algorand pk address
                    formatted_value=encode_address(decoded_bytes)
            elif formatted_key == 'creator' or formatted_key == 'whose_turn' or formatted_key == 'guest':
                pk=base64.b64decode(value['bytes'])
                formatted_value=encode_address(pk)
            else:
                decoded_bytes=base64.b64decode(value['bytes'])
                formatted_value = decoded_bytes.decode('utf-8')
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value['uint']
    return formatted

# helper function to read app global state
def read_global_state(client, app_id):
    app = client.application_info(app_id)
    #app_params = app['params'] #what are all of the params?
    #print(app_params)
    global_state = app['params']['global-state'] if "global-state" in app['params'] else []
    return format_state(global_state)

def read_local_state(client, app_id):
    pass