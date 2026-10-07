"""Validação do kit_a01: sem colisões na turma, checagens batem com o gerador.

Não é um pacote de testes formal (o repositório não usa framework de
terceiros) — é um script de verificação, no mesmo espírito do
`distribuicao()`. Rode com::

    python3 -m scripts.test_kit_a01
"""

from . import core
from .kit_a01 import _checagens, dados_de, ltv, parecer_meta, RAZAO_LTV_CAC_SAUDAVEL, META_ANO


def test_sem_colisoes():
    matriculas = [str(20261234500 + i) for i in range(core.TURMA_MAX)]
    vistos = {}
    for m in matriculas:
        d = dados_de(m)
        vistos.setdefault(d["MEU_NEGOCIO"], []).append(m)
    repetidos = {k: v for k, v in vistos.items() if len(v) > 1}
    assert not repetidos, f"negócios repetidos na turma simulada: {repetidos}"
    print(f"✅ sem colisões em {len(matriculas)} matrículas simuladas "
          f"({len(vistos)} negócios distintos)")


def test_checagens_batem_com_gerador():
    d = dados_de("20261234567")

    # Exercício 1
    receita_anual = d["MEU_FATURAMENTO"] * 12
    alto_ticket = d["MEU_TICKET_MEDIO"] > 300.0
    ficha = (
        f"{d['MEU_NEGOCIO']} ({d['MINHA_UF']}) | {d['MINHA_CATEGORIA']} | "
        f"ticket R$ {d['MEU_TICKET_MEDIO']:.2f}"
    )
    resultados = _checagens("exercicio-1", dict(
        receita_anual=receita_anual, alto_ticket=alto_ticket, ficha=ficha,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 2
    ltv_val = ltv(d["MEU_TICKET_MEDIO"], d["MINHA_CHURN"])
    resultados = _checagens("exercicio-2", dict(
        ltv=ltv_val,
        razao_ltv_cac=ltv_val / d["MEU_CAC"],
        saudavel=ltv_val > RAZAO_LTV_CAC_SAUDAVEL * d["MEU_CAC"],
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 3
    anos = d["MEU_ANO"] - d["MEU_ANO_BASE"]
    razao = d["MEU_FATURAMENTO"] / d["MEU_FATURAMENTO_BASE"]
    cagr_pct = (razao ** (1 / anos) - 1) * 100
    total_pct = (razao - 1) * 100
    resultados = _checagens("exercicio-3", dict(
        anos_da_serie=anos,
        crescimento_total_pct=total_pct,
        cagr_pct=cagr_pct,
        media_ingenua_pct=total_pct / anos,
        projecao_otimista=d["MEU_CRESCIMENTO"] > cagr_pct,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 4
    codigo = d["MEU_CODIGO_PEDIDO"]
    resultados = _checagens("exercicio-4", dict(
        prefixo=codigo[:3],
        ano_pedido=int(codigo[4:8]),
        uf_pedido=codigo[9:11],
        sequencial_pedido=codigo[12:17],
        canal_pedido=codigo[-1],
        veio_do_app=codigo[-1] == "A",
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 5
    horizonte = META_ANO - d["MEU_ANO"]
    projetado = d["MEU_FATURAMENTO"] * (1 + d["MEU_CRESCIMENTO"] / 100) ** horizonte
    resultados = _checagens("exercicio-5", dict(
        horizonte=horizonte,
        faturamento_projetado=projetado,
        percentual_da_meta=projetado / d["MINHA_META"] * 100,
        parecer=parecer_meta(projetado, d["MINHA_META"]),
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    print("✅ todas as checagens (exercícios 1–5) batem com o gerador para "
          "a matrícula de teste")


if __name__ == "__main__":
    test_sem_colisoes()
    test_checagens_batem_com_gerador()
    print("OK")
