import asyncio
from app.agent.engine import AIEngine

async def main():
    engine = AIEngine()
    answer = await engine.get_answer("Привет! Ты меня слышишь?")
    print(f"ОТВЕТ ИИ: {answer}")

if __name__ == "__main__":
    asyncio.run(main())