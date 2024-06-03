# Uno Game

This project contains an Uno game on terminal programmed in Python. 

## Rules

1. **Card Types**:
   - **Number Cards**: Cards with numbers ranging from 0 to 9.
   - **Action Cards**: Cards with special actions (Skip (S), Reverse (R), Draw Two (+2), Wild (W), Wild Draw Four (W+4)).

2. **Card Colors**:
   - Card colors include: Red, Green, Blue, Yellow

3. **Gameplay**:
   - Players take turns matching a card from their hand with the current card shown on the discard pile by either color or Type.
   - If a player cannot match the discard pile, they must draw a card from the draw pile.
   - Action cards have specific effects that alter the flow of the game.
     -   Skip: The next player loses their round.
     -   Reverse: The direction of play is reversed.
     -   Draw Two: The next player loses their round and has to draw 2 cards.
     -   Wild: Can be placed on anything and the current player specifies the color for the next player.
     -   Wild Draw Four: Same as Wild, but the next player loses their round and has to draw 4 cards.

4. **Winning**:
   - When the player places their second to last card, they have to call "UNO" or someone else can call "STOP UNO".
     When "UNO" is called, the game continues, but if "STOP UNO" is called, the player has to draw 2 cards.
   - The first player to get rid of all their cards wins.
