import asyncio
import time
from rich.console import Console

console = Console()


async def unix_test():
    # Проверка "бесконечного" спиннера
    with console.status("[bold cyan]Запуск бесконечного теста Nexus...", spinner="moon") as status:
        for i in range(1, 11):
            status.update(f"[bold cyan]Nexus: Тест системы #{i} (Поток живой)...")
            # Имитируем нагрузку, но даем asyncio переключать контекст
            await asyncio.sleep(1)
            console.log(f"Этап {i} завершен успешно")

    console.print("[bold green]Тест пройден. Если ты видел луну — терминал в порядке![/bold green]")


if __name__ == "__main__":
    asyncio.run(unix_test())