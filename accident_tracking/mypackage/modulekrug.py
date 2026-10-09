import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

data_dir =  Path('../data')
figures_dir = Path('../reports/figures')

df_head = pd.read_csv(data_dir/'df_listparam.csv')
#3 Функция берет на вход название параметра и выдает его обозначение

def get_name(parametr):
    
    """
    Функция находит обозначение заданного параметра в таблице "df_head" 
    """
    try:       
        parametr_name = df_head[df_head['position'].isin([parametr.lower()])]
        return parametr_name
    except:
        print('Параметр не найден')

#4 Функция находит все значения в поле 'name'
# Метод .str.contains() проверяет, содержит ли каждое значение в столбце заданный шаблон
#(который может быть регулярным выражением),
#и возвращает булево Series или DataFrame с теми же размерами, что и исходные данные.
#case=False , т.е. без учета регистра

def find_parametr(text):
    
    """
    Функция находит параметры содержащие в названии заданное слово без учета регистра
    """
    try:
        parametr = df_head[df_head['name'].str.contains(text, case=False)]
        return parametr
    except:
        print('Параметр не найден')

#5  Поиск в поле index. Ищет заданное значение и выдает название параметра и его обозначение.
def find_values_by_index(parametrs):
    
    try:
        lable_text = []
        for par in parametrs:
            if len(df_head[df_head['position'].isin([par.lower()])])>0:
                parametr_name = df_head[df_head['position'].isin([par.lower()])]                
                ch_par = get_name(par).iloc[0]['name']
            else:
                ch_par = par
            lable_text.append(par + " - " + ch_par)
        return lable_text
    except Exception as e:
        print('Параметр не найден', e)

def add_savefig(list_parametrs, value_resample, name_fig='par'):
    params_str = '_'.join(str(p) for p in list_parametrs)
    if len(params_str) > 33:
        params_str = params_str[:33] + f'_and_{len(list_parametrs)-3}more'
    filename = f'Trends_{name_fig}_{params_str}_{value_resample}.png'
    plt.savefig(figures_dir/filename , dpi=150, bbox_inches='tight')

#6 
def plot_trends(data, list_parametrs, value_resample = '1h', name_fig='par', savefig=True):
    
    """
    функция строит графики изменения заданных параметров.
    data -  название DataFrame,
    parametrs - список параметров для построения,
    По желанию можно ресемплировать данные - value_resample
    Для подписей используется db_head 
    """   
    try:
        plt.style.use('bmh')
        labl_text = find_values_by_index(list_parametrs)
        data.columns=data.columns.str.lower()
        i = 0    
        for i, x in enumerate(list_parametrs, 0):
            if x.lower() in data:            
                data[x.lower()].resample(value_resample).mean().plot(figsize=(10, 5), label = labl_text[i], alpha=.7)
                plt.legend(loc = 'upper left', prop = {'size': 10})
                
        plt.title(f'\nГрафик за период с {str(data.index[0])} по {str(data.index[-1])}', fontsize = 14, color='#2F4F4F')    
        plt.xlabel('Метки времени', fontsize = 12, color='#4682B4')
        plt.ylabel('Показания приборов', fontsize = 12, color='#4682B4')

        #params_str = '_'.join(str(p) for p in list_parametrs)
        #if len(params_str) > 80:
        #    params_str = params_str[:80] + f'_and_{len(list_parametrs)-3}more'
        #filename = f'Trends_{params_str}_{value_resample}.png'
        #plt.savefig(figures_dir/filename , dpi=150, bbox_inches='tight')
        if savefig:
            add_savefig(list_parametrs, value_resample, name_fig)
        plt.show()
    except Exception as e:
        print('Параметр не найден', e)

#7 
def plot_group(data, list_parametrs, value_resample = '1h', savefig=True):
    
    """
    функция строит графики изменения заданных параметров.
    data -  название DataFrame,
    parametrs - список параметров для построения,
    По желанию можно ресемплировать данные - value_resample
    Для подписей используется 'db_head' 
    """
    try:
        plt.style.use('bmh')
        data.columns = data.columns.str.lower()
        n_plots = len(list_parametrs)
        fig_height = n_plots * 2.5 
        fig = plt.figure(figsize=(10, fig_height))

        plt.suptitle(f'\nГрафик за период с {str(data.index[0])} по {str(data.index[-1])}', fontsize = 12, color='#2F4F4F')        
        rows = len(list_parametrs)
        for i, parametr in enumerate(list_parametrs, 1):       
            title = str(find_values_by_index([parametr]))
            ax = fig.add_subplot(rows, 1, i)
            plt.xlabel('Date', fontsize = 8, color='#4682B4')
            plt.ylabel('Values', fontsize = 8, color='#4682B4')
            if value_resample == '':
                plt.plot(data[parametr.lower()])
            else:    
                plt.plot(data[parametr.lower()].resample(value_resample).mean())
        
            ax.set_title(f'{title}\n', fontsize = 10, color='#2F4F4F')
            """ plt.tight_layout() - это функция в библиотеке Matplotlib, 
                которая автоматически настраивает размещение элементов на графике, 
                чтобы они не накладывались друг на друга и занимали доступное пространство оптимальным образом."""
            plt.tight_layout()
        
        if savefig:
            add_savefig(list_parametrs, value_resampleб , name_fig='group')            
        plt.show()
    except Exception as e:
        print('Параметр не найден', e)

#8 

def plot_corr(data, parametrs, method='pearson', print_table=False, savefig=True):
    """
    функция строит Heatmap для отображения корреляции. 
    data -  название DataFrame,
    parametrs - список параметров для построения,
    method - метод корреляции: 
     - 'pearson': стандартный коэффициент корреляции Пирсона (по умолчанию).
     - 'kendall': коэффициент корреляции Кендалла.
     - 'spearman': коэффициент корреляции Спирмена.
    Для подписей используется 'db_head' 
    """
    try:
        x = len(parametrs) * 0.8
        y = len(parametrs) * 0.8
        plt.figure(figsize=(x, y), dpi= 80)
        plt.title('Корреляционная матрица', fontsize=14, color='#2F4F4F')
    
        labl_text_x = []
        labl_text_y = []
        
        try:
            labl_text_x = find_values_by_index(parametrs)
            labl_text_y = find_values_by_index(parametrs)
        except:
            labl_text_x = parametrs
            labl_text_y = parametrs
                   
        #cmap='BrBG',
        corr_table = data[parametrs].corr(method=method)
        sns.heatmap(corr_table, cmap='coolwarm',  annot=True, fmt='.2f', 
                    xticklabels = labl_text_x, 
                    yticklabels = labl_text_y,
                    center=0)

        plt.xticks(fontsize=9, color='#008080', rotation=45, ha='right')
        plt.yticks(fontsize=9, color='#008080')
        if savefig:
            params_str = '_'.join(str(p) for p in parametrs)
            if len(params_str) > 33:
                params_str = params_str[:33] + f'_and_{len(parametrs)-3}more'
            filename = f'Matrix_{params_str}_{method}.png'
            plt.savefig(figures_dir/filename , dpi=150, bbox_inches='tight')
        plt.show()
        if print_table == True:
            display(corr_table)
    except Exception as e:
        print('Параметр не найден', e)    