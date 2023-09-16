# <span style="color:orange;">Pawn</span>hub


Chess is a board game for two players, called White and Black. Each controlling an army of chess pieces in their color, with the objective to checkmate the opponent's king. 

<strong>Pawnhub</strong> is a chess variant. Capturing rival pieces demotes the capturing piece to pawn piece after eleminating captured piece.


### <span style="color:orange;">Key</span> mappings

| KEYBOARD - KEY  | KEY MAPPINGS |
| ------------- | ------------- |
| KEY - ESCAPE | Quits the Application|
| KEY -  E | Resets the ongoing Game  |
| KEY - T | Change the theme |


### <span style="color:orange;">Pawn</span> promotion mappings
| KEYBOARD - KEY  | KEY MAPPINGS |
| ------------- | ------------- |
| KEY - Q | Promote to <span style="color:orange;">Queen</span> after pawn reaches last rank|
| KEY - R  | Promote to <span style="color:orange;">Rook</span> after pawn reaches last rank  |
| KEY - B  | Promote to <span style="color:orange;">Bishop</span> after pawn reaches last rank  |
| KEY - K  | Promote to <span style="color:orange;">Knight</span> after pawn reaches last rank  |


### <span style="color:orange;">Low Level</span> design



### <span style="color:orange;">Themes</span> in pawnhub


At pawnhub there are four color configuration which can be switched between by pressing <span style="color:orange;">Key - T</span>

![Themes available in application](screenshots/themes.png)

### <span style="color:orange;">Rules</span> in pawnhub

All the traditional chess rules work as it is except captures

- ### Castling 

    <img src="screenshots/castling.png" alt="drawing" width="300"/>

- ### Promotion

    <img src="screenshots/promotion.png" alt="drawing" width="800"/>

- ### En passant

    <img src="screenshots/en_passant.png" alt="drawing" width="600"/>

- ### Capturing

    Capturing works little different at pawnhub, When player plays a move which captures opponents pieces, after eliminating the opponents piece the playes piece demotes in Pawn piece
    
    <span style="color:orange;">How is this fair ?</span>

    Capturing pieces with same value is trick here, As higher value pieces gets demoted to pawn pieces player needs to evalute possible captures which doesnt put him at disadvantage. This makes the game more interesting.

  <img src="screenshots/capturing.png" alt="drawing" width="600"/>

