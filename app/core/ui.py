# app/core/ui.py
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.theme import Theme
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

class UIService:
    def __init__(self):
        self.theme = Theme({
            "pda.low": "#005f5f",
            "pda.mid": "#00afaf",
            "pda.hi": "#00ffff",
            "pda.warn": "bold magenta",
            "pda.error": "bold red"
        })
        self.console = Console(theme=self.theme)

    def idle_scan(self, duration=1.2):
        """Анимация спутника и сканирования частот"""
        msg = Text(" 🛰️ PDA: СИНХРОНИЗАЦИЯ СО СПУТНИКОМ... СЕКТОР ЧИСТ", style="pda.mid")
        with Live(Spinner("earth", text=msg), refresh_per_second=10, transient=True):
            time.sleep(duration)

    def show_engine_boot(self):
        """Тот самый 'Квантовый' прогрев систем при старте"""
        with Progress(
            SpinnerColumn(spinner_name="simpleDotsScrolling"),
            TextColumn("[pda.mid]{task.description}"),
            BarColumn(bar_width=None, pulse_style="pda.hi"),
            console=self.console, transient=True
        ) as prg:
            prg.add_task("Инициализация квантового ядра Nexus...", total=None)
            time.sleep(0.8)
            prg.add_task("Загрузка архитектурных паттернов Грегори...", total=None)
            time.sleep(0.6)
            prg.add_task("Установка защищенного канала связи...", total=None)
            time.sleep(0.4)

    def print_header(self, ai_status: str):
        header_text = (
            "[bold pda.hi]NEXUS AI CORE [v3.0][/bold pda.hi]\n"
            f"[pda.low]Status: Online | Node: {ai_status}[/pda.low]"
        )
        self.console.print(Panel(
            header_text,
            border_style="pda.mid",
            title="[SYSTEM TERMINAL]",
            subtitle="[ENCRYPTED]"
        ))

    def show_advanced_progress(self):
        """Глубокое сканирование с квантованием (то, что ты любишь)"""
        with Progress(
                SpinnerColumn(spinner_name="dots12"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40, pulse_style="pda.hi"),
                TaskProgressColumn(),
                console=self.console,
                transient=True
        ) as progress:
            t1 = progress.add_task("[pda.low]Поиск в векторных слоях...", total=100)
            t2 = progress.add_task("[pda.mid]Извлечение контекста Грегори...", total=100)
            t3 = progress.add_task("[pda.hi]Квантование ответа Gemini...", total=100)

            while not progress.finished:
                progress.update(t1, advance=2.5)
                progress.update(t2, advance=1.8)
                progress.update(t3, advance=1.2)
                time.sleep(0.015)

    def get_input(self) -> str:
        self.console.print("[pda.hi]🖵 [PDA_READY][/pda.hi]")
        return self.console.input("[bold green]>>> [/bold green]")