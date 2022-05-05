# algo-game

A simple tic-tac-toe game on the Algorand blockchain, implemented using PyTeal.

Use generate_account.py to create an Algorand address, passphrase pair that is stored in `addresses/`. 
Only use on testnet! Mnemonic phrases should not be shared publicly if using actual algo on mainnet!
Add testnet algos using the [testnet dispenser.](https://bank.testnet.algorand.network)

The PyTeal code is in `tic_tac_toe.py` with two functions that compile the approval program and the clear state program.

Deploy the application to testnet using `deploy_app.py`. The creator of the app specifies the address of the guest they are challenging. Keep track of all deployed applications in `all_deployed.txt`. Record global state after creation in `deployed/application[app_id].txt`.

Take turns selecting the location of the next move using `take_turn.py` until there's a winner or the board is full. Record global state after each move in `deployed/application[app_id].txt`.
