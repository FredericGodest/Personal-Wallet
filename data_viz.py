"""
This is the module for plotly figures creation.
"""

# IMPORTS
import plotly.graph_objects as go
import plotly.express as px

# CONSTANTS
HEIGHT = 800
WIDTH = 800

def SunBursts(df)-> object:
    """
    This function is creating two different sunbursts from a given dataframe.

    :param df: pandas dataframe
    :return fig1, fig2: Two plotly sunbursts figures
    """
    dividendes = int(df["Dividende/an"].sum())
    total_valorisation = int(df["Valorisation"].sum())

    fig1 = px.sunburst(df, path=["Type", "Titre"],
                      values="Percent",
                      title=f'Répartition des valorisations en % (total = {total_valorisation}€)',
                      height=HEIGHT, width=WIDTH)
    fig1.update_traces(textinfo='label+percent entry')
    fig1.update_layout(title_x=0.5)

    fig2 = px.sunburst(df, path=["Type", "Titre"],
                      values="Dividende/an",
                      title=f'Répartition des dividendes perçus en € (Dividendes annuels = {dividendes}€)',
                      height=HEIGHT, width=WIDTH)
    fig2.update_traces(textinfo='label+value')
    fig2.update_layout(title_x=0.5)

    return fig1, fig2


def Benefice_Evolution(df)-> object:
    """
    This function is creating an area plot of the benefit based on a given dataframe.

    :param df: pandas dataframe.
    :return fig: plotly area figure
    """
    max_val = int(df["Total valorisé"][df["Total valorisé"] != 0][-1])

    fig = px.area(df, x=df.index, y=["Total investi", "Différence valorisé/investi"],
                  title='Evolution des bénéfices en fonction du temps',
                  height=HEIGHT/2, width=WIDTH)
    fig.update_layout(title=f"Evolution du patrimoine en fonction du temps (Total valorisé = {max_val}€)",
                      yaxis_title='Euros',
                      xaxis_title="Temps",
                      title_x=0.5)
    return fig

def Epargne_Evolution(df)-> object:
    """
    This function is creating an bar plot of the saving based on a given dataframe.

    :param df: pandas dataframe.
    :return fig: plotly bar figure
    """

    df["MA"] = df["Epargné ce mois ci"].rolling(window=4).mean()
    s = df["Epargné ce mois ci"]
    delta_epargne = int(s[s < 2500].std())
    epargne = int(s[s < 2500].mean())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Epargné ce mois ci"],
        name='Epargne réelle',
        marker_color='blue'
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["MA"],
        name='Moyenne mobile',
        marker_color='lightsalmon'
    ))

    fig.update_layout(title=f"Evolution de l'épargne mensuelle (moyenne = {epargne}€ [+/- {delta_epargne}€])",
                    xaxis_title='Temps',
                    yaxis_title='Euros',
                    title_x=0.5)

    return fig

def Patrimoine_Evolution(df)-> object:
    """
    This function is creating an area plot of the patrimony based on a given dataframe.

    :param df: pandas dataframe.
    :return fig: plotly area figure
    """
    track_list = ["Comptes courants",
                  "Comptes sur livret",
                  "PEL",
                  "Assurance vie (placement)",
                  "Assurance vie (fond euros)",
                  "PEA Valorisé",
                  "CTO Valorisé"]

    fig = px.area(df, x=df.index, y=track_list,
                  height=HEIGHT/2, width=WIDTH)
    fig.update_layout(title_text="Evolution du patrimoine sur tout supports confondus",
                      yaxis_title="Euros",
                      xaxis_title="Temps",
                      title_x=0.5)

    return fig

def Waterfall_Perso(df)-> object:
    """
    This function is creating an waterfall chart of the depense based on a given dataframe.

    :param df: pandas dataframe.
    :return fig: plotly waterfall figure
    """
    group = df.groupby(by=["Type"]).sum().sort_values(by="Valeur finale", ascending=False)
    measures = list(group.index)
    y = [int(group.iloc[i]["Valeur finale"]) for i in range(len(group))]
    y_label = [str(el) + "€" for el in y]
    reste = int(group["Valeur finale"].sum())

    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=measures,
        x=measures,
        textposition="outside",
        text=y_label,
        y=y,
    ))
    fig.update_layout(title_text=f"Waterfall des cash flow (Reste à vivre = {reste}€)",
                      yaxis_title="Euros",
                      height=HEIGHT*2/3, width=WIDTH,
                      title_x=0.5)

    return fig

def Pie_Charge(df)-> object:
    """
    This function is creating an pie chart of the charges based on a given dataframe.

    :param df: pandas dataframe.
    :return fig: plotly pie figure
    """
    charge = df[df["Type"] == "Charges"]
    fig = px.pie(charge, values='Final Abs', names='Description',
                 title='Répartitions des charges mensuelles',
                 height=HEIGHT, width=WIDTH)

    fig.update_layout(title_x=0.5)

    return fig