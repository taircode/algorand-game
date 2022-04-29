from pyteal import *

def play_tic_tac_toe(invited_guest):

    handle_creation = Seq(
        App.globalPut(Bytes("creator"), Txn.sender()), #creator will be O's
        App.globalPut(Bytes("guest"), Addr(invited_guest)), #invited_guest will be X's
        App.globalPut(Bytes("whose_turn"), Addr(invited_guest)), #invited_guest will go first
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

    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), #fail if transaction is grouped with any others
        Assert(App.globalGet(Bytes("whose_turne"))==Txn.sender()), #fail if transaction is sent by someone other than whose turn it is
        Cond(#note if you try to go in a location that's already marked, the transaction will fail
            [Txn.application_args[0] == Bytes("N"), If(App.globalGet(Bytes("N"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("E"), If(App.globalGet(Bytes("E"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("S"), If(App.globalGet(Bytes("S"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("W"), If(App.globalGet(Bytes("W"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("NE"), If(App.globalGet(Bytes("NE"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("SE"), If(App.globalGet(Bytes("SE"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("SW"), If(App.globalGet(Bytes("SW"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("NW"), If(App.globalGet(Bytes("NW"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))],
            [Txn.application_args[0] == Bytes("C"), If(App.globalGet(Bytes("C"))==Int(0), If(App.globalGet(Bytes("whose_turn"))==App.globalGet(Bytes("guest")),App.globalPut(Bytes("N"),Bytes("X")),App.globalPut(Bytes("N"),Bytes("O"))),Return(Int(0)))]            
        ),
        If(Or(
            App.globalGet(Bytes("N"))==Int(0),
            App.globalGet(Bytes("E"))==Int(0),
            App.globalGet(Bytes("S"))==Int(0),
            App.globalGet(Bytes("W"))==Int(0),
            App.globalGet(Bytes("NE"))==Int(0),
            App.globalGet(Bytes("SE"))==Int(0),
            App.globalGet(Bytes("SW"))==Int(0),
            App.globalGet(Bytes("NW"))==Int(0),
            App.globalGet(Bytes("C"))==Int(0)
        ),flip_whose_turn,declare_winner),
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
    program = play_tic_tac_toe(
        "ZZAF5ARA4MEC5PVDOP64JM5O5MQST63Q2KOY2FLYFLXXD3PFSNJJBYAFZM"
    )
    print(compileTeal(program, mode=Mode.Application, version=3))

