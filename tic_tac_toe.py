from pyteal import *

"""
A simple game of tic-tac-toe
Later add functionality for a wager -or- receiving an NFT stating that winner won the game
"""
def play_tic_tac_toe():

    handle_creation = Seq(
        App.globalPut(Bytes("creator"), Txn.sender()), #creator will be O's in tic-tac-toe
        App.globalPut(Bytes("guest"), Txn.application_args[0]), #guest will be X's in tic-tac-toe
        App.globalPut(Bytes("whose_turn"), Txn.application_args[0]), #guest goes first
        App.globalPut(Bytes("bet"),Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("N"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("E"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("S"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("W"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("NE"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("SE"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("SW"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("NW"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("C"), Bytes("empty")), # write a byte slice
        App.globalPut(Bytes("winner"), Bytes("pending")), # write a byte slice
        Return(Int(1)) # Could also be Approve()
    )

    #no local states so don't need this
    handle_optin = Return(Int(0)) # Could also be Reject()

    #no local states so nothing for a user to close-out
    handle_closeout = Return(Int(0)) # Could also be Reject()

    handle_updateapp = Return(Int(0)) # Could also be Reject()

    #what if this is Return(Int(0))? Can you just never delete the app then?
    handle_deleteapp =  Return(Int(1))
    
    """ handle_deleteapp better
    Seq(
        InnerTxnBuilder.Begin(),
        #InnerTxnBuilder.SetFields({
        #    TxnField.type_enum: TxnType.Payment,
        #    TxnField.amount: Mul(App.globalGet(Bytes("bet")),Int(10**6)),
        #    TxnField.receiver: App.globalGet(Bytes("guest")) 
        #}),
        #InnerTxnBuilder.Next(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.close_remainder_to: Global.creator_address() 
        }),
        InnerTxnBuilder.Submit(),
        Return(Int(1))
    )
    """

    flip_whose_turn = If(
            App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("creator")),
            App.globalPut(Bytes("whose_turn"), App.globalGet(Bytes("guest"))),
            App.globalPut(Bytes("whose_turn"), App.globalGet(Bytes("creator")))
        )

    #return an even split of the money
    no_winner = Seq(        
        App.globalPut(Bytes("winner"),Bytes("tie")),
        #payback the guest
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Mul(App.globalGet(Bytes("bet")),Int(10**6)),
            TxnField.receiver: App.globalGet(Bytes("guest")) 
        }),
        #All addresses in inner transactions have to be part of the foreign accounts array!
        #https://forum.algorand.org/t/escrow-transaction/5030
        InnerTxnBuilder.Next(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.close_remainder_to: Global.creator_address()
        }),
        InnerTxnBuilder.Submit(),
    )
    #clear board to play again -or- just delete?

    #check to see if someone won
    #there's probably a quicker way to do this using the location of the most recent move, but this works too
    check_if_winner = Or(
        And(App.globalGet(Bytes("NW"))==Bytes("X"),App.globalGet(Bytes("W"))==Bytes("X"),App.globalGet(Bytes("SW"))==Bytes("X")),
        And(App.globalGet(Bytes("N"))==Bytes("X"),App.globalGet(Bytes("C"))==Bytes("X"),App.globalGet(Bytes("S"))==Bytes("X")),
        And(App.globalGet(Bytes("NE"))==Bytes("X"),App.globalGet(Bytes("E"))==Bytes("X"),App.globalGet(Bytes("SE"))==Bytes("X")),

        And(App.globalGet(Bytes("NW"))==Bytes("X"),App.globalGet(Bytes("N"))==Bytes("X"),App.globalGet(Bytes("NE"))==Bytes("X")),
        And(App.globalGet(Bytes("W"))==Bytes("X"),App.globalGet(Bytes("C"))==Bytes("X"),App.globalGet(Bytes("E"))==Bytes("X")),
        And(App.globalGet(Bytes("SW"))==Bytes("X"),App.globalGet(Bytes("S"))==Bytes("X"),App.globalGet(Bytes("SE"))==Bytes("X")),

        And(App.globalGet(Bytes("NW"))==Bytes("X"),App.globalGet(Bytes("C"))==Bytes("X"),App.globalGet(Bytes("SE"))==Bytes("X")),
        And(App.globalGet(Bytes("SW"))==Bytes("X"),App.globalGet(Bytes("S"))==Bytes("X"),App.globalGet(Bytes("NE"))==Bytes("X")),

        And(App.globalGet(Bytes("NW"))==Bytes("O"),App.globalGet(Bytes("W"))==Bytes("O"),App.globalGet(Bytes("SW"))==Bytes("O")),
        And(App.globalGet(Bytes("N"))==Bytes("O"),App.globalGet(Bytes("C"))==Bytes("O"),App.globalGet(Bytes("S"))==Bytes("O")),
        And(App.globalGet(Bytes("NE"))==Bytes("O"),App.globalGet(Bytes("E"))==Bytes("O"),App.globalGet(Bytes("SE"))==Bytes("O")),

        And(App.globalGet(Bytes("NW"))==Bytes("O"),App.globalGet(Bytes("N"))==Bytes("O"),App.globalGet(Bytes("NE"))==Bytes("O")),
        And(App.globalGet(Bytes("W"))==Bytes("O"),App.globalGet(Bytes("C"))==Bytes("O"),App.globalGet(Bytes("E"))==Bytes("O")),
        And(App.globalGet(Bytes("SW"))==Bytes("O"),App.globalGet(Bytes("S"))==Bytes("O"),App.globalGet(Bytes("SE"))==Bytes("O")),

        And(App.globalGet(Bytes("NW"))==Bytes("O"),App.globalGet(Bytes("C"))==Bytes("O"),App.globalGet(Bytes("SE"))==Bytes("O")),
        And(App.globalGet(Bytes("SW"))==Bytes("O"),App.globalGet(Bytes("S"))==Bytes("O"),App.globalGet(Bytes("NE"))==Bytes("O")),
    )

    #payout some money or something.
    #clear board to play again -or- delete app
    declare_winner = If(Or(
        And(App.globalGet(Bytes("NW"))==Bytes("X"),App.globalGet(Bytes("W"))==Bytes("X"),App.globalGet(Bytes("SW"))==Bytes("X")),
        And(App.globalGet(Bytes("N"))==Bytes("X"),App.globalGet(Bytes("C"))==Bytes("X"),App.globalGet(Bytes("S"))==Bytes("X")),
        And(App.globalGet(Bytes("NE"))==Bytes("X"),App.globalGet(Bytes("E"))==Bytes("X"),App.globalGet(Bytes("SE"))==Bytes("X")),

        And(App.globalGet(Bytes("NW"))==Bytes("X"),App.globalGet(Bytes("N"))==Bytes("X"),App.globalGet(Bytes("NE"))==Bytes("X")),
        And(App.globalGet(Bytes("W"))==Bytes("X"),App.globalGet(Bytes("C"))==Bytes("X"),App.globalGet(Bytes("E"))==Bytes("X")),
        And(App.globalGet(Bytes("SW"))==Bytes("X"),App.globalGet(Bytes("S"))==Bytes("X"),App.globalGet(Bytes("SE"))==Bytes("X")),

        And(App.globalGet(Bytes("NW"))==Bytes("X"),App.globalGet(Bytes("C"))==Bytes("X"),App.globalGet(Bytes("SE"))==Bytes("X")),
        And(App.globalGet(Bytes("SW"))==Bytes("X"),App.globalGet(Bytes("S"))==Bytes("X"),App.globalGet(Bytes("NE"))==Bytes("X"))
        ),
        App.globalPut(Bytes("winner"),App.globalGet(Bytes("guest"))),
        App.globalPut(Bytes("winner"),App.globalGet(Bytes("creator")))
    )

    pay_winner=Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Mul(Mul(App.globalGet(Bytes("bet")),Int(2)),Int(10**6)),
            TxnField.receiver: Txn.sender() #only the sender could have won the game on the turn b/c we check board after each turn
        }),
        InnerTxnBuilder.Submit(),
    )

    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), #fail if transaction is grouped with any others
        Assert(App.globalGet(Bytes("whose_turn"))==Txn.sender()), #fail if transaction is sent by someone other than whose turn it is
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
        If(check_if_winner,Seq(declare_winner,pay_winner),
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
            ),flip_whose_turn,no_winner)
        ),
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
    return compileTeal(program, mode=Mode.Application, version=6)

def get_clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=6)
    
if __name__ == "__main__":
    program = play_tic_tac_toe()
    print(compileTeal(program, mode=Mode.Application, version=6))

