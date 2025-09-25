import warnings
import pandas as pd
# IMPORTS/CONFIGURATIONS
# Bibliotecas para manipulação de dados
# Biblioteca de avisos
# Configurações de exibição do pandas
warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:,.2f}'.format
pd.options.display.max_rows = None
pd.options.display.max_colwidth = None


def hex_to_rgba_str(hex_color, alpha=1.0):
    from matplotlib.colors import to_rgba
    r, g, b, a = to_rgba(hex_color, alpha)
    return f"rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {a})"


def card_chart(nome, subtexto, valor, icone_url, nome_cor='gray', subtexto_cor='gray', num_color="#1D4ED8", bg_color="light gray", width=250, height=120):
    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode="number",
        value=valor,
        title={"text": ""},
        number={
            "prefix": "R$ ",
            # "valueformat": ",.2f",
            "font": {
                "color": num_color,
                'size': 20
            }
        }
    ))

    # Adiciona o ícone
    fig.add_layout_image(
        dict(
            source=icone_url,
            xref="paper", yref="paper",
            x=0.425,
            y=1.1,
            sizex=0.4,
            sizey=0.4,
            xanchor="left", yanchor="top",
            layer="above"
        )
    )

    # Nome do indicador e subtexto
    fig.add_annotation(
        text=f"<span style='color:{nome_cor}'><b>{nome}</b></span><br><span style='color:{subtexto_cor};font-size:0.7em'>{subtexto}</span>",
        x=0.5,
        y=-0.1,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="center"
    )

    fig.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=height,
        width=width,
        margin=dict(t=20, b=20, l=10, r=10),
        font=dict(family="Arial", color="#1D4ED8"),
        title=dict(
            text="",
            x=0.5,
            xanchor="center"
        )
    )

    return fig


def financial_transaction_chart(saldo_inicial, entradas, saidas, saldo_final):
    import plotly.graph_objects as go

    fig = go.Figure(go.Waterfall(
        name="Fluxo de Caixa",
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Saldo Inicial", "Entradas", "Saídas", "Saldo Final"],
        textposition="outside",
        text=[
            f"R$ {saldo_inicial:,.2f}", f"+R$ {entradas:,.2f}",
            f"-R$ {saidas:,.2f}", f"R$ {saldo_final:,.2f}"],
        y=[saldo_inicial, entradas, saidas, 0],
        connector={"line": {"color": "#f0aa40", "width": 2}},
        increasing={"marker": {"color": hex_to_rgba_str("#57CEA7", 0.75),
                    'line': {
                        'color': hex_to_rgba_str("#57CEA7", 1),
                        'width': 2}}},
        decreasing={"marker": {"color": hex_to_rgba_str("#e74c3c", 0.75),
                    'line': {
                        'color': hex_to_rgba_str("#e74c3c", 1),
                        'width': 2}}},
        totals={"marker": {"color": hex_to_rgba_str("#75A7F9", 0.75),
                'line': {
                    'color': hex_to_rgba_str("#75A7F9", 1),
                    'width': 2}}},
        width=0.5
    ))

    max_y = saldo_inicial+entradas  # 'valores' é sua lista/array de valores das barras
    fig.update_yaxes(range=[0, max_y * 1.15])  # 10% de espaço extra no topo

    fig.update_layout(
        template="plotly_white",
        title=dict(
            text="<b>Resumo da Movimentação Financeira</b>",
            x=0.5,
            font=dict(family="Arial", color="#1D4ED8")
        ),
        yaxis=dict(
            title=None,
            showticklabels=False,
            # showgrid=False,
            # zeroline=False
        ),
        xaxis=dict(
            # showgrid=False,
            # zeroline=False
        ),
        font=dict(family="Arial", color="gray"),
        margin=dict(l=0, r=0, t=50, b=20, pad=0),
        height=400,
        width=1200,
    )

    return fig


def donut_chart(labels, values, title="", pull=0.05, colors=None, width=500, height=400, margin=None, bg_color="#f5f6fa"):
    """
    Cria um gráfico de rosca (donut) estilizado com Plotly.

    Parâmetros:
        labels (list): Lista de rótulos das fatias.
        values (list): Lista de valores correspondentes às fatias.
        title (str): Título do gráfico.
        colors (list): Lista de cores para as fatias (opcional).
        hole (float): Tamanho do buraco central (0 a 1).
        width (int): Largura do gráfico.
        height (int): Altura do gráfico.
        bg_color (str): Cor de fundo do gráfico.

    Retorna:
        plotly.graph_objects.Figure: Figura do gráfico de rosca.
    """
    import plotly.graph_objects as go

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.7,
        pull=pull,
        textinfo="percent+label+value",
        texttemplate="<b>%{label}</b><br>%{percent}",
        insidetextorientation="radial",
        marker=dict(colors=colors),
        sort=True,
    ))

    # # Valor total centralizado, destacado
    # fig.add_annotation(
    #     text=f"<span style='font-size:1.2em'><b>Total</b></span><br><span style='font-size:1.5em'><b>R$ {sum(values):,.2f}</b></span>",
    #     x=0.5, y=0.5,
    #     font=dict(size=10, family="Arial"),
    #     showarrow=False
    # )

    fig.update_layout(
        template='plotly_white',
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            y=0.95,
            font=dict(family="Arial", color="#1D4ED8")
        ),
        showlegend=False,
        font=dict(family="Arial", color="gray"),
        width=width,
        height=height,
        margin=margin
    )

    return fig


def v_bar_chart(
    x,
    y,
    title="",
    textposition='outside',
    color=None,
    width=600,
    height=500,
    show_values=True,
    values_fmt=",.2f",
    margin=dict(l=20, r=20, t=50, b=20),
):
    """
    Cria um gráfico de barras (vertical ou horizontal) estilizado com Plotly.

    Parâmetros:
        x (list): Rótulos do eixo x (ou y, se horizontal).
        y (list): Valores das barras.
        title (str): Título do gráfico.
        color (str): Cor das barras.
        bar_width (float): Largura das barras (0 a 1).
        bg_color (str): Cor de fundo do gráfico.
        width (int): Largura do gráfico.
        height (int): Altura do gráfico.
        show_values (bool): Exibir valores nas barras.
        values_fmt (str): Formato dos valores exibidos.

    Retorna:
        plotly.graph_objects.Figure: Figura do gráfico de barras.
    """
    import plotly.graph_objects as go
    import plotly

    if color == 'labels':
        num_labels = len(x)
        color = plotly.colors.qualitative.Plotly * \
            (num_labels // len(plotly.colors.qualitative.Plotly) + 1)
        color = color[:num_labels]
    else:
        pass

    bar = go.Bar(
        x=x,
        y=y,
        marker_color=color,
        text=[f"R${v:{values_fmt}}" for v in y] if show_values else None,
        textposition=textposition
    )

    fig = go.Figure(bar)

    max_y = y.max()  # 'valores' é sua lista/array de valores das barras
    fig.update_yaxes(range=[0, max_y * 1.1])  # 10% de espaço extra no topo

    fig.update_layout(
        template='plotly_white',
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            y=0.95,
            font=dict(family="Arial", color="#1D4ED8")),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        font=dict(family="Arial", color="gray"),
        width=width,
        height=height,
        margin=margin,
    )

    return fig


def h_bar_chart(
    y,
    x,
    title="",
    textposition='auto',
    color="#4a90e2",
    bg_color="#f5f6fa",
    width=500,
    height=400,
    show_values=True,
    values_fmt=",.2f",
    margin=dict(l=20, r=20, t=50, b=20),
):
    """
    Cria um gráfico de barras horizontal estilizado com Plotly.

    Parâmetros:
        y (list): Rótulos do eixo y.
        x (list): Valores das barras.
        title (str): Título do gráfico.
        color (str): Cor das barras.
        bg_color (str): Cor de fundo do gráfico.
        width (int): Largura do gráfico.
        height (int): Altura do gráfico.
        show_values (bool): Exibir valores nas barras.
        values_fmt (str): Formato dos valores exibidos.

    Retorna:
        plotly.graph_objects.Figure: Figura do gráfico de barras horizontal.
    """
    import plotly.graph_objects as go
    import plotly

    if color == 'labels':
        num_labels = len(x)
        color = plotly.colors.qualitative.Plotly * \
            (num_labels // len(plotly.colors.qualitative.Plotly) + 1)
        color = color[:num_labels]
    else:
        pass

    bar = go.Bar(
        y=y,
        x=x,
        orientation="h",
        marker_color=color,
        text=[f"R${v:{values_fmt}}" for v in x] if show_values else None,
        textposition=textposition
    )

    fig = go.Figure(bar)

    fig.update_layout(
        template='plotly_white',
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            y=0.95,
            font=dict(family="Arial", color="#1D4ED8")),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False),
        yaxis=dict(
            showgrid=False,
            zeroline=False),
        font=dict(family="Arial", color="gray"),
        width=width,
        height=height,
        margin=margin,
    )

    return fig


def comparison_card_chart(title, name1, value1, name2, value2, length=1):
    import plotly.graph_objects as go

    dif_values = value1 - value2
    if dif_values >= -0.5 or dif_values <= 0.5:
        color = '#047857'
        paper_bgcolor = "#EFF6FF"
    else:
        paper_bgcolor = "#FFEFF7"
        color = '#e74c3c'

    fig = go.Figure()

    fig.add_annotation(
        text=f'{name1}:',
        font=dict(
            family="Arial",
            size=10),
        xref="paper", yref="paper",
        x=0.1, y=0.7,  # Ajuste esses valores para posicionar ao lado do número
        showarrow=False)

    fig.add_trace(go.Indicator(
        mode="number",
        value=value1,
        number=dict(
            valueformat=',.2f',
            prefix="R$ ",
            font=dict(
                family="Arial",
                size=10)),
        # align='right',
        domain={'x': [0.8, 0.9], 'y': [0.59, 0.7]}
    ))

    fig.add_annotation(
        text=f'{name2}:',
        font=dict(
            family="Arial",
            size=10),
        xref="paper", yref="paper",
        x=0.1, y=0.45,  # Ajuste esses valores para posicionar ao lado do número
        showarrow=False)

    fig.add_trace(go.Indicator(
        mode="number",
        value=value2,
        number=dict(
            valueformat=',.2f',
            prefix="R$ ",
            font=dict(
                family="Arial",
                size=10)),
        # align='right',
        domain={'x': [0.8, 0.9], 'y': [0.39, 0.5]}
    ))

    fig.add_annotation(
        text='<b>Diferença:</b>',
        font=dict(
            family="Arial",
            size=10,
            color=color),
        xref="paper", yref="paper",
        x=0.1, y=0.15,  # Ajuste esses valores para posicionar ao lado do número
        showarrow=False)

    fig.add_trace(go.Indicator(
        mode="number",
        value=dif_values,
        number=dict(
            valueformat=',.2f',
            prefix="R$ ",
            font=dict(
                family="Arial",
                size=10,
                color=color),
        ),
        # align='right',
        domain={'x': [0.8, 0.9], 'y': [0.02, 0.4]}
    ))

    fig.update_layout(
        title=dict(
            text=f'<b>{title}</b>',
            font=dict(
                family="Arial",
                size=12,
                color="#1D4ED8"),
            y=0.9, x=0.1),
        paper_bgcolor=paper_bgcolor,
        grid={'rows': 2, 'columns': 1, 'pattern': "independent"},
        shapes=[
            dict(
                type="line",
                x0=0, y0=0, x1=0, y1=1,
                line=dict(
                    color="#1D4ED8",
                    width=8,
                ),
            )
        ],
        margin=dict(t=0, b=0, l=0, r=20),
        height=120,
        width=1200/length,
    )

    return fig


def table_chart(
        data,
        cell_format=[None, ',.2f'],
        cell_align=['left', 'right'],
        cell_fill_color=['#EFF6FF', '#F9FAFB', 'white'],
        columnwidth=None,
        cellheight=None,
        font_size=12,
        width=600,
        height=300):

    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[f'<b>{v}</b>' for v in data.columns],
            fill_color='rgba(224, 231, 255, 1)',
            font=dict(
                color='rgba(30, 64, 175, 1)',
                size=font_size+2,
                family='Segoe UI, Arial'),
            align='center',
            line_color='rgba(0,0,0,0.05)',
            line_width=4,
            height=cellheight
        ),
        cells=dict(
            values=[data[f'{column}'] for column in data.columns],
            format=cell_format,
            font=dict(
                color='#374151',
                size=font_size,
                family='Segoe UI, Arial'),
            align=cell_align,
            fill_color=[cell_fill_color],
            line_color='white',
            line_width=4,
            height=cellheight
        ),
        columnwidth=columnwidth,
    )])

    fig.update_layout(
        width=width,
        height=height,
        margin=dict(l=1, r=1, t=1, b=1),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig


def indicator_chart(tittle, subtittle, value, delta_reference, color_up=True):
    import plotly.graph_objects as go

    if color_up:
        increasing_color = {'color': "#27ae60"}
        increasing_bar_color = "#ffe6e6"
        decreasing_color = {'color': "#e74c3c"}
        decreasing_bar_color = "#E0FDF2"
    else:
        increasing_color = {'color': "#e74c3c"}
        increasing_bar_color = "#E0FDF2"
        decreasing_color = {'color': "#27ae60"}
        decreasing_bar_color = "#ffe6e6"

    fig = go.Figure(go.Indicator(
        title={"text": f"<span style='color:#1D4ED8'><b>{tittle}</b></span><br><span style='font-size:0.8em'>{subtittle}</span>"},
        mode="number+delta+gauge",
        value=value,
        number={
            'suffix': "%",
            'font': {"size": 46, "color": "#4a90e2", "family": "Arial"}
        },
        delta={
            'reference': delta_reference,
            'increasing': increasing_color,
            'decreasing': decreasing_color},
        gauge={
            'shape': 'angular',
            'axis': {
                'range': [0, 100],
                'tickmode': 'linear',
                'dtick': 10,
                # 'bar':{'color':'darkblue'}
            },
            "bar": {"color": "#4a90e2", "thickness": 0.3},
            'steps': [
                {'range': [0, delta_reference], 'color': increasing_bar_color},
                {'range': [delta_reference, 100],
                    'color': decreasing_bar_color}
            ],
            'threshold': {
                'line': {'color': "#e74c3c", 'width': 2},
                'thickness': 1,
                'value': delta_reference
            },
            "borderwidth": 0,  # Remove o contorno
            # Garante que a cor do contorno é transparente
            "bordercolor": "rgba(0,0,0,0)"
        },
    ))

    fig.update_layout(
        paper_bgcolor="white",
        height=250,
        width=400,
        margin=dict(l=40, r=40, t=90, b=20),
        font={'family': "Arial", 'size': 18, 'color': 'gray'}
    )
    return fig
