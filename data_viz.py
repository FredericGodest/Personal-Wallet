import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

dict_df = Getdata()

def SunBursts(df)-> object:
    fig1 = px.sunburst(df, path=["Type", "Titre"],
                      values="Percent",
                      title='Répartition des valorisations en %',
                      height=800, width=800)

    fig2 = px.sunburst(df, path=["Type", "Titre"],
                      values="Dividende/an",
                      title=f'Répartition des dividende s perçus en €. (Dividendes annuels = {Dividendes}€)',
                      height=800, width=800)

    return fig1, fig2


def Benefice_Evolution(df)-> object:
    max_val = int(df["Total valorisé"][df["Total valorisé"] != 0][-1])

    fig = px.area(df, x=df.index, y=["Total investi", "Différence valorisé/investi"],
                  title='Evolution des bénéfices en fonction du temps')
    fig.update_layout(title=f"Evolution du patrimoine en fonction du temps. (Total valorisé = {max_val}€)",
                      xaxis_title='Temps',
                      yaxis_title='Euros')

    return fig

def Epargne_Evolution(df)-> object:
    epargne = int(df["Epargné ce mois ci"].mean())

    fig = px.bar(df, x=df.index, y=["Epargné ce mois ci"])
    fig.update_layout(title=f"Evolution de l'épargne mensuelle en fonction du temps. (moyenne = {epargne}€)",
                      xaxis_title='Temps',
                      yaxis_title='Euros')

    return fig

def Patrimoine_Evolution(df)-> object:
    track_list = ["Comptes courants",
                  "Comptes sur livret",
                  "PEL",
                  "Assurance vie (placement)",
                  "Assurance vie (fond euros)",
                  "PEA Valorisé",
                  "CTO Valorisé"]

    fig = px.area(df, x=df.index, y=track_list)
    fig.update_layout(title_text="Evolution du patrimoine sur tout support confondus",
                      xaxis_title="Temps",
                      yaxis_title="Euros")

    return fig

def Waterfall_Perso(df)-> object:
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
        y=y
    ))
    fig.update_layout(title_text=f"Waterfall des cash flow. (Reste à vivre = {reste}€)",
                      yaxis_title="Euros")

    return fig

def Pie_Charge(df)-> object:
    charge = df[df["Type"] == "Charges"]
    fig = px.pie(charge, values='Final Abs', names='Description',
                 title='Répartitions des charges mensuelles',
                 height=800, width=800)

    return fig