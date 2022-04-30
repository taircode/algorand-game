from algosdk import account, v2client, mnemonic
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
            if formatted_key == 'creator' or formatted_key == 'whose_turn' or formatted_key == 'guest':
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