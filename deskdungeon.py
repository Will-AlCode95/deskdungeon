from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, Label, Input, Static, Button
)
from textual.screen import Screen
from textual.binding import Binding

from ddscreens import (TelaInicial, TelaNovoJogador, TelaJogo)
from ddmodel import *

class DeskDungeon(App):
    TITLE = "Desk Dungeon"
    SUB_TITLE = "um dungeon crawler modo texto"
    SCREENS = {
        "inicial" : TelaInicial,
        "novo_jogador": TelaNovoJogador,
        "tela_jogo": TelaJogo,
    }

    BINDINGS = [
        Binding("n", "novo_jogador", "Novo Jogador"),
        Binding("j", "tela_jogo", "Jogo"),
        Binding("escape", "tela_inicial", "Início"),
    ]

    def on_mount(self):
        self.push_screen("inicial")

    def action_tela_jogo(self):
        self.switch_screen("tela_jogo")
        
    def action_tela_inicial(self):
        self.switch_screen("inicial")

    def action_novo_jogador(self):
        self.switch_screen("novo_jogador")

if __name__ == "__main__":
    app = DeskDungeon()
    app.run()