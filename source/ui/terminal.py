from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.player.base.player import Player
    from collections import Counter

import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box


import utility.constants as const
from ui.base.ui import GameUI
from models.bid import Bid
from utility.type_parsing import try_parse_int, try_parse_bool

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
        
        
    def start_game(self, players: list[Player], wild_ones: bool):
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
        
        
        
    def show_round(self, round_num: int, players: list[Player], wild_ones: bool):
        self.console.print()
        self.console.rule(f"[bold yellow]⚔  Round {round_num}  ⚔[/bold yellow]", style="yellow")

        table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
        table.add_column("Player", style="bold")
        table.add_column("Dice", justify="center")
        table.add_column("Status", justify="center")

        for p in players:
            dice_bar = "🎲" * p.cnt_dice
            tag = "[green]Bot[/green]" if p.is_bot else "[yellow]You[/yellow]"
            table.add_row(p.name, dice_bar or "[red]—[/red]", tag)

        self.console.print(table)

        if wild_ones:
            self.console.print("  [magenta bold]★ Wild Ones Mode Active ★[/magenta bold]  "
                        "[dim]1s count as any face[/dim]\n")
        
        
        
        
    def show_turn(self, player_name: str, is_bot: bool):
        style = "cyan" if is_bot else "yellow"
        icon = "🤖" if is_bot else "🧑"
        self.console.print()
        self.console.rule(f"[{style}]{icon}  {player_name}'s Turn[/{style}]", style=style)
        
        
        
        
    def show_reveal(self, players: list[Player], dice_face_count: Counter, wild_ones: bool):
        self.console.print()
        self.console.rule("[bold red]🎲  REVEAL  🎲[/bold red]", style="red")
        self.console.print()
        
        for p in players:
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
        
            
            
    
    def show_round_result(self, loser_name: str, loser_is_bot: bool, eliminated: bool, bid_str: str, challenger_name: str, bid_valid: bool):
        self.console.print()
        if bid_valid:
            self.console.print(Panel(
                f"[green bold]Bid stands![/green bold]\n"
                f"[dim]{bid_str} — it was real![/dim]\n\n"
                f"[red]{'🤖' if loser_is_bot else '🧑'} {challenger_name} challenged too soon — loses a die.[/red]",
                border_style="green", padding=(0, 2)
            ))
        else:
            self.console.print(Panel(
                f"[red bold]Bluff called![/red bold]\n"
                f"[dim]{bid_str} — wasn't there![/dim]\n\n"
                f"[red]{'🤖' if loser_is_bot else '🧑'} {loser_name} was bluffing — loses a die.[/red]",
                border_style="red", padding=(0, 2)
            ))
        if eliminated:
            self.console.print(f"\n  [bold red]💀 {loser_name} is eliminated![/bold red]")
        time.sleep(1.5)
        
        
        
        
    def show_winner(self, player_name: str, is_bot: bool):
        self.console.print()
        self.console.rule("[bold yellow]🏆  GAME OVER  🏆[/bold yellow]", style="yellow")
        icon = "🤖" if is_bot else "🎉"
        self.console.print()
        self.console.print(
            Panel.fit(
                f"{icon}  [bold yellow]{player_name} wins![/bold yellow]  {icon}\n"
                f"[dim]Last die standing.[/dim]",
                border_style="yellow",
                padding=(1, 6),
            )
        )
        self.console.print()
        
        
        
        
    def get_set_up_vars(self) -> dict:

        setup = {}
        
        setup["cnt_ai"] = self._ask_ai_count(
            const.CNT_MIN_PLAYERS - 1, # -1 for the human player
            const.CNT_MAX_PLAYER - 1,  # -1 for the human player
            const.SUGGESTION_AI_PLAYER_CNT
            )
        setup["player_name"] = self._ask_player_name(const.SUGGESTION_PLAYER_NAME)
        setup["wild_ones"] = self._ask_wild_ones()
        print()
        return setup
        
        
        
    def ask_player_move(self,
        current_bid: Bid,
        player_dice: list[int],
        dice_cnt: int,
        wild_ones: bool = False):
        
        #* Show human_player hand,
        symbols = " ".join(self.FACE_SYMBOLS[v] for v in sorted(player_dice))
        self.console.print(f"\n  [bold yellow]Your dice:[/bold yellow] {symbols}  "
                      f"[dim]({', '.join(str(v) for v in sorted(player_dice))})[/dim]") 
        
        #* Show current_bid
        if current_bid is not None:
            self.console.print(f"\n  [bold]Current bid:[/bold] [cyan]{current_bid}[/cyan]")
            self.console.print(f"  [dim]Total dice on table: {dice_cnt}[/dim]")
            
        #* Show dice_count
        self.console.print(f"  [dim]Total dice on table: {dice_cnt}[/dim]")
        
        #* Show wild_ones mode
        if wild_ones:
            self.console.print(f"  [dim magenta]Wild Ones active — 1s count as any face[/dim magenta]")
        
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
        cnt = self._ask_number("Quantity (how many dice): ")
        face = self._ask_number("Face value (1-6): ")
        
        return (face, cnt)
    
    
    def show_message(self, msg: str):
        print(msg) 
        
        
    def ask_confirmation(self, msg: str = "Press Enter to continue..."):
        self.console.print(msg)
        input()
        
        
    def _ask_ai_count(self, min_cnt: int, max_cnt: int, suggestion: int) -> int:
        while not min_cnt <= (
            number:= self._ask_number(f"Enter count of AI enemies [{min_cnt}:{max_cnt}]({suggestion}): ")
        ) <= max_cnt:
            
            print("\tInvalid AI count!")
            
        return number


    def _ask_player_name(self, suggestion: str) -> str:
        reserved_names = {name for name in const.AI_PLAYERS.keys()}
        
        while True:
            self.console.print(
                "[bold yellow]Your name, challenger[/bold yellow]"
                f"[cyan]({suggestion})[/cyan]")
            
            p_name = input()
            
            if not 0 < len(p_name) < 30:
                print("\tCannot accept empty name!")
                continue
            if p_name in reserved_names:
                print("\tName is reserved by AI player!")
                continue
            
            return p_name

            
            
    def _ask_wild_ones(self) -> bool:
        while True:
            try:
                self.console.print(
                    "[bold]Enable Wild Ones mode?[/bold] "
                    "[dim](1s count as any face)[/dim]"
                    "[magenta bold](y/n)[/magenta bold] "
                    "[cyan bold](n)[/cyan bold]: "
                    )
                return try_parse_bool(input())
            except ValueError:
                print("[red]Please enter Y or N[/red]")


    def _ask_number(self, msg: str):
        while True:
            try:
                return try_parse_int(input(msg))
            except ValueError:
                self.console.print("[red]Number input is required![/red]")
                

