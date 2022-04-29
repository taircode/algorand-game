from pyteal import *

def play_tic_tac_toe():

    handle_creation = Seq(
        App.globalPut(Bytes("creator"), Txn.sender()), #creator will be O's
        App.globalPut(Bytes("guest"), Txn.application_args[0]), #invited_guest will be X's
        App.globalPut(Bytes("whose_turn"), Txn.application_args[0]), #invited_guest will go first
        App.globalPut(Bytes("N"), Int(0)), # write a byte slice
        App.globalPut(Bytes("E"), Int(0)), # write a byte slice
        App.globalPut(Bytes("S"), Int(0)), # write a byte slice
        App.globalPut(Bytes("W"), Int(0)), # write a byte slice
        App.globalPut(Bytes("NE"), Int(0)), # write a byte slice
        App.globalPut(Bytes("SE"), Int(0)), # write a byte slice
        App.globalPut(Bytes("SW"), Int(0)), # write a byte slice
        App.globalPut(Bytes("NW"), Int(0)), # write a byte slice
        App.globalPut(Bytes("C"), Int(0)), # write a byte slice
        Return(Int(1)) # Could also be Approve()
    )

    handle_optin = Return(Int(0)) # Could also be Reject()

    handle_closeout = Return(Int(0)) # Could also be Reject()

    handle_updateapp = Return(Int(0)) # Could also be Reject()

    handle_deleteapp = Return(Int(0)) # Could also be Reject()

    flip_whose_turn = If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("creator")),App.globalPut(Bytes("whose_turn"), App.globalGet(Bytes("guest"))),App.globalPut(Bytes("whose_turn"), App.globalGet(Bytes("creator"))))

    #payout some money or something.
    declare_winner = Return(Int(1))

    #return an even split of the money
    no_winner = Return(Int(1))

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
        Assert(App.globalGet(Txn.application_args[0])==Int(0)), #fail if the location you are trying to mark has already been marked
        #mark the squre X if guest, O if creator
        If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Txn.application_args[0],Bytes("X")),App.globalPut(Txn.application_args[0],Bytes("O"))),
        #you should check if someone got three in a row
        #check_if_winner, if so, declare_winner
        If(Or(#check to see if board is full
            App.globalGet(Bytes("N"))==Int(0),
            App.globalGet(Bytes("E"))==Int(0),
            App.globalGet(Bytes("S"))==Int(0),
            App.globalGet(Bytes("W"))==Int(0),
            App.globalGet(Bytes("NE"))==Int(0),
            App.globalGet(Bytes("SE"))==Int(0),
            App.globalGet(Bytes("SW"))==Int(0),
            App.globalGet(Bytes("NW"))==Int(0),
            App.globalGet(Bytes("C"))==Int(0)
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
    
if __name__ == "__main__":
    program = play_tic_tac_toe()
    print(compileTeal(program, mode=Mode.Application, version=3))

