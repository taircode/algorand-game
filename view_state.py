
from algosdk import v2client
from helper import read_global_state, read_local_state
from algosdk.encoding import decode_address
import argparse
from algosdk import account
from graphics import *

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--app_id",default="latest",help="provide an app_id, otherwise app_id of most recently deployed is used.")
    args = parser.parse_args()

    #you could actually read global state from the app here, and see if it matches whose_turn

    #get the app id from args or from file
    if args.app_id=='latest':
        with open("./all_deployed.txt","r") as f:
            for line in f:
                pass
            app_id=int(line)
    else:
        app_id=int(args.app_id)

    # user declared algod connection parameters.
    # Node must have EnableDeveloperAPI set to true in its config
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    creator_mnemonic = {
        "creator":"cushion raccoon snap tragic come seat rhythm canal clarify oven pipe misery maid mutual gossip real flat snake witness achieve concert wrestle praise abstract hundred",
        "guest":"ill captain pluck horn reduce stadium logic such short empty install analyst again final ladder marine push ask clerk shrug toe zoo seat abstract fee"
    }

    # initialize an algodClient
    algod_client = v2client.algod.AlgodClient(algod_token, algod_address)

    # read global state of application
    global_state=read_global_state(algod_client, app_id)
    print("Global state:", global_state)

    win = GraphWin("Current Board",600,600) 
    message = Text(Point(win.getWidth()/2, 580), 'Click anywhere to quit.')
    message.draw(win)

    creator_address=global_state['creator']
    creator = Text(Point(win.getWidth()/2, 500), 'O: Creator is '+creator_address)
    creator.draw(win)

    guest_address=global_state['guest']
    guest = Text(Point(win.getWidth()/2, 515), 'X: Guest is '+guest_address)
    guest.draw(win)

    bet_size=global_state['bet']
    pot_size=bet_size*2
    bet_text=Text(Point(500,100), 'Pot size: '+str(pot_size)+" MicroAlgos")
    bet_text.draw(win)

    creator_address="4NVPTGTJQLCGN7QFVH4WCZATFXE6RXGI6QZQYTC5DPW5C4O5BUCEGTC3BA"
    guest_address="ST5KMIXPPQTFMBIYBIYUVPPY3BIWZAPBTRGUDDHWBG2WF4P4BO6MXRVHGI"
    
    #creator_pk=decode_address(creator_address)
    #guest_pk=decode_address(guest_address)

    print("about to do read_local_state")
    local_creator=read_local_state(algod_client, app_id, creator_address)

    if 'amount' in local_creator:
        creator_amount=local_creator['amount']
        creator_sent_text=Text(Point(500,125), 'Creator sent: '+str(creator_amount)+" MicroAlgos")
        creator_sent_text.draw(win)
        if creator_amount<bet_size+10**3:
            creator_request_text=Text(Point(480,140), 'Please send '+str(bet_size+10**3-creator_amount)+" more MicroAlgos")
            creator_request_text.draw(win)
    else:
        creator_optin_text=Text(Point(500,125), 'Creator must opt-in to place bet.')
        creator_optin_text.draw(win)

    local_guest=read_local_state(algod_client, app_id, guest_address)
    if 'amount' in local_guest:
        guest_amount=local_guest['amount']
        guest_sent_text=Text(Point(500,185), 'Guest sent: '+str(guest_amount)+" MicroAlgos")
        guest_sent_text.draw(win)
        if guest_amount<bet_size+10**3:
            guest_request_text=Text(Point(480,200), 'Please send '+str(bet_size+10**3-guest_amount)+" more MicroAlgos")
            guest_request_text.draw(win)
    else:
        guest_optin_text=Text(Point(500,185), 'Creator must opt-in to place bet.')
        guest_optin_text.draw(win)

    winner=global_state['winner']
    if winner=='tie':
        winner_text=Text(Point(win.getWidth()/2, 410), 'The game ended in a tie.')
    else:
        winner_text=Text(Point(win.getWidth()/2, 410), 'The winner is '+winner)
    winner_text.draw(win)

    if winner=='pending':
        turn_address=global_state['whose_turn']
        if turn_address==guest_address:
            whose_turn= Text(Point(win.getWidth()/2, 390), 'It is X\'s turn.')
        else:
            whose_turn= Text(Point(win.getWidth()/2, 390), 'It is O\'s turn.')
        whose_turn.draw(win)
    
    #draw the grid
    x_offset=10
    y_offset=10
    rect = Rectangle(Point(x_offset, y_offset), Point(360+x_offset, 360+y_offset))
    vert1=Line(Point(x_offset+120,y_offset),Point(x_offset+120,360+y_offset))
    vert2=Line(Point(x_offset+240,y_offset),Point(x_offset+240,360+y_offset))
    hor1=Line(Point(x_offset,y_offset+120),Point(x_offset+360,y_offset+120))
    hor2=Line(Point(x_offset,y_offset+240),Point(x_offset+360,y_offset+240))
    rect.draw(win)
    vert1.draw(win)
    vert2.draw(win)
    hor1.draw(win)
    hor2.draw(win)

    grid_points=dict(NW=Point(x_offset+60,y_offset+60),
    N=Point(x_offset+180,y_offset+60),
    NE=Point(x_offset+300,y_offset+60),

    W=Point(x_offset+60,y_offset+180),
    C=Point(x_offset+180,y_offset+180),
    E=Point(x_offset+300,y_offset+180),

    SW=Point(x_offset+60,y_offset+300),
    S=Point(x_offset+180,y_offset+300),
    SE=Point(x_offset+300,y_offset+300)
    )

    for key, val in global_state.items():
        if key not in ['whose_turn','creator','guest','winner','bet']:
            if val!='empty':
                if val=='X':
                    #draw an X at location key
                    x_center=grid_points[key].getX()
                    y_center=grid_points[key].getY()
                    line1=Line(Point(x_center-12.5,y_center-12.5), Point(x_center+12.5,y_center+12.5))
                    line2=Line(Point(x_center+12.5,y_center-12.5), Point(x_center-12.5,y_center+12.5))
                    line1.draw(win)
                    line2.draw(win)
                else:
                    #draw an O at location key
                    cir = Circle(grid_points[key], 25)
                    cir.draw(win)
    win.getMouse() # Pause to view result
    win.close()