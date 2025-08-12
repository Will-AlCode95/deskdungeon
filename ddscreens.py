from textual.app import ComposeResult
from textual.widgets import (
    Header, Footer, Label, Input, Static,
    Button, Select, ListItem
)
from textual.screen import Screen
from textual.containers import VerticalGroup
from textual.binding import Binding
from textual.message import Message

import ddmodel as model


class TelaInicial(Screen):

    CSS = """
    #game_title {
        color: magenta;
    }

    Static {
        content-align: center middle;        
        color: cyan;        
    }

    VerticalGroup {
        align: center middle;
        height: 100%;
    }
"""

    def compose(self) -> ComposeResult:
        yield Header()

        yield VerticalGroup(
            Static("𝕯𝖊𝖘𝕶 𝕯𝖚𝖓𝖌𝖊𝖔𝖓", id="game_title"),
            Static(),
            Static("𝓾𝓶 𝓭𝓾𝓷𝓰𝓮𝓸𝓷 𝓬𝓻𝓪𝔀𝓵𝓮𝓻"),
            Static("𝓮𝓶 𝓶𝓸𝓭𝓸 𝓽𝓮𝔁𝓽𝓸")
        )        
        yield Footer()
    
    def on_screen_resume(self):
        if not model.JOGADOR.nome == "sem nome":
            self.sub_title = f"({model.JOGADOR.nome})"

class TelaNovoJogador(Screen):

    CSS = '''
    Static {
        content-align: center middle;
        color: cyan;
        padding: 1;
    }
'''
    BINDINGS = [
        Binding("ctrl+s", "salvar", "Salvar"),
        Binding("ctrl+n", "novo_item", "Novo Item")
    ]

    def compose(self):
        yield Header()
        yield Static("𝕹𝖔𝖛𝖔 𝕵𝖔𝖌𝖆𝖉𝖔𝖗")
        yield Label("Nome")
        yield Input(id="tx_nome")
        yield Label("Classe")   
        yield Select([
            ("Mago", "mago"),
            ("Cavaleiro", "cavaleiro"),
            ("Assassina", "assassina")], id="sl_classe")        
        yield Static(f"Item equipado: {model.JOGADOR.item_equipado.get_nome()}",id="stt_item_equipado")        
        yield Footer()

    def action_novo_item(self):
        # Atualiza Model
        model.JOGADOR.item_equipado = Item()
        # Atualiza View
        stt_item = self.query_one("#stt_item_equipado",Static)
        stt_item.update(f"Item equipado: {model.JOGADOR.item_equipado.get_nome()}")


    def action_salvar(self):
        nome = self.query_one("#tx_nome",Input).value
        classe = self.query_one("#sl_classe", Select).value
        # Atualizamos a model
        model.JOGADOR.nome = nome
        model.JOGADOR.classe = classe        
        self.notify("Jogador salvo")


class WidgetItens(Static):

    class Pegou(Message):
        def __init__(self):
            super().__init__()

    def on_mount(self):
        yield Static(self.get_conteudo())

    def get_conteudo(self):
        conteudo = str()
        for item in model.CENA_ATUAL.itens.keys():
            conteudo += f"[@click=pegar('{item}')]Pegar[/]: {item}\n"

        return conteudo

    def action_pegar(self, item):
        # Acesso a model, causando uma mudança
        model.pegar_item(item)        
        # Eu já me atualizo, mostrando as modificações da minha model
        self.update(self.get_conteudo())
        # Aviso "os outros" do que aconteceu comigo
        self.post_message(self.Pegou())

class WidgetInventario(Static):
    def on_mount(self):
        yield Static(self.get_conteudo())
    
    def get_conteudo(self):
        conteudo = "Inventário:\n"
        for item in model.JOGADOR.inventario.keys():
            conteudo += f"{item}\n"
        
        return conteudo

class TelaJogo(Screen):

    CSS = """"""
    SUB_TITLE = ""

    BINDINGS = [
        Binding("up","norte", "Norte"),
        Binding("down","sul", "Sul"),
        Binding("right","leste", "Leste"),
        Binding("left","oeste", "Oeste"),        
    ]

    
    def compose(self):
        yield Header()
        yield Static(f'Cena: {model.CENA_ATUAL.nome}', id="stt_nome_cena_atual")
        yield WidgetItens()
        yield Static(f'Jogador: {model.JOGADOR.nome}', id="stt_nome_jogador")
        yield WidgetInventario()        
        yield Footer()

    def atualizar_jogador(self):
        stt_nome_jogador = self.query_one("#stt_nome_jogador",Static)
        stt_nome_jogador.update(f'Jogador: {model.JOGADOR.nome}')

        widget_inventario = self.query_one("WidgetInventario", WidgetInventario)
        widget_inventario.update(widget_inventario.get_conteudo())


    def atualizar_cena(self):
        stt_nome_cena_atual = self.query_one("#stt_nome_cena_atual",Static)
        stt_nome_cena_atual.update(f'Cena: {model.CENA_ATUAL.nome}')

        widget_itens = self.query_one('WidgetItens', WidgetItens)
        widget_itens.update(widget_itens.get_conteudo())

    def on_widget_itens_pegou(self, evento:WidgetItens.Pegou):
        self.atualizar_jogador()

    def on_screen_resume(self):
        self.atualizar_cena()
        self.atualizar_jogador()        

    def action_norte(self):              
        if model.CENA_ATUAL.norte:
            model.CENA_ATUAL = model.CENA_ATUAL.norte
            self.atualizar_cena()

    def action_sul(self):
        if model.CENA_ATUAL.sul:
            model.CENA_ATUAL = model.CENA_ATUAL.sul
            self.atualizar_cena()

    def action_leste(self):
        if model.CENA_ATUAL.leste:
            model.CENA_ATUAL = model.CENA_ATUAL.leste
            self.atualizar_cena()

    def action_oeste(self):
        if model.CENA_ATUAL.oeste:
            model.CENA_ATUAL = model.CENA_ATUAL.oeste
            self.atualizar_cena()