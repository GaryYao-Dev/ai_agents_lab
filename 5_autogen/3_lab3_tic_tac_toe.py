from dataclasses import dataclass
from dotenv import load_dotenv
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core import SingleThreadedAgentRuntime
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
import asyncio
import re

load_dotenv(override=True)

SIZE = 3
NUM_IN_A_ROW_TO_WIN = 3

@dataclass
class Message:
    content: str



class PlayerAgent(RoutedAgent):
    """Player Agent - Responsible for deciding the next move"""
    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name)
        self.symbol = symbol
        opponent = 'O' if symbol == 'X' else 'X'
        model_client = OpenAIChatCompletionClient(model="gpt-5-nano")
        system_msg = (
            f"You are an expert {SIZE}x{SIZE} Tic-Tac-Toe player playing as '{symbol}'. Your opponent is '{opponent}'. "
            f"Goal: Get {NUM_IN_A_ROW_TO_WIN} in a row (horizontal, vertical, or diagonal) to win.\n\n"
            f"STRATEGY PRIORITIES (in order):\n"
            f"1. WIN: If you can complete {NUM_IN_A_ROW_TO_WIN} in a row on your next move, do it immediately!\n"
            f"2. BLOCK IMMEDIATE THREAT: If opponent can complete {NUM_IN_A_ROW_TO_WIN} in a row on their next move, block them!\n"
            f"3. PREVENT 'OPEN THREE': If opponent has 2-in-a-row with BOTH ends open (not at edges), "
            f"they can form an unstoppable 3-in-a-row. Block one end NOW! Example: '-XX--' is dangerous because "
            f"it becomes '-XXX-' and you can't block both ends.\n"
            f"4. CREATE YOUR 'OPEN THREE': Build your own 2-in-a-row with both ends open to create winning threat.\n"
            f"5. BUILD SEQUENCES: Create 3-in-a-row (with one end open) or extend your 2-in-a-row.\n"
            f"6. DISRUPT OPPONENT: Block opponent's 2-in-a-row with one open end.\n"
            f"7. CENTER CONTROL: Prefer center positions (2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (4,2), (4,3), (4,4).\n"
            f"8. STRATEGIC POSITIONING: Create multiple threats simultaneously (fork strategy).\n\n"
            f"CRITICAL DEFENSE RULE:\n"
            f"Pattern '-XX-' or '-OO-' (2-in-a-row with both ends open and not at board edge) is EXTREMELY dangerous! "
            f"Once it becomes '-XXX-', you cannot defend both ends. Prevent this by occupying one end position.\n\n"
            f"ANALYSIS STEPS:\n"
            f"1. Scan for your {NUM_IN_A_ROW_TO_WIN-1}-in-a-row that can become {NUM_IN_A_ROW_TO_WIN} → WIN immediately.\n"
            f"2. Scan for opponent's {NUM_IN_A_ROW_TO_WIN-1}-in-a-row → BLOCK immediately.\n"
            f"3. **CRITICAL**: Scan for opponent's 2-in-a-row with BOTH ends open (pattern: -XX- or -OO-) → BLOCK one end!\n"
            f"4. Look for your 2-in-a-row with both ends open → Extend to create open-three.\n"
            f"5. Look for your 2-in-a-row or 3-in-a-row with one open end → Extend.\n"
            f"6. Look for opponent's 2-in-a-row with open ends → Disrupt.\n"
            f"7. If none above, choose strategic center or corner positions.\n\n"
            f"RESPONSE FORMAT:\n"
            f"Respond with ONLY 'row,col' (e.g., '3,2'). Row and col must be between 1 and {SIZE}.\n"
            f"Before giving your answer, briefly explain your reasoning in one sentence."
        )
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=system_msg)

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> Message:
        text_message = TextMessage(content=message.content, source='user')
        res = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        print(f"Player {self.symbol} chose move: {res.chat_message.content}")
        return Message(content=res.chat_message.content)


class JudgeAgent(RoutedAgent):
    """Judge Agent - Responsible for determining if the game is over and who wins"""
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-5-nano")
        system_msg = (
            f"You are a {SIZE}x{SIZE} Tic-Tac-Toe judge. Given a {SIZE}x{SIZE} board, determine if the game is over. "
            f"Check for: 1) {NUM_IN_A_ROW_TO_WIN} in a row (horizontal, vertical, or diagonal) - that player wins. "
            f"2) Board is full with no winner - it's a draw. 3) Game continues if neither condition is met. "
            f"Respond with ONLY one of: 'X wins', 'O wins', 'Draw', or 'Continue'."
        )
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=system_msg)

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> Message:
        text_message = TextMessage(content=message.content, source='user')
        res = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        return Message(content=res.chat_message.content)


class GameMasterAgent(RoutedAgent):
    """Game Master Agent - Manages game state and multi-round loop"""
    def __init__(self, name: str) -> None:
        super().__init__(name)
        # Initialize the board, using '-' to represent empty spaces
        self.board = [['-'] * SIZE for _ in range(SIZE)]
        self.current_player = 'X'
        self.move_count = 0
        self.max_moves = SIZE * SIZE  # Total number of spaces on the board

    def display_board(self) -> str:
        """Display the board"""
        result = "\n=== Current Board ===\n"
        result += "  " + " ".join(str(i) for i in range(1, SIZE + 1)) + "\n"
        for i, row in enumerate(self.board, 1):
            result += f"{i} {' '.join(row)}\n"
        return result

    def make_move(self, row: int, col: int, symbol: str) -> bool:
        """Execute a move"""
        if 1 <= row <= SIZE and 1 <= col <= SIZE:
            r, c = row - 1, col - 1  # Convert to 0-indexed
            if self.board[r][c] == '-':
                self.board[r][c] = symbol
                self.move_count += 1
                return True
        return False

    def get_board_state(self) -> str:
        """Get text description of the board state"""
        state = "Current board state:\n"
        state += "  " + " ".join(str(i) for i in range(1, SIZE + 1)) + "\n"
        for i, row in enumerate(self.board, 1):
            state += f"{i} {' '.join(row)}\n"
        return state

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> Message:
        """Handle game loop"""
        print(f"=== {SIZE}x{SIZE} Tic-Tac-Toe Game Start ===")
        print(f"Goal: Get {NUM_IN_A_ROW_TO_WIN} in a row (horizontal, vertical, or diagonal) to win!\n")
        
        game_log = ""
        
        # Game loop - maximum moves
        for round_num in range(1, self.max_moves + 1):
            print(f"\n{'='*40}")
            print(f"--- Round {round_num} ---")
            print(self.display_board())
            print(f"Current player: {self.current_player}")
            
            # Ask current player for next move
            player_id = AgentId("player_x" if self.current_player == 'X' else "player_o", "default")
            prompt = f"{self.get_board_state()}\nYou are player {self.current_player}. Where do you want to place your mark? Reply with 'row,col' format."
            
            player_response = await self.send_message(Message(prompt), player_id)
            
            # Parse player's move
            move_match = re.search(r'(\d)[,\s]+(\d)', player_response.content)
            if move_match:
                row, col = int(move_match.group(1)), int(move_match.group(2))
                
                if self.make_move(row, col, self.current_player):
                    print(f"✓ Player {self.current_player} placed at ({row},{col})")
                    print(self.display_board())
                    
                    # Ask judge if game is over
                    judge_id = AgentId("judge", "default")
                    judge_prompt = f"{self.get_board_state()}\nCheck if the game is over."
                    judge_response = await self.send_message(Message(judge_prompt), judge_id)
                    print(f"Judge decision: {judge_response.content}")
                    
                    # Check if game is over
                    if 'wins' in judge_response.content.lower() or 'draw' in judge_response.content.lower():
                        print(f"\n{'='*40}")
                        print(f"🎮 GAME OVER: {judge_response.content}")
                        print(self.display_board())
                        print(f"{'='*40}\n")
                        game_log = f"Game ended at round {round_num}. Result: {judge_response.content}"
                        return Message(content=game_log)
                    
                    # Switch player
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                else:
                    print(f"✗ Invalid move at ({row},{col}), position already taken or out of bounds!")
            else:
                print(f"✗ Could not parse move from: {player_response.content}")
        
        print(f"\n{'='*40}")
        print("🎮 Game ended - Maximum moves reached!")
        print(self.display_board())
        print(f"{'='*40}\n")
        game_log = "Game ended - Maximum moves reached (Draw)"
        return Message(content=game_log)


async def main():
    """Main async function to run the Tic-Tac-Toe game."""
    runtime = SingleThreadedAgentRuntime()
    
    # Register player agents
    await PlayerAgent.register(runtime, "player_x", lambda: PlayerAgent("player_x", "X"))
    await PlayerAgent.register(runtime, "player_o", lambda: PlayerAgent("player_o", "O"))
    
    # Register judge agent
    await JudgeAgent.register(runtime, "judge", lambda: JudgeAgent("judge"))
    
    # Register game master agent
    await GameMasterAgent.register(runtime, "gamemaster", lambda: GameMasterAgent("gamemaster"))
    
    runtime.start()

    # Start the game
    gamemaster_id = AgentId("gamemaster", "default")
    message = Message(content="start")
    response = await runtime.send_message(message, gamemaster_id)
    
    # Final result
    print("\n" + "="*40)
    print("FINAL RESULT:", response.content)
    print("="*40)

    await runtime.stop()
    await runtime.close()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())