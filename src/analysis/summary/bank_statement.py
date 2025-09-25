import calendar

import pandas as pd


def bank_statement_movement_summary(
    bank_statement_data: pd.DataFrame, moviment: str
) -> pd.Series:
    """
    Gera um resumo das entradas (créditos) no extrato bancário,
    agrupando por histórico e calculando o total.

    Parâmetros:
        bank_statement_data (pd.DataFrame): DataFrame do extrato bancário,
            contendo pelo menos as colunas 'INF', 'HIST' e 'VALOR'.

    Retorna:
        pd.DataFrame: Dataframe com o valor total por histórico bancário e um campo 'TOTAL'
                   com a soma geral.
    """
    moviment = moviment.upper()
    if moviment == "C":
        bank_history_exclude = "Resgate Automático"
        ascending = False
    else:
        bank_history_exclude = "BB-APLIC C.PRZ-APL.AUT"
        ascending = True
    # Filtra apenas créditos, excluindo 'Resgate Automático'
    credits = bank_statement_data[
        (bank_statement_data["INF"] == moviment)
        & (bank_statement_data["HIST"] != bank_history_exclude)
    ]

    # Agrupa por histórico e soma os valores
    grouped_credits = credits.groupby("HIST")["VALOR"].sum()

    # Transforma em dataframe
    grouped_credits = grouped_credits.to_frame().reset_index()

    # Renomeia colunas
    grouped_credits.columns = ["HISTÓRICO_BANCÁRIO", "VALOR_ACUMULADO"]

    # Ordena valores do maior para o menor
    grouped_credits = grouped_credits.sort_values(
        by="VALOR_ACUMULADO", ascending=ascending
    )

    # Adiciona o total geral
    grouped_credits.loc["TOTAL", "VALOR_ACUMULADO"] = grouped_credits[
        "VALOR_ACUMULADO"
    ].sum()

    return grouped_credits


def banks_statement_summary(
    bank_statement_data: pd.DataFrame, year: int, month: int = 12
) -> pd.Series:
    """
    Gera um resumo detalhado do extrato bancário para um período específico.

    Parâmetros:
        bank_statement_data (pd.DataFrame): DataFrame contendo o extrato bancário,
            com colunas obrigatórias: 'INF', 'HIST', 'VALOR', 'VALOR_APP', 'SALDO'.
        year (int): Ano de referência.
        month (int, opcional): Mês final do período (1-12). Padrão: 12.

    Retorna:
        pd.Series: Série com totais e subtotais organizados por categorias.
    """
    # --- FILTRO POR PERÍODO ---
    last_day = calendar.monthrange(year, month)[1]
    bank_statement_data = bank_statement_data.loc[
        bank_statement_data.index <= f"{year}-{month:02d}-{last_day}"
    ]

    # --- SALDO INICIAL ---
    saldo_inicial = bank_statement_data["SALDO"].iloc[0]

    # --- ENTRADAS ---
    total_aplicado = bank_statement_data.loc[
        bank_statement_data["HIST"] == "BB-APLIC C.PRZ-APL.AUT", "VALOR_APP"
    ].sum()

    total_resgatado = bank_statement_data.loc[
        bank_statement_data["HIST"] == "Resgate Automático", "VALOR_APP"
    ].sum()

    rendimentos = (
        bank_statement_data.loc[bank_statement_data["HIST"] == "RENDIMENTOS", "VALOR"]
        .sum()
        .round(2)
    )

    total_entradas = (
        bank_statement_data.loc[bank_statement_data["INF"] == "C", "VALOR"]
        .sum()
        .round(2)
    )

    repasses_fnde = (
        bank_statement_data.loc[
            bank_statement_data["HIST"].isin(
                [
                    "IPVA",
                    "IPI/EXPORTACAO",
                    "FPE/FPM",
                    "RECEBIMENTO DE ICMS",
                    "ITR",
                    "ITCMD",
                ]
            ),
            "VALOR",
        ]
        .sum()
        .round(2)
    )

    repasses_uniao_vaaf = (
        bank_statement_data.loc[
            bank_statement_data["HIST"] == "VAAF Complemento FUNDEB", "VALOR"
        ]
        .sum()
        .round(2)
    )

    repasses_uniao_vaat = (
        bank_statement_data.loc[
            bank_statement_data["HIST"] == "VAAT Complemento FUNDEB", "VALOR"
        ]
        .sum()
        .round(2)
    )

    repasses_uniao_vaar = (
        bank_statement_data.loc[
            bank_statement_data["HIST"] == "VAAR Complemento FUNDEB", "VALOR"
        ]
        .sum()
        .round(2)
    )

    ajuste_repasses_uniao_vaar = (
        bank_statement_data.loc[
            bank_statement_data["HIST"] == "Ajuste Complemento VAAR", "VALOR"
        ]
        .sum()
        .round(2)
    )

    # --- OUTRAS ENTRADAS ---
    ordens_canceladas = (
        bank_statement_data.loc[
            bank_statement_data["HIST"] == "ORDEM BANC CANCELADA", "VALOR"
        ]
        .sum()
        .round(2)
    )

    transferencias_recebidas = (
        bank_statement_data.loc[
            bank_statement_data["HIST"].isin(
                [
                    "Devolução",
                    "Dep Cheque BB Liquidado",
                    "Transferência recebida",
                    "TED Devolvida",
                    "TED-Crédito em Conta",
                    "Transferido da poupança",
                ]
            ),
            "VALOR",
        ]
        .sum()
        .round(2)
    )

    outras_entradas = (
        bank_statement_data.loc[
            bank_statement_data["HIST"] == "COTA DAF-DEBITO", "VALOR"
        ]
        .sum()
        .round(2)
    )

    # --- SAÍDAS ---
    total_saidas = (
        bank_statement_data.loc[bank_statement_data["INF"] == "D", "VALOR"]
        .sum()
        .round(2)
    )

    despesas = (
        bank_statement_data.loc[
            bank_statement_data["HIST"].isin(
                [
                    "TED Transf.Eletr.Disponiv",
                    "Folha de Pagamento",
                    "Pagamentos Diversos",
                    "Emissão Ordem Bancária",
                    "Impostos",
                    "Tar Lib/Ant Float Pg Div",
                    "Tarif ORBAN-Crédito Conta",
                    "Pagto via Auto-Atend.BB",
                ]
            ),
            "VALOR",
        ]
        .sum()
        .round(2)
    )

    outras_saidas = outras_entradas

    # --- SALDO FINAL ---
    saldo_final = saldo_inicial + total_entradas + total_saidas

    # --- DICIONÁRIO DE RESUMO ---
    summary = {
        "1. SALDO INICIAL": saldo_inicial,
        "": "",
        "2. TOTAL DE ENTRADAS": total_entradas,
        "   2.1. ENTRADAS CORRENTES": total_entradas
        - (
            ordens_canceladas
            + transferencias_recebidas
            - outras_entradas
            - ajuste_repasses_uniao_vaar
        ),
        "       2.1.1. TOTAL DE REPASSES": repasses_fnde
        + repasses_uniao_vaaf
        + repasses_uniao_vaat
        + repasses_uniao_vaar
        + outras_entradas
        + ajuste_repasses_uniao_vaar,
        "           2.1.1.1. FUNDEB - Impostos e Transferências de Impostos (FNDE)": repasses_fnde
        + outras_entradas,
        "               2.1.1.1.1. PRINCIPAL": repasses_fnde,
        "               2.1.1.1.2. Ajustes (COTA DAF)": outras_entradas,
        "           2.1.1.2. COMPLEMENTAÇÃO DA UNIÃO": repasses_uniao_vaaf
        + repasses_uniao_vaat
        + repasses_uniao_vaar
        + ajuste_repasses_uniao_vaar,
        "               2.1.1.2.1. VAAF": repasses_uniao_vaaf,
        "               2.1.1.2.2. VAAT": repasses_uniao_vaat,
        "               2.1.1.2.3. VAAR": repasses_uniao_vaar,
        "               2.1.1.2.4. Ajustes de complementação da União": ajuste_repasses_uniao_vaar,
        "       2.1.2. RENDIMENTOS DE APLICAÇÕES FINANCEIRAS": rendimentos,
        "   2.2. OUTRAS ENTRADAS": ordens_canceladas
        + transferencias_recebidas
        - outras_entradas
        - ajuste_repasses_uniao_vaar,
        "       2.2.1. ORDENS CANCELADAS (ENTRADAS)": ordens_canceladas,
        "       2.2.2. TRANSFERÊNCIAS RECEBIDAS (ENTRADAS)": transferencias_recebidas,
        "       2.2.3. Ajustes (COTA DAF)": -outras_entradas,
        "       2.2.4. Ajustes de complementação da União": -ajuste_repasses_uniao_vaar,
        " ": "",
        "3. TOTAL DE SAÍDAS": total_saidas,
        "   3.1. DESPESAS CANCELADAS/ANULADAS": -(
            ordens_canceladas + transferencias_recebidas
        ),
        "   3.2. Ajustes (COTA DAF)": outras_saidas,
        "   3.3. Ajustes de complementação da União": ajuste_repasses_uniao_vaar,
        "   3.4. DESPESAS EFETIVAMENTE PAGAS": -(
            -total_saidas
            - (ordens_canceladas + transferencias_recebidas)
            + outras_saidas
            + ajuste_repasses_uniao_vaar
        ),
        "  ": "",
        "4. SALDO FINAL": saldo_final,
        "   ": "",
        "5. TOTAL APLICADO": total_aplicado,
        "6. TOTAL RESGATADO": total_resgatado,
    }

    return pd.Series(summary, name="TOTAIS")
