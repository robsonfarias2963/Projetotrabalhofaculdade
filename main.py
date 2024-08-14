import os
import sqlite3
from datetime import datetime, timedelta
import threading
import time
from gtts import gTTS
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

# ------------------------------
# Configuração da Interface (KV)
# ------------------------------
kv = """
ScreenManager:
    id: screen_manager
    TelaInicial:
    TelaGerenciamento:
    TelaRelatorio:
    AdicionarMedicamento:
    AdicionarUsuario:
    ExcluirMedicamento:
    ExcluirUsuario:
<TelaInicial>:
    name: 'tela_inicial'
    FloatLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        MDLabel:
            id: titulo_inicio
            text: "Bem-vindo ao Gerenciador de Medicamentos"
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
        
        MDRaisedButton:
            text: "Medicamentos e Usuários"
            on_press: root.ir_para_gerenciamento()
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            size_hint: (0.4, 0.1)
            md_bg_color: 0.2, 0.2, 0.2, 1
            
        
        MDRaisedButton:
            text: "Ver Relatório"
            on_press: root.ir_para_relatorio()
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (0.4, 0.1)
            md_bg_color: 0.2, 0.2, 0.2, 1
        
        MDRaisedButton:
            text: "Sair do Programa"
            on_press: app.stop()
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            size_hint: (0.4, 0.1)
            md_bg_color: 0.2, 0.2, 0.2, 1

<TelaGerenciamento>:
    name: 'tela_gerenciamento'
    FloatLayout:
        MDLabel:
            id: titulo_inicio
            text: "Cadastro de Medicamentos e Usuarios"
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
        
        MDRaisedButton:
            text: 'Adicionar Medicamento'
            on_press: root.ir_para_adicionar_medicamento()
            pos_hint: {'center_x': 0.5, 'center_y': 0.8}
            size_hint: (0.4, 0.1)
        
        MDRaisedButton:
            text: "Adicionar Usuário"
            on_press: root.ir_para_adicionar_usuario()
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            size_hint: (0.4, 0.1)
        
        MDRaisedButton:
            text: "Excluir Medicamento"
            on_press: root.ir_para_excluir_medicamento()
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            size_hint: (0.4, 0.1)
        
        MDRaisedButton:
            text: "Excluir Usuário"
            on_press: root.ir_para_excluir_usuario()
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (0.4, 0.1)
        
        MDRaisedButton:
            text: "Voltar"
            on_press: root.ir_para_inicial()
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            size_hint: (0.4, 0.1)
            md_bg_color: 1, 0, 0, 1

<TelaRelatorio>:
    name: 'tela_relatorio'
    FloatLayout:
        MDLabel:
            id: titulo_inicio
            text: "Relatorio de Medicamentos e Usuarios"
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
                        
        ScrollView:
            size_hint: (1, 0.9)
            do_scroll_x: False
            do_scroll_y: True
            
            MDList:
                id: lista_relatorio
        
        MDRaisedButton:
            text: "Voltar"
            on_press: root.ir_para_inicial()
            pos_hint: {'center_x': 0.5, 'center_y': 0.05}
            size_hint: (0.4, 0.1)
            md_bg_color: 1, 0, 0, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

<AdicionarMedicamento>:
    name: 'adicionar_medicamento'
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Image:
            source: ''
            allow_stretch: True
            keep_ratio: False
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (1, 1)
        
        MDLabel:
            text: "Adicionar Medicamento"
            font_style: 'H6'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.90}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
        
        MDTextField:
            id: nome
            hint_text: 'Nome do Medicamento'
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}
            size_hint: (0.6, 0.05)
        
        MDTextField:
            id: dosagem
            hint_text: 'Dosagem'
            pos_hint: {'center_x': 0.5, 'center_y': 0.68}
            size_hint: (0.6, 0.05)
        
        MDTextField:
            id: horario
            hint_text: 'Horário'
            pos_hint: {'center_x': 0.5, 'y': 0.61}
            size_hint: (0.6, 0.05)
        
        MDRaisedButton:
            text: "Adicionar"
            on_press: root.adicionar_medicamento()
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 1, 0, 1
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
        
        MDRaisedButton:
            text: "Cancelar"
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 0, 0, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

<AdicionarUsuario>:
    name: 'adicionar_usuario'
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Image:
            source: ''
            allow_stretch: True
            keep_ratio: False
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (1, 1)
        
        MDLabel:
            text: "Adicionar Usuário"
            font_style: 'H6'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.90}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
        
        MDTextField:
            id: nome
            hint_text: 'Nome do Usuário'
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}
            size_hint: (0.6, 0.05)
        
        MDTextField:
            id: idade
            hint_text: 'Idade'
            pos_hint: {'center_x': 0.5, 'center_y': 0.68}
            size_hint: (0.6, 0.05)
        
        MDTextField:
            id: peso
            hint_text: 'Peso'
            pos_hint: {'center_x': 0.5, 'y': 0.61}
            size_hint: (0.6, 0.05)
        
        MDRaisedButton:
            text: "Adicionar"
            on_press: root.adicionar_usuario()
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 1, 0, 1
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
        
        MDRaisedButton:
            text: "Cancelar"
            on_press: root.voltar()
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 0, 0, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

<ExcluirMedicamento>:
    name: 'excluir_medicamento'
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Image:
            source: ''
            allow_stretch: True
            keep_ratio: False
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (1, 1)
        
        MDLabel:
            text: "Excluir Medicamento"
            font_style: 'H6'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.90}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
        
        MDTextField:
            id: nome
            hint_text: 'Nome do Medicamento'
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}
            size_hint: (0.6, 0.05)
        
        MDRaisedButton:
            text: "Excluir"
            on_press: root.excluir_medicamento()
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 1, 0, 1
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
        
        MDRaisedButton:
            text: "Cancelar"
            on_press: root.voltar()
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 0, 0, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

<ExcluirUsuario>:
    name: 'excluir_usuario'
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Image:
            source: ''
            allow_stretch: True
            keep_ratio: False
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (1, 1)
        
        MDLabel:
            text: "Excluir Usuário"
            font_style: 'H6'
            halign: 'center'
            size_hint_y: None
            height: dp(30)
            pos_hint: {'center_x': 0.5, 'top': 0.90}
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1
        
        MDTextField:
            id: nome
            hint_text: 'Nome do Usuário'
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}
            size_hint: (0.6, 0.05)
        
        MDRaisedButton:
            text: "Excluir"
            on_press: root.excluir_usuario()
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 1, 0, 1
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
        
        MDRaisedButton:
            text: "Cancelar"
            on_press: root.voltar()
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            size_hint: (0.6, 0.05)
            md_bg_color: 1, 0, 0, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
"""


# ------------------------------
# Funções de Banco de Dados
# ------------------------------
def criar_tabela_medicamentos():
    conn = sqlite3.connect("medicamentos.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS medicamentos (
                 nome TEXT PRIMARY KEY,
                 dosagem TEXT,
                 horario TEXT
                 )"""
    )
    conn.commit()
    conn.close()


def criar_tabela_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            peso REAL
        )
    """
    )
    conn.commit()
    conn.close()


def inicializar_banco_dados():
    conn = sqlite3.connect("medicamentos.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            dosagem TEXT,
            horario TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def inicializar_banco_dados():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute(
        """
          CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            peso REAL
        )
    """
    )
    conn.commit()
    conn.close()


def obter_medicamentos():
    conn = sqlite3.connect("medicamentos.db")
    c = conn.cursor()
    c.execute("SELECT * FROM medicamentos")
    medicamentos = c.fetchall()
    conn.close()
    return medicamentos


def inicializar_banco_dados():
    criar_tabela_medicamentos()
    criar_tabela_usuarios()


# Chame esta função ao iniciar o aplicativo
inicializar_banco_dados()


def obter_usuarios():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    return usuarios


def criar_tabela_usuarios():
    print("Criando tabela de usuários...")
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            peso REAL
        )
    """
    )
    conn.commit()
    conn.close()
    print("Tabela de usuários criada.")


def verificar_tabelas():
    conn = sqlite3.connect("medicamentos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    conn.close()
    print("Tabelas no banco de dados:", tabelas)


verificar_tabelas()


def adicionar_medicamento_db(nome, dosagem, horario):
    conn = sqlite3.connect("medicamentos.db")
    c = conn.cursor()

    # Verificar se o medicamento já existe
    c.execute("SELECT COUNT(*) FROM medicamentos WHERE nome = ?", (nome,))
    count = c.fetchone()[0]

    if count > 0:
        print("Medicamento com este nome já existe.")
        conn.close()
        return

    # Inserir o novo medicamento
    c.execute(
        "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)",
        (nome, dosagem, horario),
    )
    conn.commit()
    conn.close()


def adicionar_usuario_db(nome, idade, peso):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO usuarios (nome, idade, peso) VALUES (?, ?, ?)", (nome, idade, peso)
    )
    conn.commit()
    conn.close()


def excluir_medicamento_db(nome):
    conn = sqlite3.connect("medicamentos.db")
    c = conn.cursor()
    c.execute("DELETE FROM medicamentos WHERE nome= ?", (nome))
    conn.commit()
    conn.close()


def excluir_usuario_db(nome):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()


def obter_medicamentos():
    conn = sqlite3.connect("medicamentos.db")
    c = conn.cursor()
    c.execute("SELECT * FROM medicamentos")
    medicamentos = c.fetchall()
    conn.close()
    return medicamentos


def obter_usuarios():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    return usuarios


# ------------------------------
# Funções de Áudio
# ------------------------------
def reproduzir_audio_thread(self, idioma):
    tela_programa = self.root.get_screen("tela_programa")
    tela_programa.ids.botao_falar.disabled = True
    tela_programa.ids.botao_nova.disabled = True

    try:
        for i in range(1, 11):
            if idioma == "Por":
                texto_audio = f"{self.numero} vezes {i} igual a {self.numero * i}, "
                tts = gTTS(text=texto_audio, lang="pt-br", slow=False)
            elif idioma == "Eng":
                texto_audio = f"{self.numero} times {i} is {self.numero * i}, "
                tts = gTTS(text=texto_audio, lang="en", slow=False)
            elif idioma == "Esp":
                texto_audio = f"{self.numero} por {i}, {self.numero * i}, "
                tts = gTTS(text=texto_audio, lang="es", slow=False)
            elif idioma == "Ita":
                texto_audio = f"{self.numero} per {i}, {self.numero * i}, "
                tts = gTTS(text=texto_audio, lang="it", slow=False)

            audio_seq = f"./{self.numero}.mp3"
            tts.save(audio_seq)
            som = SoundLoader.load(audio_seq)

            if som:
                som.play()
                time.sleep(3.3)
            else:
                self.popup_internet(
                    "Erro de áudio", "Não foi possível reproduzir o áudio."
                )
                break
    except Exception as e:
        self.popup_internet("Conexão", "Erro ao gerar ou reproduzir o áudio.")
    finally:
        tela_programa.ids.botao_falar.disabled = False
        tela_programa.ids.botao_nova.disabled = False


def audio(self, idioma):
    thread = threading.Thread(target=self.reproduzir_audio_thread, args=(idioma,))
    thread.start()


# ------------------------------
# Classes de Tela
# ------------------------------
class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        # Aqui você pode adicionar lógica para verificar o login
        # Por simplicidade, vamos assumir que qualquer login é bem-sucedido
        if self.username.text and self.password.text:
            self.manager.current = "main"


class TelaInicial(Screen):
    def ir_para_gerenciamento(self):
        self.manager.current = "tela_gerenciamento"

    def ir_para_relatorio(self):
        self.manager.current = "tela_relatorio"


class TelaGerenciamento(Screen):
    def ir_para_adicionar_medicamento(self):
        self.manager.current = "adicionar_medicamento"

    def ir_para_adicionar_usuario(self):
        self.manager.current = "adicionar_usuario"

    def ir_para_excluir_medicamento(self):
        self.manager.current = "excluir_medicamento"

    def ir_para_excluir_usuario(self):
        self.manager.current = "excluir_usuario"

    def ir_para_inicial(self):
        self.manager.current = "tela_inicial"


class TelaRelatorio(Screen):
    def on_pre_enter(self, *args):
        self.ids.lista_relatorio.clear_widgets()
        medicamentos = obter_medicamentos()
        usuarios = obter_usuarios()
        for nome, dosagem, horario in medicamentos:
            self.ids.lista_relatorio.add_widget(
                Label(
                    text=f"Medicamento: {nome}, Dosagem: {dosagem}, Horário: {horario}",
                    halign="center",
                )
            )
        for nome, idade, peso in usuarios:
            self.ids.lista_relatorio.add_widget(
                Label(
                    text=f"Usuário: {nome}, Idade: {idade}, Peso: {peso}",
                    halign="center",
                )
            )

    def ir_para_inicial(self):
        self.manager.current = "tela_inicial"


class AdicionarMedicamento(Screen):
    def adicionar_medicamento(self):
        nome = self.ids.nome.text
        dosagem = self.ids.dosagem.text
        horario = self.ids.horario.text
        if nome and dosagem and horario:
            adicionar_medicamento_db(nome, dosagem, horario)
            (
                f" Esta na Hora de Tomar seu medicamento {nome} com dosagem {dosagem} e horário {horario}"
            )
            self.manager.current = "tela_gerenciamento"
        else:
            print("Todos os campos devem ser preenchidos!")


class AdicionarUsuario(Screen):
    def adicionar_usuario(self):
        nome = self.ids.nome.text
        idade = self.ids.idade.text
        peso = self.ids.peso.text
        if nome and idade and peso:
            adicionar_usuario_db(nome, int(idade), float(peso))
            (f"Adicionar usuário {nome} com idade {idade} e peso {peso}")
            self.manager.current = "tela_gerenciamento"
        else:
            print("Todos os campos devem ser preenchidos!")

    def ir_para_inicial(self):
        self.manager.current = "tela_inicial"


class ExcluirMedicamento(Screen):
    def excluir_medicamento(self):
        nome = self.ids.nome.text
        if nome:
            excluir_medicamento_db(nome)
            (f"Excluir medicamento {nome}")
            self.manager.current = "tela_gerenciamento"
        else:
            print("O campo nome deve ser preenchido!")


class ExcluirUsuario(Screen):
    def excluir_usuario(self):
        nome = self.ids.nome.text
        if nome:
            excluir_usuario_db(nome)
            (f"Excluir usuário {nome}")
            self.manager.current = "tela_gerenciamento"
        else:
            print("O campo nome deve ser preenchido!")


class GerenciadorApp(MDApp):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    GerenciadorApp().run()
