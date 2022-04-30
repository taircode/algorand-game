from pyteal import *

"""
A simple game of tic-tac-toe
Later add functionality for a wager -or- receiving an NFT stating that winner won the game
"""
def play_tic_tac_toe():

    handle_creation = Seq(
        App.globalPut(Bytes("creator"), Txn.sender()), #creator will be O's
        #guest is hard-coded for now. Add a feature for the creator to set who they want to challenge
        App.globalPut(Bytes("guest"), Addr("ST5KMIXPPQTFMBIYBIYUVPPY3BIWZAPBTRGUDDHWBG2WF4P4BO6MXRVHGI")), #invited_guest will be X's
        App.globalPut(Bytes("whose_turn"), Addr("ST5KMIXPPQTFMBIYBIYUVPPY3BIWZAPBTRGUDDHWBG2WF4P4BO6MXRVHGI")), #invited_guest will go first #the guest starts first
        App.globalPut(Bytes("N"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("E"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("S"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("W"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("NE"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("SE"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("SW"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("NW"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("C"), Bytes("empty")), # write a byte slice
        Return(Int(1)) # Could also be Approve()
    )

    handle_optin = Return(Int(0)) # Could also be Reject()

    handle_closeout = Return(Int(0)) # Could also be Reject()

    handle_updateapp = Return(Int(0)) # Could also be Reject()

    handle_deleteapp = Return(Int(1)) #what if this is 0? can you just never delete the app then?

    flip_whose_turn = If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("creator")),App.globalPut(Bytes("whose_turn"), App.globalGet(Bytes("guest"))),App.globalPut(Bytes("whose_turn"), App.globalGet(Bytes("creator"))))

    #payout some money or something.
    declare_winner = Return(Int(1))
    #clear board to play again

    #return an even split of the money
    no_winner = Return(Int(1))
    #clear board to play again

    #need to implement a check to see if someone won
    #check_if_winner = 

    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), #fail if transaction is grouped with any others
        Assert(App.globalGet(Bytes("whose_turne"))==Txn.sender()), #fail if transaction is sent by someone other than whose turn it is
        Assert(#fail if you provide something that is not a valid direction
            Or(
            Txn.application_args[0]==Bytes("N"),
            Txn.application_args[0]==Bytes("E"),
            Txn.application_args[0]==Bytes("S"),
            Txn.application_args[0]==Bytes("W"),
            Txn.application_args[0]==Bytes("NE"),
            Txn.application_args[0]==Bytes("SE"),
            Txn.application_args[0]==Bytes("SW"),
            Txn.application_args[0]==Bytes("NW"),
            Txn.application_args[0]==Bytes("C"),
            )
        ),
        Assert(App.globalGet(Txn.application_args[0])==Bytes("empty")), #fail if the location you are trying to mark has already been marked
        #mark the squre X if guest, O if creator
        If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Txn.application_args[0],Bytes("X")),App.globalPut(Txn.application_args[0],Bytes("O"))),
        #you should check if someone got three in a row
        #check_if_winner, if so, declare_winner
        If(Or(#check to see if board is full
            App.globalGet(Bytes("N"))==Bytes("empty"),
            App.globalGet(Bytes("E"))==Bytes("empty"),
            App.globalGet(Bytes("S"))==Bytes("empty"),
            App.globalGet(Bytes("W"))==Bytes("empty"),
            App.globalGet(Bytes("NE"))==Bytes("empty"),
            App.globalGet(Bytes("SE"))==Bytes("empty"),
            App.globalGet(Bytes("SW"))==Bytes("empty"),
            App.globalGet(Bytes("NW"))==Bytes("empty"),
            App.globalGet(Bytes("C"))==Bytes("empty")
        ),flip_whose_turn,no_winner),
        Return(Int(1))
    )

    return Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

def get_approval_program():
    program = play_tic_tac_toe()
    return compileTeal(program, mode=Mode.Application, version=3)

def get_clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)
    
if __name__ == "__main__":
    program = play_tic_tac_toe()
    print(compileTeal(program, mode=Mode.Application, version=3))

