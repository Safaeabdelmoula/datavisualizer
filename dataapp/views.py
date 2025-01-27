from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Utilise le backend non interactif
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# importation du fichier CSV
def upload(request):
    error_message = None
    output = None
    file_name = request.session.get('file_name', None)
    action = request.POST.get('action')  # Récupère l'action depuis le bouton
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        try:
            df = pd.read_csv(file,delimiter=",")
            request.session['data'] = df.to_dict()
            request.session['columns'] = df.columns.tolist()
            request.session['shape'] = df.shape
            request.session['file_name'] = file.name  # Sauvegarde le nom du fichier
            return redirect('upload')
        except Exception as e:
            error_message = f"Erreur : {str(e)}"
    if 'data' in request.session:
        df = pd.DataFrame.from_dict(request.session['data'])
        if action == 'shape':
            output = f"Lignes: {df.shape[0]}, Colonnes: {df.shape[1]}"
        elif action == 'head':
            output = df.head(10).to_html(classes='table table-striped table-sm', index=False)
        elif action == 'columns':
            output = df.columns.tolist()
        elif action == 'data':
            output = df.to_html(classes='table table-striped table-sm', index=False)

    return render(request, 'upload.html', {
        'error_message': error_message,
        'output': output,
        'action': action,
        'file_name': file_name
    })

def index(request):
    data = request.session.get('data')
    line_data = None
    column_stats = None
    line_index = None
    column_name = None
    error_message = None
    column_names = []

    if data:
        df = pd.DataFrame.from_dict(data)  # Convertir les données de session en DataFrame
        column_names = df.select_dtypes(include='number').columns.tolist()

        if request.method == 'POST':
            line_index = request.POST.get('line-index')
            column_name = request.POST.get('column-name')
            action = request.POST.get('action')  # Identifier l'action (données ou stats)

            # Gestion de l'index de ligne
            if line_index:
                try:
                    line_index = int(line_index)
                    if 0 <= line_index < len(df):
                        line_data = df.iloc[line_index].to_dict()
                    else:
                        line_data = f"Index hors limites. Max : {len(df)-1}"
                except ValueError:
                    line_data = "Veuillez entrer un index valide (nombre entier)."
                except Exception as e:
                    line_data = f"Erreur : {str(e)}"

            # Gestion des statistiques de colonne
            if column_name:
                try:
                    if column_name in df.columns:
                        if action == 'stats':  # Afficher uniquement les statistiques
                            if pd.api.types.is_numeric_dtype(df[column_name]):
                                column_stats = {
                                    'mean': df[column_name].mean(),
                                    'variance': df[column_name].var(),
                                    'std': df[column_name].std(),
                                    'min': df[column_name].min(),
                                    'max': df[column_name].max()
                                }
                            else:
                                column_stats = "Les statistiques ne peuvent être calculées que sur des colonnes numériques."
                        else:
                            column_stats = None
                    else:
                        column_stats = f"La colonne '{column_name}' n'existe pas."
                except Exception as e:
                    column_stats = f"Erreur : {str(e)}"
    else:
        error_message = "Aucune donnée disponible. Veuillez téléverser un fichier CSV."

    return render(request, 'index.html', {
        'line_data': line_data,
        'column_stats': column_stats,
        'line_index': line_index,
        'column_name': column_name,
        'column_names': column_names,
        'error_message': error_message
    })

def stats(request):
    data = request.session.get('data')
    if not data:
        return render(request, 'stats.html', {'error': 'Aucune donnée disponible. Veuillez téléverser un fichier.'})
    
    df = pd.DataFrame(data)
    stats_data = []

    for column in df.select_dtypes(include='number').columns:
        stats_data.append({
            'column': column,
            'var': df[column].var(),
            'mean': df[column].mean(),
            'std': df[column].std(),
            'min': df[column].min(),
            'max': df[column].max()

        })
    
    return render(request, 'stats.html', {'stats': stats_data})


# Étape 4 : Visualisation des données

def visualize(request):
    data = request.session.get('data', {})
    chart_type = request.GET.get('chart_type', 'hist')
    column_x = request.GET.get('column_x', None)
    column_y = request.GET.get('column_y', None)

    if not data:
        return render(request, 'visualize.html', {'error': 'Aucune donnée disponible pour la visualisation.'})

    df = pd.DataFrame.from_dict(data)
    numeric_columns = df.select_dtypes(include='number').columns.tolist()

    if not numeric_columns:
        return render(request, 'visualize.html', {'error': 'Aucune colonne numérique à afficher.'})

    buf = io.BytesIO()
    plt.figure(figsize=(12, 8))
    sns.set(style='whitegrid')

    try:
        if chart_type == 'hist' and column_x:
            sns.histplot(df[column_x], kde=True, color='skyblue')
            plt.title(f'Histogramme de {column_x}', fontsize=16)
        elif chart_type == 'box' and column_x:
            sns.boxplot(data=df[[column_x]], color='lightgreen')
            plt.title(f'Boîte à moustaches de {column_x}', fontsize=16)
        elif chart_type == 'scatter' and column_x and column_y:
            sns.scatterplot(x=df[column_x], y=df[column_y], color='coral')
            plt.title(f'Nuage de points : {column_x} vs {column_y}', fontsize=16)
        elif chart_type == 'bar' and column_x:
            df[column_x].value_counts().plot(kind='bar', color='orange')
            plt.title(f'Diagramme en barres de {column_x}', fontsize=16)
        elif chart_type == 'pairplot' and len(numeric_columns) >= 2:
            sns.pairplot(df[numeric_columns], diag_kind='kde', corner=True)
            plt.suptitle('🔗 Pairplot des Colonnes Numériques', fontsize=16)
        elif chart_type == 'heatmap' and len(numeric_columns) > 1:
            correlation_matrix = df[numeric_columns].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Matrice de Corrélation', fontsize=16)
        elif chart_type == 'violin' and column_x:
            sns.violinplot(data=df, x=column_x , color='purple')
            plt.title(f'Violin Plot de {column_x}', fontsize=16)
        else:
            plt.text(0.5, 0.5, 'Veuillez sélectionner une colonne et un type de graphique valide.',
                     horizontalalignment='center', verticalalignment='center', fontsize=12)

        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode('utf-8')
        uri = 'data:image/png;base64,' + string

    except Exception as e:
        return render(request, 'visualize.html', {'error': f'Erreur : {str(e)}'})

    return render(request, 'visualize.html', {
        'chart': uri,
        'chart_type': chart_type,
        'column_x': column_x,
        'column_y': column_y,
        'numeric_columns': numeric_columns
    })

def download_graph(request):
    # Récupérer les paramètres de l'URL
    chart_type = request.GET.get('chart_type', 'hist')
    column_x = request.GET.get('column_x', None)
    column_y = request.GET.get('column_y', None)

    # Récupérer les données depuis la session
    data = request.session.get('data', {})
    
    if not data:
        return HttpResponse("Aucune donnée disponible pour le téléchargement.")

    df = pd.DataFrame.from_dict(data)
    numeric_columns = df.select_dtypes(include='number').columns.tolist()

    if not numeric_columns:
        return HttpResponse("Aucune colonne numérique à afficher.")

    if chart_type == 'scatter' and (not column_x or not column_y):
        return HttpResponse("Les colonnes X et Y doivent être spécifiées pour un graphique de type 'scatter'.")
    
    # Préparer le graphique
    try:
        plt.figure(figsize=(10, 6))
        sns.set(style='whitegrid')

        # Génération du graphe selon le type choisi
        if chart_type == 'hist' and column_x:
            sns.histplot(df[column_x], kde=True, color='skyblue')
            plt.title(f'Histogramme de {column_x}', fontsize=16)
        elif chart_type == 'box' and column_x:
            sns.boxplot(data=df[[column_x]], color='lightgreen')
            plt.title(f'Boîte à moustaches de {column_x}', fontsize=16)
        elif chart_type == 'scatter' and column_x and column_y:
            sns.scatterplot(x=df[column_x], y=df[column_y], color='coral')
            plt.title(f'Nuage de points : {column_x} vs {column_y}', fontsize=16)
        elif chart_type == 'bar' and column_x:
            df[column_x].value_counts().plot(kind='bar', color='orange')
            plt.title(f'Diagramme en barres de {column_x}', fontsize=16)
        elif chart_type == 'pairplot' and len(numeric_columns) >= 2:
            sns.pairplot(df[numeric_columns], diag_kind='kde', corner=True)
            plt.suptitle('Pairplot des Colonnes Numériques', fontsize=16)
        elif chart_type == 'heatmap' and len(numeric_columns) > 1:
            correlation_matrix = df[numeric_columns].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Matrice de Corrélation', fontsize=16)
        elif chart_type == 'violin' and column_x:
            sns.violinplot(data=df, x=column_x, color='purple')
            plt.title(f'Violin Plot de {column_x}', fontsize=16)
        else:
            plt.text(0.5, 0.5, 'Veuillez sélectionner une colonne et un type de graphique valide.',
                     horizontalalignment='center', verticalalignment='center', fontsize=12)

        # Préparer le fichier à télécharger
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="graphique.png"'
        plt.tight_layout()
        plt.savefig(response, format='png')
        plt.close()

        return response

    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")
