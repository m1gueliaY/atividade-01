"""Kit da Atividade 01 — O Raio-X do Seu Negócio.

Cenário: você é fundador(a) de um pequeno negócio digital brasileiro,
sorteado e personalizado a partir da sua matrícula. Todos os exercícios
aplicam ferramentas de Python aos números REAIS (personalizados) do SEU
negócio: ficha do negócio, CAC vs. LTV, crescimento do faturamento (CAGR),
o código do seu último pedido, e a projeção até a meta.

O notebook do aluno usa seis funções, e é só isso::

    iniciar(matricula, nome)      liga o kit e cria os seus dados
    prever(**respostas)           carimba a sua previsão antes de revelar
    registrar(etapa, nota)        marca uma etapa no diário de bordo
    conferir(etapa, **respostas)  devolve um retorno sobre o que você resolveu
    diario()                      mostra o seu ritmo de trabalho
    assinatura()                  emite a linha de entrega

Nada aqui usa rede, arquivo externo ou biblioteca de terceiros.

**Nível de estruturas: 1** — só escalares (números e textos soltos). A
Atividade 01 cobre as Aulas 1–5, então o aluno ainda não tem `if`, laços
nem funções — só indexação e fatiamento de strings (Aula 5). O kit não pode
entregar nenhuma dessas coisas ainda.

Este arquivo é legível de propósito: se você quiser entender de onde saíram
os seus números, leia o código. A mecânica compartilhada (semente, diário,
assinatura) mora em ``core.py``.
"""

from . import core
from .core import (
    checar_bool,
    checar_igual,
    checar_numero,
    checar_texto_contem,
)

ATIVIDADE = "a01"
VERSAO = "1.0"

# ---------------------------------------------------------------- o painel
# (nome, uf, categoria, prefixo do código de pedido, faturamento mensal em
# R$, ticket médio mensal por cliente em R$, clientes ativos/mês, CAC em
# R$, churn mensal em %)
#
# ⚠️ Valores são APROXIMAÇÕES DIDÁTICAS para tornar as contas legíveis em
# sala — não são estatísticas de mercado reais e não devem ser citadas como
# tais.
#
# O painel tem **43 linhas** — um número primo maior que a turma máxima
# prevista (40) — para garantir que cada aluno receba um negócio diferente,
# mesmo que as matrículas da turma avancem de 2 em 2 ou de 3 em 3.
#
# A composição cobre 11 categorias do empreendedorismo digital brasileiro, e
# inclui DE PROPÓSITO ~10 negócios com unit economics ruim (CAC alto demais
# para o LTV) — como as anomalias do painel de municípios do ppge-pad-lab,
# são casos que valem discussão em sala: nem todo negócio saudável em
# faturamento tem uma aquisição de cliente saudável.
_PAINEL = [
    # moda (MOD)
    ("Ateliê Flor de Lis", "SP", "moda", "MOD", 22000.0, 180.0, 220, 28.0, 10.0),
    ("Trama Urbana", "RJ", "moda", "MOD", 31000.0, 210.0, 260, 32.0, 9.0),
    ("Closet da Ana", "MG", "moda", "MOD", 15500.0, 140.0, 190, 22.0, 12.5),
    ("Verve Streetwear", "PE", "moda", "MOD", 27000.0, 195.0, 240, 2200.0, 11.0),
    # pet (PET)
    ("Patinhas Felizes", "SP", "pet", "PET", 18000.0, 130.0, 240, 28.0, 7.5),
    ("Miau & Cia", "RS", "pet", "PET", 14000.0, 110.0, 210, 24.0, 8.0),
    ("Cão Doido Pet Shop", "PR", "pet", "PET", 21000.0, 150.0, 250, 33.0, 6.5),
    ("Bicho Solto", "BA", "pet", "PET", 12500.0, 95.0, 190, 1000.0, 9.5),
    # delivery (DEL)
    ("Sabor Express", "SP", "delivery", "DEL", 42000.0, 62.0, 900, 12.0, 22.0),
    ("Fominha Delivery", "RJ", "delivery", "DEL", 35000.0, 55.0, 780, 10.0, 25.0),
    ("Panela de Barro Delivery", "BA", "delivery", "DEL", 28000.0, 48.0, 680, 9.0, 19.0),
    ("Prato Rápido", "CE", "delivery", "DEL", 24000.0, 45.0, 640, 244.0, 20.5),
    # educação (EDU)
    ("Aprendex Cursos", "MG", "educação", "EDU", 19000.0, 280.0, 110, 65.0, 6.0),
    ("Fluência Fácil Idiomas", "SP", "educação", "EDU", 26000.0, 320.0, 140, 80.0, 5.0),
    ("Academia do Código", "PB", "educação", "EDU", 22000.0, 350.0, 105, 95.0, 5.5),
    ("Notas & Acordes Música", "RS", "educação", "EDU", 13000.0, 220.0, 90, 2418.0, 7.0),
    # beleza (BEL)
    ("Studio Bela Face", "SP", "beleza", "BEL", 17000.0, 160.0, 180, 30.0, 8.5),
    ("Barbearia Navalha de Ouro", "RJ", "beleza", "BEL", 15000.0, 95.0, 280, 18.0, 6.0),
    ("Espaço Renove Estética", "PE", "beleza", "BEL", 21000.0, 200.0, 170, 38.0, 9.0),
    ("Tinta na Pele Tatuagem", "PR", "beleza", "BEL", 19500.0, 380.0, 80, 4750.0, 4.0),
    # fitness (FIT)
    ("Respira Yoga Studio", "SP", "fitness", "FIT", 11000.0, 180.0, 110, 42.0, 9.0),
    ("Corpo em Movimento Pilates", "MG", "fitness", "FIT", 14500.0, 210.0, 120, 50.0, 8.0),
    ("PersonalFit Online", "RS", "fitness", "FIT", 9500.0, 150.0, 100, 35.0, 10.5),
    ("Vitalis Academia", "CE", "fitness", "FIT", 24000.0, 130.0, 280, 1615.0, 11.5),
    # casa (CAS)
    ("Casa Encantada Decor", "SP", "casa", "CAS", 13000.0, 120.0, 170, 25.0, 13.0),
    ("Papelaria Girassol", "PB", "casa", "CAS", 9000.0, 85.0, 180, 16.0, 11.0),
    ("Lar Doce Lar Ateliê", "BA", "casa", "CAS", 10500.0, 100.0, 155, 20.0, 14.5),
    ("Cantinho Zen Decorações", "PR", "casa", "CAS", 12000.0, 135.0, 140, 1227.0, 10.0),
    # tecnologia (TEC)
    ("ReBoot Eletrônicos", "SP", "tecnologia", "TEC", 34000.0, 310.0, 160, 55.0, 12.0),
    ("TechNova Usados", "RJ", "tecnologia", "TEC", 29000.0, 280.0, 150, 48.0, 13.5),
    ("Circuito Reuso", "MG", "tecnologia", "TEC", 21000.0, 250.0, 120, 42.0, 10.5),
    ("GadgetLar", "DF", "tecnologia", "TEC", 26000.0, 290.0, 135, 1648.0, 11.0),
    # artesanato (ART)
    ("Brechó Retrô Vibe", "SP", "artesanato", "ART", 8000.0, 75.0, 160, 14.0, 12.0),
    ("Mãos que Criam Artesanato", "PB", "artesanato", "ART", 6500.0, 68.0, 140, 12.0, 13.5),
    ("Segunda Vida Brechó", "RS", "artesanato", "ART", 9500.0, 82.0, 175, 16.0, 11.5),
    ("Fio & Arte", "PE", "artesanato", "ART", 7000.0, 70.0, 145, 588.0, 14.0),
    # gastronomia (GAS)
    ("Café das Letras", "SP", "gastronomia", "GAS", 16000.0, 42.0, 560, 9.0, 16.0),
    ("Sorveteria Polar Doce", "CE", "gastronomia", "GAS", 19000.0, 38.0, 680, 7.0, 18.5),
    ("Doceria da Vovó", "MG", "gastronomia", "GAS", 13000.0, 45.0, 420, 8.0, 15.0),
    ("Confeitaria Flor de Açúcar", "BA", "gastronomia", "GAS", 15500.0, 50.0, 460, 309.0, 13.5),
    # serviços (SRV)
    ("Lava & Leva Lavanderia", "SP", "serviços", "SRV", 11500.0, 95.0, 180, 20.0, 12.5),
    ("Faxina Já", "RJ", "serviços", "SRV", 14000.0, 120.0, 155, 24.0, 11.0),
    ("Oficina do Seu Zé", "PR", "serviços", "SRV", 17500.0, 145.0, 190, 28.0, 9.5),
]

_ANOS_FOCO = [2024, 2025, 2026]
_JANELAS = [2, 3, 4]  # tamanho da série histórica do faturamento, em anos
_CANAIS = ["A", "W", "M"]  # A=app, W=site próprio, M=marketplace

#: Ano-alvo fixo da meta de faturamento (Exercício 5) — horizonte varia
#: conforme o ano foco do aluno, exatamente como a meta 2030 do modelo.
META_ANO = 2029

#: Ticket médio mensal acima do qual o negócio é considerado "alto ticket".
CORTE_ALTO_TICKET = 300.0

#: Razão LTV/CAC de referência ("regra dos 3x") usada no Exercício 2.
RAZAO_LTV_CAC_SAUDAVEL = 3.0


# ------------------------------------------------------------ geração
def _gerar(matricula, ger):
    """Deriva os dados personalizados do aluno a partir da matrícula.

    A **ordem dos sorteios** abaixo é parte do contrato: mudá-la muda os
    dados de toda a turma e invalida as assinaturas já emitidas. Se precisar
    alterar, suba ``VERSAO``.
    """
    nome, uf, categoria, prefixo, faturamento, ticket, clientes, cac, churn = (
        _PAINEL[core.indice_sem_colisao(matricula, len(_PAINEL))]
    )

    ano = _ANOS_FOCO[ger.randrange(len(_ANOS_FOCO))]
    faturamento = round(core.perturbar(faturamento, ger, 0.10, minimo=2000.0), 2)
    ticket = round(core.perturbar(ticket, ger, 0.10, minimo=15.0), 2)
    clientes = round(core.perturbar(clientes, ger, 0.10, minimo=20.0))
    cac = round(core.perturbar(cac, ger, 0.12, minimo=3.0), 2)
    churn = round(core.perturbar(churn, ger, 0.15, minimo=1.0, maximo=40.0), 2)

    # série histórica: o faturamento de hoje, "desandado" por um crescimento
    # observado que pode ser negativo — negócio digital jovem também encolhe,
    # e o exercício de CAGR precisa disso.
    janela = _JANELAS[ger.randrange(len(_JANELAS))]
    observado = ger.uniform(-0.20, 0.70)
    faturamento_base = round(faturamento / (1 + observado) ** janela, 2)

    sequencial = ger.randrange(10000, 100000)
    canal = _CANAIS[ger.randrange(len(_CANAIS))]
    codigo_pedido = f"{prefixo}-{ano}-{uf}-{sequencial}-{canal}"

    return {
        "MEU_NEGOCIO": nome,
        "MINHA_UF": uf,
        "MINHA_CATEGORIA": categoria,
        "MEU_ANO": ano,
        "MEU_FATURAMENTO": faturamento,
        "MEU_ANO_BASE": ano - janela,
        "MEU_FATURAMENTO_BASE": faturamento_base,
        "MEU_TICKET_MEDIO": ticket,
        "MEUS_CLIENTES_ATIVOS": clientes,
        "MEU_CAC": cac,
        "MINHA_CHURN": churn,
        "MEU_CODIGO_PEDIDO": codigo_pedido,
        "MEU_CRESCIMENTO": round(ger.uniform(5.0, 35.0), 2),
        "MINHA_META": round(faturamento * ger.uniform(1.5, 4.0), -2),
        "MINHAS_PARCELAS": ger.randrange(12, 49),
        "MINHA_PARCELA": round(ger.uniform(150.0, 3000.0), 2),
    }


def _apresentar(d):
    """Imprime o briefing do fundador no Passo 0."""
    print(f"🚀  Negócio: {d['MEU_NEGOCIO']} ({d['MINHA_UF']}) — {d['MINHA_CATEGORIA']}")
    print(f"    MEU_FATURAMENTO ....... R$ {d['MEU_FATURAMENTO']:.2f} /mês")
    print(f"    MEU_TICKET_MEDIO ...... R$ {d['MEU_TICKET_MEDIO']:.2f} /cliente/mês")
    print(f"    MEUS_CLIENTES_ATIVOS .. {d['MEUS_CLIENTES_ATIVOS']}")
    print()
    print("📈  Série do faturamento")
    print(f"    MEU_ANO_BASE ........... {d['MEU_ANO_BASE']}")
    print(f"    MEU_FATURAMENTO_BASE ... R$ {d['MEU_FATURAMENTO_BASE']:.2f}")
    print(f"    MEU_ANO ................ {d['MEU_ANO']}")
    print(f"    MEU_FATURAMENTO ........ R$ {d['MEU_FATURAMENTO']:.2f}")
    print()
    print("💰  Aquisição e retenção de clientes")
    print(f"    MEU_CAC ................ R$ {d['MEU_CAC']:.2f}")
    print(f"    MINHA_CHURN ............ {d['MINHA_CHURN']:.2f}% ao mês")
    print()
    print("🎯  Plano de crescimento")
    print(f"    MEU_CRESCIMENTO ........ {d['MEU_CRESCIMENTO']}% a.a. (projeção)")
    print(f"    MINHA_META .............. R$ {d['MINHA_META']:.2f} "
          f"(faturamento mensal até {META_ANO})")
    print()
    print("🧾  Último pedido registrado")
    print(f"    MEU_CODIGO_PEDIDO ...... {d['MEU_CODIGO_PEDIDO']!r}")
    print()
    print("🏗️  Investimento inicial")
    print(f"    MINHAS_PARCELAS ........ {d['MINHAS_PARCELAS']} parcelas mensais")
    print(f"    MINHA_PARCELA .......... R$ {d['MINHA_PARCELA']:.2f} por mês")


# ------------------------------------------------------------ as réguas
# Estas funções são a "resposta" do professor. Existem separadas das
# checagens para que a regra fique escrita uma vez só — e para que o
# gabarito e a conferência nunca divirjam.
def ltv(ticket_medio, churn_pct):
    return ticket_medio / (churn_pct / 100)


def parecer_meta(projetado, meta):
    if projetado >= meta:
        return "✅ meta alcançada"
    if projetado >= 0.90 * meta:
        return "⚠️ meta próxima, exige aceleração"
    return "❌ meta inalcançável no ritmo atual"


# ------------------------------------------------------------ checagens
def _checagens(etapa, r, d):
    """Monta a lista de checagens de uma etapa: ``[(ok, mensagem), ...]``.

    Todos os valores esperados são recalculados a partir de ``d`` — os
    mesmos números **já arredondados** que o aluno vê. Nunca a partir de
    valores intermediários da geração, senão a conferência discorda do
    enunciado na terceira casa decimal.
    """
    faturamento = d["MEU_FATURAMENTO"]
    faturamento_base = d["MEU_FATURAMENTO_BASE"]
    ticket = d["MEU_TICKET_MEDIO"]
    churn = d["MINHA_CHURN"]
    cac = d["MEU_CAC"]
    meta = d["MINHA_META"]
    codigo = d["MEU_CODIGO_PEDIDO"]
    anos_serie = d["MEU_ANO"] - d["MEU_ANO_BASE"]
    horizonte = META_ANO - d["MEU_ANO"]

    if etapa == "exercicio-1":
        return [
            checar_numero(
                "receita_anual", r.get("receita_anual"), faturamento * 12,
                "MEU_FATURAMENTO está em R$ por MÊS — o ano tem 12 meses.",
            ),
            checar_bool(
                "alto_ticket", r.get("alto_ticket"),
                ticket > CORTE_ALTO_TICKET,
                f"o corte de alto ticket é R$ {CORTE_ALTO_TICKET:.2f} — "
                "compare com MEU_TICKET_MEDIO, sem se esquecer do sinal >.",
            ),
            checar_texto_contem(
                "ficha", r.get("ficha"),
                [d["MEU_NEGOCIO"], d["MINHA_UF"], d["MINHA_CATEGORIA"]],
                "Use as variáveis dentro das chaves da f-string, não o "
                "texto digitado à mão.",
            ),
        ]

    if etapa == "exercicio-2":
        ltv_calc = ltv(ticket, churn)
        return [
            checar_numero(
                "ltv", r.get("ltv"), ltv_calc,
                "LTV = ticket médio mensal ÷ (churn mensal em FRAÇÃO, não "
                "percentual — divida por 100 antes).",
            ),
            checar_numero(
                "razao_ltv_cac", r.get("razao_ltv_cac"), ltv_calc / cac,
                "é o LTV que você acabou de calcular, dividido pelo CAC.",
            ),
            checar_bool(
                "saudavel", r.get("saudavel"),
                ltv_calc > RAZAO_LTV_CAC_SAUDAVEL * cac,
                f"a regra de bolso é LTV > {RAZAO_LTV_CAC_SAUDAVEL:.0f}×CAC "
                "— sem `if`, a comparação já devolve o bool.",
            ),
        ]

    if etapa == "exercicio-3":
        razao = faturamento / faturamento_base
        cagr_pct = (razao ** (1 / anos_serie) - 1) * 100
        total_pct = (razao - 1) * 100
        return [
            checar_numero(
                "anos_da_serie", r.get("anos_da_serie"), anos_serie,
                f"de {d['MEU_ANO_BASE']} a {d['MEU_ANO']}: conte os "
                "INTERVALOS entre os anos, não os anos.",
                tolerancia=0,
            ),
            checar_numero(
                "crescimento_total_pct", r.get("crescimento_total_pct"),
                total_pct,
                "é a variação do período: (final / inicial − 1) × 100. "
                "Pode ser negativa — negócio jovem também encolhe.",
            ),
            checar_numero(
                "cagr_pct", r.get("cagr_pct"), cagr_pct,
                "o expoente é FRACIONÁRIO: (final/inicial) ** (1/anos) − 1, "
                "tudo isso × 100. Cuidado com os parênteses do expoente.",
            ),
            checar_numero(
                "media_ingenua_pct", r.get("media_ingenua_pct"),
                total_pct / anos_serie,
                "é o crescimento total dividido pelo número de anos — a "
                "média que a gente quer justamente mostrar que é errada.",
            ),
            checar_bool(
                "projecao_otimista", r.get("projecao_otimista"),
                d["MEU_CRESCIMENTO"] > cagr_pct,
                "compare MEU_CRESCIMENTO (a projeção do seu plano) com o "
                "CAGR que o negócio de fato entregou até aqui.",
            ),
        ]

    if etapa == "exercicio-4":
        return [
            checar_igual(
                "prefixo", r.get("prefixo"), codigo[:3],
                f"MEU_CODIGO_PEDIDO é {codigo!r} — os 3 primeiros "
                "caracteres, com fatiamento [:3].",
            ),
            checar_numero(
                "ano_pedido", r.get("ano_pedido"), int(codigo[4:8]),
                "posições 4 a 8 (fatiamento [4:8]), convertidas para "
                "inteiro com int().", tolerancia=0,
            ),
            checar_igual(
                "uf_pedido", r.get("uf_pedido"), codigo[9:11],
                "posições 9 a 11 (fatiamento [9:11]).",
            ),
            checar_igual(
                "sequencial_pedido", r.get("sequencial_pedido"), codigo[12:17],
                "posições 12 a 17 (fatiamento [12:17]) — mantenha como "
                "texto, não converta para número.",
            ),
            checar_igual(
                "canal_pedido", r.get("canal_pedido"), codigo[-1],
                "o ÚLTIMO caractere — use índice negativo [-1], sem "
                "precisar saber o tamanho do texto.",
            ),
            checar_bool(
                "veio_do_app", r.get("veio_do_app"),
                codigo[-1] == "A",
                "compare o canal_pedido com \"A\" — sem if, a comparação "
                "já devolve o bool.",
            ),
        ]

    if etapa == "exercicio-5":
        projetado = faturamento * (1 + d["MEU_CRESCIMENTO"] / 100) ** horizonte
        return [
            checar_numero(
                "horizonte", r.get("horizonte"), horizonte,
                f"de {d['MEU_ANO']} a {META_ANO} são quantos períodos de "
                "crescimento? Mesmo raciocínio do CAGR do Exercício 3.",
                tolerancia=0,
            ),
            checar_numero(
                "faturamento_projetado", r.get("faturamento_projetado"),
                projetado,
                "confira os parênteses: (1 + g/100) elevado ao horizonte, "
                "tudo multiplicando MEU_FATURAMENTO. Releia a Parte 1.",
            ),
            checar_numero(
                "percentual_da_meta", r.get("percentual_da_meta"),
                projetado / meta * 100,
                "é a projeção sobre a MINHA_META, vezes 100.",
            ),
            checar_igual(
                "parecer", r.get("parecer"), parecer_meta(projetado, meta),
                "compare a sua projeção com MINHA_META e com 90% dela.",
            ),
        ]

    return [(False, f"❓ etapa desconhecida: {etapa!r}")]


# ---------------------------------------------------------------- montagem
_KIT = core.Kit(
    atividade=ATIVIDADE,
    titulo="Atividade 01 — O Raio-X do Seu Negócio",
    versao=VERSAO,
    gerar_dados=_gerar,
    apresentar=_apresentar,
    checagens=_checagens,
)

iniciar = _KIT.iniciar
prever = _KIT.prever
registrar = _KIT.registrar
conferir = _KIT.conferir
diario = _KIT.diario
limpar_diario = _KIT.limpar_diario
assinatura = _KIT.assinatura
dados_de = _KIT.dados_de


def distribuicao(matriculas):
    """Mostra o negócio e os indicadores de cada matrícula da turma.

    Ferramenta **do professor**, não do aluno::

        from scripts.kit_a01 import distribuicao
        distribuicao(["20261234500", "20261234501", "20261234502"])

    ⚠️ Nunca versione a lista de matrículas: é dado pessoal do aluno e este
    repositório é público.
    """
    return _KIT.distribuicao(
        matriculas,
        colunas=[
            ("negócio", "MEU_NEGOCIO", "<18"),
            ("categoria", "MINHA_CATEGORIA", "<12"),
            ("faturamento", "MEU_FATURAMENTO", ">12.2f"),
            ("ticket", "MEU_TICKET_MEDIO", ">9.2f"),
            ("CAC", "MEU_CAC", ">9.2f"),
            ("churn", "MINHA_CHURN", ">7.2f"),
            ("ano", "MEU_ANO", ">5"),
        ],
    )
