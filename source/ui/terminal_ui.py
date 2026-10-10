from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.player.base.player import Player
    from collections import Counter

import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box


from ui.base.ui import GameUI
from models.bid import Bid
import utility.constants as c

class TerminalUI(GameUI):
    
    
    FACE_SYMBOLS = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

    _BANNER = r"""
    [bold yellow]
    ██╗     ██╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗ ██████╗ ███████╗
    ██║     ██║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██║██╔════╝ ██╔════╝
    ██║     ██║███████║██████╔╝███████╗    ██║  ██║██║██║      █████╗ 
    ██║     ██║██╔══██║██╔══██╗╚════██║    ██║  ██║██║██║      ██╔══╝
    ███████╗██║██║  ██║██║  ██║███████║    ██████╔╝██║╚██████╗ ███████╗
    ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝
    [/bold yellow]"""

    
    
    
    def __init__(self):
        self.console = Console()
    
    
    def initiate(self):
        self.console.clear()
        self.console.print(self._BANNER)
        self.console.print(
            Panel.fit(
                "[bold white]Liar's Dice — The Classic Bluffing Game[/bold white]\n"
                "[dim]Roll. Bid. Bluff. Call it. Last die standing wins.[/dim]",
                border_style="yellow",
                padding=(0, 4),
            )
        )
        self.console.print()
        
    def get_setup_vars(self) -> dict:

        setup = {}
        min_ai_cnt = c.CNT_MIN_PLAYERS - 1 # -1 because of the human player
        max_ai_cnt = c.CNT_MAX_PLAYERS - 1 # -1 because of the human player
        
        setup["cnt_ai"] = self._ask_number(
            "[bold]How many AI opponents?[/bold] "
            + f"[dim][{min_ai_cnt}:{max_ai_cnt}][/dim]"
            + f"[cyan bold]({c.SUGGESTED_AI_PLAYER_CNT})[/cyan bold]",
            min_ai_cnt,
            max_ai_cnt,
            "Please enter valid number of enemies"
        )
        setup["player_name"] = self._ask_player_name(c.RESERVED_NAMES)
        setup["wild_ones"] = self._ask_bool(
            "[bold]Enable Wild Ones mode?[/bold] "
            "[dim](1s count as any face)[/dim]",
            False
        )
        

        return setup
        
        
    def show_prestart(self, players: list[Player], wild_ones: bool):
        self.console.print()
        self.console.print(f"  [dim]Players at the table:[/dim]")
        for p in players:
            tag = "[cyan]Bot[/cyan]" if p.is_bot else "[yellow]You[/yellow]"
            self.console.print(f"    • {tag} [bold]{p.name}[/bold]")

        self.console.print()
        if wild_ones:
            self.console.print("  [magenta bold]★ Wild Ones Mode is ON ★[/magenta bold]")

        self.console.print()
        self.ask_confirmation("  Press Enter to set sail... 🏴‍☠️  ")
        
        
        
    def show_round(
        self,
        round_num: int,
        active_players: list[Player],
        dice_cnt: int,
        wild_ones: bool
        ):
        
        self.console.print()
        self.console.rule(f"[bold yellow]⚔  Round {round_num}  ⚔[/bold yellow]", style="yellow")

        table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
        table.add_column("Player", style="bold")
        table.add_column("Dice", justify="center")
        table.add_column("Status", justify="center")

        for p in active_players:
            dice_bar = "🎲" * p.cnt_dice
            tag = "[green]Bot[/green]" if p.is_bot else "[yellow]You[/yellow]"
            table.add_row(p.name, dice_bar or "[red]—[/red]", tag)

        self.console.print(table)

        if wild_ones:
            self.console.print("  [magenta bold]★ Wild Ones Mode Active ★[/magenta bold]  "
                        "[dim]1s count as any face[/dim]\n")
            
        self.ask_confirmation("[dim]Press enter to continue...[/dim]")
        
        
    def show_turn_header(self, current_player: Player):
        style = "cyan" if current_player.is_bot else "yellow"
        icon = "🤖" if current_player.is_bot else "🧑"
        self.console.print()
        self.console.rule(f"[{style}]{icon}  {current_player.name}'s Turn[/{style}]", style=style)
    
        
    def show_turn(self, player: Player, bid: Bid | None):

        if bid is None:
            move_str = f"  [bold red]{player.name}[/bold red] calls [bold]LIAR![/bold]  💀"
        else:
            bid = str(bid)
            move_str = (
                f"  [bold cyan]{player.name}[/bold cyan] bids "
                f"[cyan bold]{bid[0]}[/bold cyan]{bid[1:]}"
            )
        self.console.print(move_str)
        
        
    def show_reveal(
        self,
        active_players: list[Player],
        dice_face_count: Counter,
        current_bid: Bid,
        wild_ones: bool
        ):
        self.console.print()
        self.console.rule("[bold red]🎲  REVEAL  🎲[/bold red]", style="red")
        self.console.print()
        
        for p in active_players:
            symbols = "  ".join(self.FACE_SYMBOLS[v] for v in sorted(p.values))
            values_str = ", ".join(str(v) for v in sorted(p.values))
            tag = "[cyan]Bot[/cyan]" if p.is_bot else "[yellow]You[/yellow]"
            self.console.print(f"  {tag} [bold]{p.name}:[/bold]  {symbols}  [dim]({values_str})[/dim]")
            
        self.console.print()
        self.console.print("  [bold dim]Full tally:[/bold dim]")
        
        tally_table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold dim")
        tally_table.add_column("Face", justify="center")
        tally_table.add_column("Count", justify="center")
        tally_table.add_column("(+wild 1s)", justify="center")
        
        for face in range(1, 7):
            count = dice_face_count[face]
            wild_count = count + (dice_face_count[1]) if wild_ones and face != 1 else 0
            wild_str = str(wild_count) if wild_ones and face != 1 else "-"
            tally_table.add_row(f"{self.FACE_SYMBOLS[face]} {face}", str(count), wild_str)
                
        self.console.print(tally_table)
        
            
            
    
    def show_round_result(
        self,
        loosing_player: Player,
        winning_player: Player,
        is_eliminated: bool,
        bid: Bid,
        challenger_player: Player,
        is_challenge_valid: bool,
        bid_holder: Player
        ):
        self.console.print()
        if is_challenge_valid is False:
            self.console.print(Panel(
                f"[green bold]Bid stands![/green bold]\n"
                f"[dim]{bid} — it was real![/dim]\n\n"
                f"[red]{'🤖' if loosing_player.is_bot else '🧑'} {challenger_player.name} challenged too soon — loses a die.[/red]",
                border_style="green", padding=(0, 2)
            ))
        else: # is True
            self.console.print(Panel(
                f"[red bold]Bluff called![/red bold]\n"
                f"[dim]{bid} — wasn't there![/dim]\n\n"
                f"[red]{'🤖' if loosing_player.is_bot else '🧑'} {loosing_player.name} was bluffing — loses a die.[/red]",
                border_style="red", padding=(0, 2)
            ))
        if is_eliminated:
            self.console.print(f"\n  [bold red]💀 {loosing_player.name} is eliminated![/bold red]")
        time.sleep(1.5)
        
        
        
        
    def show_winner(self, player: Player) -> bool:
        self.console.print()
        self.console.rule("[bold yellow]🏆  GAME OVER  🏆[/bold yellow]", style="yellow")
        icon = "🤖" if player.is_bot else "🎉"
        self.console.print()
        self.console.print(
            Panel.fit(
                f"{icon}  [bold yellow]{player.name} wins![/bold yellow]  {icon}\n"
                f"[dim]Last die standing.[/dim]",
                border_style="yellow",
                padding=(1, 6),
            )
        )
        self.console.print()
        
        return self._ask_bool("Do you want to play again", default=False)

        
    def ask_player_move(
        self,
        current_bid: Bid,
        player: Player,
        dice_cnt: int,
        wild_ones: bool = False
        ):
        
        player_dice = player.values
        #* Show human_player hand,
        symbols = " ".join(self.FACE_SYMBOLS[v] for v in sorted(player_dice))
        self.console.print(f"\n  [bold yellow]Your dice:[/bold yellow] {symbols}  "
                      f"[dim]({', '.join(str(v) for v in sorted(player_dice))})[/dim]") 
        
        #* Show current_bid
        if current_bid is not None:
            self.console.print(f"\n  [bold]Current bid:[/bold] [cyan]{current_bid}[/cyan]")
            
        #* Show dice_count
        self.console.print(f"  [dim]Total dice on table: {dice_cnt}[/dim]")
        
        #* Show wild_ones mode
        if wild_ones:
            self.console.print(f"  [dim magenta]Wild Ones active — 1s count as any face[/dim magenta]")
        
        self.console.print()
        #* Ask for move
        if current_bid is not None:
            self.console.print("\n  [bold]Your move:[/bold]")
            self.console.print("  [green][1][/green] Raise the bid")
            self.console.print("  [red][2][/red] Challenge — call LIAR!")
            choice = Prompt.ask("  Choose", choices=["1", "2"])
            
            if choice == "2":
                return ("Challenge", None)
                
                
        return ("Bid", self._ask_bid())
                    
            
    def _ask_bid(self) -> tuple[int, int]:
        """Returns (for_face, dice_cnt)"""
        cnt = self._ask_number("Quantity (how many dice)")
        face = self._ask_number("Face value (1-6)", 1, 6, "Please enter valid die face")
        
        return (face, cnt)
    
    
    def show_message(self, msg: str):
        print(msg) 
        
        
    def show_error(self, error_msg: str = "Error"):
        self.console.print(f"[red]{error_msg}[/red]")
      
      
    def ask_confirmation(self, msg: str = "Press Enter to continue..."):        
        self.console.print(msg, end='')
        input()
        

    def _ask_player_name(self, reserved_names: set[str]) -> str:
        
        while True:
            p_name = Prompt.ask("[bold yellow]Your name, challenger[/bold yellow]", default="Captain")
            
            if len(p_name) > 15:
                self.show_error("Name too long, max - 15")
                continue
            if p_name in reserved_names:
                self.show_error("Name is reserved by AI player")
                continue
            
            return p_name

         
    def _ask_bool(self, msg: str, default: bool) -> bool:
        return Confirm.ask(msg, case_sensitive=False, default = default)


    def _ask_number(
        self,
        msg: str,
        min_value:int = None,
        max_value: int = None,
        error_msg: str = ""
        ) -> int:
        """Ask user to type in valid number.
        Optinally provide validation range with min & max & guiding error msg"""
        while True:
            value = IntPrompt.ask(msg)
            
            if (
                (min_value is not None and value < min_value) or 
                (max_value is not None and value > max_value)
            ):
                self.show_error(error_msg)
                continue
                
            return value
            

        
      
                

