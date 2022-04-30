from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

    with open("addresses/"+str(address)+".txt", "w") as f:
        f.write("address: {}".format(address))
        f.write("\n")
        f.write("passphrase: {}".format(mnemonic.from_private_key(private_key)))

if __name__=="__main__":
    generate_algorand_keypair()