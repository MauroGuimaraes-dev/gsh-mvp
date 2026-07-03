"""
Robô de teste — abre a página de histórico da GSH Corp no Chromium (Playwright) e valida HTTP 200.

Depois mantém o navegador aberto por alguns minutos (útil para demo e logs no dashboard).
O Agent clona o repositório, roda pip + playwright install quando há playwright no requirements.
"""
from __future__ import annotations

import os
import sys
import time

from playwright.sync_api import sync_playwright

# Página alvo da demonstração
URL_ALVO = "https://ri.gshcorp.com.br/sobre-a-gsh-corp/breve-historico/"

# Tempo com o navegador aberto após carregar (demo: 2 min; reduza se o timeout do agendamento for menor)
DURACAO_EXTRA_SEG = 2 * 60
INTERVALO_LOG_SEG = 10


def _headless() -> bool:
    """Em VM sem interface gráfica, use headless=true (padrão). Para ver o browser na tela: PLAYWRIGHT_HEADLESS=false."""
    v = os.environ.get("PLAYWRIGHT_HEADLESS", "true").strip().lower()
    return v in ("1", "true", "yes", "on")


def _playwright_channel() -> str | None:
    """Lê PLAYWRIGHT_CHANNEL do agent/.env (ex.: chrome) repassado pelo subprocesso."""
    v = os.environ.get("PLAYWRIGHT_CHANNEL", "").strip()
    return v or None


def main() -> None:
    headless = _headless()
    channel = _playwright_channel()
    navegador = channel or "Chromium (empacotado)"

    modo = "sem janela (headless)" if headless else "com janela visível"
    print(f"Iniciando Playwright — {navegador} ({modo}). URL: {URL_ALVO}")
    if not headless:
        print(
            "Dica: se não aparecer janela, use Alt+Tab ou veja Chrome/Chromium na barra de tarefas / outro monitor."
        )

    launch_args: list[str] = []
    if not headless:
        launch_args = ["--start-maximized", "--window-position=0,0"]

    launch_kw: dict = {"headless": headless, "args": launch_args}
    if channel:
        launch_kw["channel"] = channel

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kw)
        context = browser.new_context(
            locale="pt-BR",
            user_agent="OrquestradorGSH-RPA-Test/Playwright/1.0",
            no_viewport=not headless,
        )
        page = context.new_page()
        try:
            response = page.goto(URL_ALVO, wait_until="domcontentloaded", timeout=60_000)
        except Exception as e:
            print(f"ERRO ao carregar a página: {e}")
            context.close()
            browser.close()
            sys.exit(1)

        status = response.status if response else 0
        if status != 200:
            print(f"ERRO: HTTP {status} (esperado 200)")
            context.close()
            browser.close()
            sys.exit(1)

        titulo = page.title()
        print(f"OK — página carregada (HTTP 200). Título: {titulo[:160]!r}")

        if not headless:
            try:
                page.bring_to_front()
            except Exception:
                pass

        fim = time.monotonic() + DURACAO_EXTRA_SEG
        passo = 0
        while time.monotonic() < fim:
            dormir = min(INTERVALO_LOG_SEG, fim - time.monotonic())
            if dormir <= 0:
                break
            time.sleep(dormir)
            passo += 1
            restante = max(0, int(fim - time.monotonic()))
            print(f"Ainda em execução… passo {passo} — ~{restante}s restantes (aba GSH aberta).")

        print("Espera concluída. Fechando navegador.")
        context.close()
        browser.close()

    print("Encerrando com sucesso.")
    sys.exit(0)


if __name__ == "__main__":
    main()
