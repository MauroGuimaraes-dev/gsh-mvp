# Automação GSH Corp  -  Robô que abre a página do GSH

## Fonte original (código executado pelo Agent)

A fonte original deste robô fica no repositório:
`D:\__PROJETOS 2026\6_GSH\Automações\Testando o Pipeline com rocketbot\Código Python a ser modificado\Gsh\GSH`

O Agent executa o código vindo da URL Git cadastrada no Orquestrador via `git clone`.

## Pasta no monorepo (`robos/GSH`)

Esta pasta é um **backup versionado** (espelho de referência) para histórico e documentação.
Ela **não é** a fonte primária de execução do Agent.

## Fluxo recomendado

1. Editar e validar primeiro em `D:\__PROJETOS 2026\6_GSH\Automações\Testando o Pipeline com rocketbot\Código Python a ser modificado\Gsh\GSH`.
2. Fazer commit/push no repositório remoto oficial do robô (GitHub).
3. Copiar para a pasta de backup no monorepo para manter o histórico alinhado.

## Descrição Técnica
Este robô utiliza **Playwright** para acessar o portal de RI da GSH Corp e validar a disponibilidade da página de histórico.
