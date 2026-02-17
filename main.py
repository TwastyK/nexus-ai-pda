# main.py
import asyncio
import os
import socket
from app.agent.nexus import NexusAgent
from app.core.ui import UIService
from app.core.context import ContextManager
from app.core.logger import AppLogger
from app.ai.factory import ProviderFactory
from app.services.vector_service import VectorService
from app.services.intent_service import IntentClassifier
from app.services.ingestion_service import IngestionService

log = AppLogger("MAIN")


def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


async def main():
    ui = UIService()
    ui.show_engine_boot()  # Визуал при старте

    try:
        # Сборка сервисов
        vector_db = VectorService(threshold=1.5)
        ai_provider = ProviderFactory.get_provider()
        intent_classifier = IntentClassifier(ai_provider)

        # Передаем intent_classifier, чтобы не было ошибки!
        agent = NexusAgent(vector_db=vector_db, intent_classifier=intent_classifier)

        ingestion = IngestionService(vector_db)
        context_manager = ContextManager(max_history=5)

        ui.print_header("FLASH-LATEST")

        # Автозагрузка
        inbox_path = os.path.join(os.getcwd(), "inbox")
        os.makedirs(inbox_path, exist_ok=True)

        with ui.console.status("[pda.mid]PDA: Синхронизация секторов...", spinner="earth"):
            await ingestion.process(inbox_path)

        session_requests = 0

        while True:
            # 1. Спутниковое сканирование (Idle Mode)
            ui.idle_scan(duration=1.2)

            # 2. Ввод пользователя
            user_input = ui.get_input().strip()

            if not user_input: continue
            if user_input.lower() in ['exit', 'quit', 'выход']:
                ui.console.print("[pda.low]Завершение сессии. КПК отключен.[/pda.low]")
                break

            if not is_connected():
                ui.console.print("[pda.error]⚠ СВЯЗЬ ПОТЕРЯНА. Проверь VPN или линк.[/pda.error]")
                continue

            session_requests += 1

            # 3. Визуал "Квантового анализа"
            ui.show_advanced_progress()

            ui.console.print(f"[pda.mid]NEXUS_LINK_#{session_requests} > [/pda.mid]", end="")

            def stream_handler(chunk):
                ui.console.print(chunk, end="", style="pda.hi", highlight=False)

            try:
                # Основная работа агента
                full_response = await agent.chat(
                    user_input,
                    context_manager,
                    stream_callback=stream_handler
                )
                context_manager.add_message("user", user_input)
                context_manager.add_message("assistant", full_response)
                ui.console.print("")

            except Exception as e:
                log.error(f"Ошибка: {e}")
                ui.console.print(f"\n[pda.error]КРИТИЧЕСКИЙ СБОЙ:[/pda.error] {e}")

            ui.console.print("[pda.low]" + "—" * 65 + "[/pda.low]")

    except KeyboardInterrupt:
        ui.console.print("\n[pda.warn]● PDA: Emergency Shutdown (KeyboardInterrupt)[/pda.warn]")
    except Exception as e:
        log.error(f"Критический сбой: {e}")
        ui.console.print(f"\n[pda.error]SYSTEM CRASH:[/pda.error] {e}")


if __name__ == "__main__":
    asyncio.run(main())