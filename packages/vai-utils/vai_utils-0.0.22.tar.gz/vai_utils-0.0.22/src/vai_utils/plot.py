import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
from PIL import Image
import random
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.ticker as ticker
# import squarify

colors =["#1D2026","#393939","#666666","#BDBDBD","#E0E0E0","#F2F2F2","#FD93B1","#FC2964","#FEC9D8","#FD5F8B","#0095FF","#E6F5FF","#5C33F6","#8566F8",]

def set_graph_dark(fig,ax,**optional_args):
    theme ='black'
    if 'theme' in optional_args:
        theme= optional_args['theme']
    if theme == 'black':
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.yaxis.set_tick_params(colors='white')
        ax.xaxis.set_tick_params(colors='white') 
        ax.xaxis.label.set_color('white') 
        ax.yaxis.label.set_color('white')
        ax.set_title('',color='white')

    if('box_plots' in optional_args):
        for element in ['caps', 'whiskers']:
            for box in optional_args['box_plots'][element]:
                box.set(color='white')




def insertion_sort(header, header_data):
    length = len(header_data)
    indices = list(range(length))
    indices.sort(key=lambda i: abs(header_data[i]), reverse=True)
    final_headers = []
    final_headers_data = []
    my_slice = slice(0,  9 if len(header)> 9 else len(header))
    indexes = indices[my_slice]
    for index in indexes:
        final_headers.append(header[index])
        final_headers_data.append(header_data[index])
    
    header = final_headers
    header_data = final_headers_data
    
    for i in range(len(header_data)):
        current = header_data[i]
        current_header = header[i]
        j = i - 1
        
        while j >= 0 and header_data[j] > current:
            header_data[j + 1] = header_data[j]
            header[j + 1] = header[j]
            j -= 1
        
        header_data[j + 1] = current
        header[j + 1] = current_header
    
    # header_data.reverse()
    # header.reverse()
    
    return {'categories':header, 'values':  header_data}

def line_chart(xAxisvalue, predicatedLine, actualLine, **optional_params):
    x = np.arange(len(xAxisvalue))
    x_smooth = np.linspace(0, len(xAxisvalue) - 1, 100)
    f_actual = interp1d(x, actualLine, kind='cubic')
    f_predicted = interp1d(x, predicatedLine, kind='cubic')
    actualLine_smooth = f_actual(x_smooth)
    predicatedLine_smooth = f_predicted(x_smooth)
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.plot(x_smooth, actualLine_smooth, color="#FF8080", label='Actual')
    ax.plot(x_smooth, predicatedLine_smooth, color="#80A0FF", label='Predicted')

    theme = 'black'
    if 'theme' in optional_params:
        theme = optional_params['theme']
        if theme == 'black':
            plt.rcParams['text.color'] = 'white'
            plt.rcParams['axes.labelcolor'] = 'white'
            plt.rcParams['axes.edgecolor'] = 'white'
            plt.rcParams['xtick.color'] = 'white'
            plt.rcParams['ytick.color'] = 'white'
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')

    legend = ax.legend(bbox_to_anchor=(1.02, 1), facecolor='black' if theme == 'black' else 'white', edgecolor='black' if theme == 'white' else 'white')
    legend.get_texts()[0].set_color('black' if theme == 'white' else 'white')
    legend.get_texts()[1].set_color('black' if theme == 'white' else 'white')
    legend.get_frame().set_facecolor('black' if theme == 'black' else 'white')
    legend.get_frame().set_edgecolor('white' if theme == 'black' else 'black')
    ax.xaxis.set_major_locator(plt.IndexLocator(base=1, offset=0))
    ax.set_xticklabels(xAxisvalue, color='black' if theme == 'white' else 'white')
    ax.yaxis.set_tick_params(colors='black' if theme == 'white' else 'white')
    ax.set_facecolor('black' if theme == 'black' else 'white')
    fig.patch.set_facecolor('black' if theme == 'black' else 'white')
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], color='white' if theme == 'black' else 'black')
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'], color='white' if theme == 'black' else 'black')
    if ('title' in optional_params):
        ax.set_title(optional_params['title'], color='white' if theme == 'black' else 'black')
    name = "line_chart"
    plt.savefig(name + '.png', facecolor='black' if theme == 'black' else 'white', transparent=True)
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()


# xAxisvalue = ['8:00 PM', '9:00 PM', '10:00 PM', '12:00 PM', '1:00 AM', '3:00 AM', '3:00 AM', '4:00 AM', '5:00 AM',
#               '3:00 AM', '3:00 AM', '4:00 AM', '5:00 AM']
# predicatedLine = [30, 30, 33, 28, 34, 29, 33, 28, 34, 29, 28, 33, 32]
# actualLine = [30, 30, 29, 33, 32, 29, 29, 33, 32, 29, 30, 31, 37]
# line_chart(xAxisvalue, predicatedLine, actualLine, xlabel='xlabel', ylabel='ylabel', title='title')



def horizontal_waterfall(categories, values, **optional_params):
    fig, ax = plt.subplots()
    theme = 'black'
    if 'theme' in optional_params:
        theme = optional_params['theme']
    categories = [c for c, v in zip(categories, values) if v is not None]
    values = [v for v in values if v is not None]
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], fontsize=12, color='white' if theme == 'black' else 'black')
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'], fontsize=12, color='white' if theme == 'black' else 'black')
    if 'title' in optional_params:
        title = optional_params['title']
        theme = optional_params.get('theme', 'black')
        title_color = 'white' if theme == 'black' else 'black'
        ax.set_title(title, fontsize=15, color=title_color)

    bars = ax.barh(categories, values, align='center')

    if theme == 'black':
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['bottom'].set_linewidth(0.8)
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['top'].set_linewidth(0.8)
        ax.spines['right'].set_linewidth(0.8)

        text_color = 'white'
        bar_color = '#0095FF'
        fig.set_facecolor('black')
        ax.grid(axis='x', color='white', linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
    else:
        text_color = 'black'
        bar_color = '#0095FF'
        fig.set_facecolor('white')
        ax.grid(axis='x', color='black', linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)

    for bar, value in zip(bars, values):
        if value < 0:
            bar.set_color('#FC2964')
        else:
            bar.set_color(bar_color)

    ax.set_yticklabels(categories, fontsize=8, color=text_color)
    ax.set_xticklabels(ax.get_xticks(), fontsize=8, color=text_color)

    ax.set_facecolor('white' if theme == 'white' else 'black')

    name = str(random.random())
    plt.savefig(name + '.png', facecolor='white' if theme == 'white' else 'black')
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()

    if 'theme' in optional_params:
        print("Theme:", optional_params['theme'])

# categories = ['Burger', 'Pizza', 'Sandwich', 'Pasta', 'Momos', 'Garlic']
# values = [-10, -5, -4, 4, 5, 10]
# title = 'Horizontal Waterfall'
# xlabel='xlabel'
# horizontal_waterfall(categories, values, xlabel=xlabel, ylabel='ylabel', title=title)



def vertical_waterfall(categories, values, **optional_params):
    fig, ax = plt.subplots()
    res =  insertion_sort(categories, values)
    categories = res['categories']
    values = res['values']
    categories = [c for c, v in zip(categories, values) if v is not None]
    values = [v for v in values if v is not None]

    if 'title' in optional_params:
        title = optional_params['title']
        theme = optional_params.get('theme', 'black')
        title_color = 'white' if theme == 'black' else 'black'
        ax.set_title(title, fontsize=15, color=title_color)

    cumulative_sum = [sum(values[:i + 1]) for i in range(len(values))]
    bars = ax.bar(categories, values, align='center')

    # ax.set_xlabel('Categories', fontsize=12, color='white')

    # ax.set_ylabel('Value', fontsize=12, color='white')
   

    theme = 'black'
    if 'theme' in optional_params:
        theme = optional_params['theme']

    if theme == 'black':
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['bottom'].set_linewidth(0.8)
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['top'].set_linewidth(0.8)
        ax.spines['right'].set_linewidth(0.8)

        text_color = 'white'
        bar_color = '#0095FF'
        fig.set_facecolor('black')
        ax.grid(axis='y', color='white', linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(axis='y', colors='white')  # Set y-axis tick color to white
    else:
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['bottom'].set_linewidth(0.8)
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['top'].set_linewidth(0.8)
        ax.spines['right'].set_linewidth(0.8)

        text_color = 'black'
        bar_color = '#0095FF'
        fig.set_facecolor('white')
        ax.grid(axis='y', color='black', linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(axis='y', colors='black')  # Set y-axis tick color to black

    ax.set_xticks(range(len(categories)))  # Adjust the x-ticks positions
    ax.set_xticklabels(categories, rotation=45, fontsize=8, color=text_color)

    ax.set_facecolor('white' if theme == 'white' else 'black')
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'],fontsize=12, color='white' if theme == 'black' else 'black')
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'],fontsize=12, color='white' if theme == 'black' else 'black')
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    for bar, value in zip(bars, values):
        if value < 0:
            bar.set_color('#FC2964')
        else:
            bar.set_color(bar_color)

    name = str(random.random())
    plt.savefig(name + '.png', facecolor='white' if theme == 'white' else 'black')
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()
    
    if 'theme' in optional_params:
        print("Theme:", optional_params['theme'])


# categories = ['W1', 'W3', 'W5', 'W7', 'W9', 'W10']
# values = [-4, -5, -10 , 10, 5, 4 ]
# title = 'Vertical Waterfall'
# vertical_waterfall(categories, values, title=title, xlabel='xlabel', ylabel='ylabel')



def baseline_graph(baseline, x_labels, series_colors,*series_data, **optional_params):
    fig, ax = plt.subplots()

    for i, series in enumerate(series_data):
        percentage_change_series = [(value - baseline[j]) / baseline[j] * 100 for j, value in enumerate(series)]
        color = series_colors[i % len(series_colors)]
        ax.plot(x_labels, percentage_change_series, label=f'Product {i+1}', marker='o', color=color)
    theme ='black'
    if 'theme' in optional_params:
        theme= optional_params['theme']
    ax.axhline(y=0,  color='black' if theme != 'black'else 'white', linestyle='dotted', label='Baseline 1')

    ax.grid(True, color='black' if theme != 'black'else 'white', linestyle='--', alpha=0.5)
    ax.set_title('Chg. from Baseline', fontdict={'fontsize': 15, 'color': 'black' if theme == 'black'else 'white'})
    legend = ax.legend(bbox_to_anchor=(1, 0.91), facecolor='black' if theme == 'black'else 'white')
    for text in legend.get_texts():
        text.set_color('black' if theme != 'black'else 'white')

    ax.set_xlabel('X Labels', fontdict={'fontsize': 12, 'color': 'black' if theme == 'black'else 'white'})
    ax.set_ylabel('Percentage Change', fontdict={'fontsize': 12, 'color':'black' if theme == 'black'else 'white'})
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], color='white' if theme == 'black' else 'black')
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'], color='white' if theme == 'black' else 'black')
    if ('title' in optional_params):
        ax.set_title(optional_params['title'], color='white' if theme == 'black' else 'black')
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    if theme == 'black':
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['bottom'].set_linewidth(0.8)
        ax.spines['left'].set_linewidth(0.8)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

    name = str(random.random())
    plt.savefig(name + '.png', bbox_inches='tight', facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()


# baseline = [10, 12, 14, 16, 18]
# series1 = [11, 15, 12, 13, 20]
# series2 = [9, 11, 13, 15, 17]
# series3 = [13, 14, 10, 12, 11]
# x_labels = ['W1', 'W3', 'W5', 'W7', 'W9']
# colors = ["#FC2964", "#0095FF", "#5C33F6"]
# baseline_graph(baseline, x_labels, colors, series1, series2, series3, title='title', xlabel='xlabel',ylabel='ylabel')



def scatter_plot_graph(marker_shapes, x_values, series_data, colors, **optional_params):
    fig, ax = plt.subplots(figsize=(11, 9))
    np.random.seed(19680801)
    sizes = np.random.rand(len(x_values[0])) * 50 + 50
    theme = 'black'
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)
    for i, marker in enumerate(marker_shapes):
        x = x_values[i]
        y = series_data[i]
        color = colors[i % len(colors)]
        ax.scatter(x, y, s=sizes, alpha=0.5, marker=marker, color=color, label="Group {}".format(i+1))

    legend = ax.legend(bbox_to_anchor=(1, 0.9), facecolor='black' if theme == 'black' else 'white')

    if theme == 'black':
        for text in legend.get_texts():
            text.set_color('white')

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], fontdict={'fontsize': 12})   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'],fontdict={'fontsize': 12}) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'],fontdict={'fontsize': 15})

    name = str(random.random())
    plt.savefig(name + '.png',  bbox_inches='tight',facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()

# marker_shapes = ['s', 'o', 'D']
# x_values = [np.arange(0.15, 50.0, 2.0), np.arange(0.15, 50.0, 2.0), np.arange(0.15, 50.0, 2.0)]
# series_data = [
#     x_values[0] ** 1.3 + np.random.rand(*x_values[0].shape) * 30.0,
#     x_values[1] ** 1.5 + np.random.rand(*x_values[1].shape) * 40.0,
#     x_values[2] ** 1.2 + np.random.rand(*x_values[2].shape) * 20.0
# ]
# colors = ["#FC2964", "#0095FF", "#5C33F6"]
# scatter_plot_graph(marker_shapes, x_values, series_data, colors,title='title', xlabel='xlabel',ylabel='ylabel')



def stack_bar(categories, below, above, **optional_params):
    theme ='black'
    if 'theme' in optional_params:
        theme= optional_params['theme']
    species = categories
    weight_counts = {
        "Below": np.array(below),
        "Above": np.array(above),
    }
    width = 0.5

    fig, ax = plt.subplots()

    bottom = np.zeros(len(categories))
    index = 0
    color = ["#FC2964", "#0095FF"]
    if 'color' in optional_params:
        color = optional_params['color']

    for boolean, weight_count in weight_counts.items():
        p = ax.bar(species, weight_count, width, color=color[index], label=boolean, bottom=bottom)
        index += 1
        bottom += weight_count

    if 'xlabel' in optional_params:
        ax.set_xlabel(optional_params['xlabel'], color='white' if theme == 'black' else 'black')
    if 'ylabel' in optional_params:
        ax.set_ylabel(optional_params['ylabel'], color='white' if theme == 'black' else 'black')
    if 'title' in optional_params:
        ax.set_title(optional_params['title'], color='white' if theme == 'black' else 'black')
    if 'legend' in optional_params:
        legend = ax.legend(loc='lower center', title=optional_params['legend'], bbox_to_anchor=(0.50, -0.30), ncol=2)
        
    fig.tight_layout()

    if theme == 'black':
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['bottom'].set_linewidth(0.8)
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['top'].set_linewidth(0.8)
        ax.spines['right'].set_linewidth(0.8)

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        legend.get_frame().set_facecolor('black')
        legend.get_title().set_color('white')
        for text in legend.get_texts():
            text.set_color('white')
    name = str(random.random())
    plt.savefig(name + '.png', facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()

# categories = ('2010','2012','2014','2016','2018','2020')
# below=[30,35,40,45,50,55]
# above=[70,70,45,50,55,60]
# stack_bar(categories,below,above,title='Stack bar chart',xlabel='xlabel',ylabel='ylabel',legend='legends')



def heatmap_graph(y_axis_data, x_axis_data, colors,**optional_params):
    fig, ax = plt.subplots(figsize=(8, 8))
    theme = "black"
    if 'theme' in optional_params:
        theme=optional_params['theme']

    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)

    data = np.random.rand(len(y_axis_data), len(x_axis_data))
    cmap = ListedColormap(colors)
    heatmap = ax.imshow(data, cmap=cmap, interpolation='nearest')
    ax.set_yticks(range(len(y_axis_data)))
    ax.set_xticks(range(len(x_axis_data)))
    cbar = plt.colorbar(heatmap)

    if theme == 'black':
        cbar.ax.tick_params(labelcolor='white')

    ax.set_xticklabels(ax.get_xticklabels(), ha='center')
    plt.subplots_adjust(bottom=0.2)

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], fontdict={'fontsize': 12})   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'],fontdict={'fontsize': 12}) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])

    name = str(random.random())
    plt.savefig(name + '.png', facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()

# y_axis_data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# x_axis_data = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2017, 2019, 2021, 2023]
# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2", "#FD93B1",
#           "#FC2964", "#FEC9D8", "#FD5F8B", "#0095FF", "#E6F5FF", "#5C33F6", "#8566F8"]
# heatmap_graph(y_axis_data, x_axis_data, colors,title='Heatmap',xlabel='xlabel',ylabel='ylabel')




def heatmap2_graph(y_axis_data, x_axis_data, colors,dataFrom,dataTo,**optional_params):
    fig, ax = plt.subplots(figsize=(8, 8))
    theme="black"
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)

    data = np.random.randint(dataFrom, dataTo, size=(len(y_axis_data), len(x_axis_data)))
    cmap = ListedColormap(colors)
    heatmap = ax.imshow(data, cmap=cmap, interpolation='nearest')
    ax.set_yticks(range(len(y_axis_data)), y_axis_data)
    ax.set_xticks(range(len(x_axis_data)), x_axis_data)
    cbar = plt.colorbar(heatmap)

    if theme == 'black':
        cbar.ax.tick_params(labelcolor='white')
    for i in range(len(y_axis_data)):
        for j in range(len(x_axis_data)):
            ax.text(j, i, str(data[i, j]), ha='center', va='center', color='black')

    ax.set_xticklabels(ax.get_xticklabels(), ha='center')
    plt.subplots_adjust(bottom=0.2)

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], fontdict={'fontsize': 12})   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'],fontdict={'fontsize': 12}) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])

    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# dataFrom=1
# dataTo=100
# y_axis_data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# x_axis_data = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2017, 2019, 2021, 2023]
# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2", "#FD93B1",
#           "#FC2964", "#FEC9D8", "#FD5F8B", "#0095FF", "#E6F5FF", "#5C33F6", "#8566F8"]
# heatmap2_graph(y_axis_data, x_axis_data, colors,dataFrom,dataTo,title='Heatmap',xlabel='xlabel',ylabel='ylabel')



def boxPlot_graph(data, titles, colors, **optional_params):

    fig, ax = plt.subplots()
    medians = [np.median(dataset) for dataset in data]
    sorted_data = sorted(zip(data, medians, titles, colors), key=lambda x: x[1])
    sorted_values, sorted_medians, sorted_titles, sorted_colors = zip(*sorted_data)
    box_plot = ax.boxplot(sorted_values, patch_artist=True)
    theme="black"
    if 'theme' in optional_params:
        theme = optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig, ax, box_plots=box_plot, theme=theme)
    for patch, color in zip(box_plot['boxes'], sorted_colors):
        patch.set(facecolor=color, linewidth=1)

    ax.set_xticklabels(sorted_titles)
    legend = ax.legend().remove()

    if 'xlabel' in optional_params:
        ax.set_xlabel(optional_params['xlabel'], fontdict={'fontsize': 12})
    if 'ylabel' in optional_params:
        ax.set_ylabel(optional_params['ylabel'], fontdict={'fontsize': 12})
    if 'title' in optional_params:
        ax.set_title(optional_params['title'])
    if 'legend' in optional_params:
        legend.set_title(optional_params['legend'])

    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# data = [[25, 26, 27, 28, 29],
#         [20, 21, 22, 23, 24],
#         [10, 12, 14, 16, 18],
#         [10, 15, 20, 25, 30],
#         [20, 23, 26, 29, 32],
#         [22, 26, 29, 33, 36]]
# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2", "#FD93B1",
#           "#FC2964", "#FEC9D8", "#FD5F8B", "#0095FF", "#E6F5FF", "#5C33F6", "#8566F8"]
# titles = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6']
# boxPlot_graph(data, titles, colors,title='Title',xlabel='xlabel',ylabel='ylabel')



def boxPlot2_graph(data, titles, colors, **optional_params):
    fig, ax = plt.subplots()
    medians = [np.median(dataset) for dataset in data]
    sorted_data = sorted(zip(data, medians, titles, colors), key=lambda x: x[1])
    sorted_values, sorted_medians, sorted_titles, sorted_colors = zip(*sorted_data)
    box_plot = ax.boxplot(sorted_values, patch_artist=True)
    theme="black"
    if 'theme' in optional_params:
        theme = optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig, ax, box_plots=box_plot, theme=theme)
    for patch, color in zip(box_plot['boxes'], sorted_colors):
        patch.set(facecolor=color, linewidth=1)

    ax.set_xticklabels(sorted_titles)
    legend = ax.legend().remove()

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'], fontdict={'fontsize': 12})   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'],fontdict={'fontsize': 12}) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if('legend' in optional_params):
        legend.set_title(optional_params['legend'])

    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# data = [[25, 26, 27, 28, 29],
#         [20, 21, 22, 23, 24],
#         [10, 12, 14, 16, 18],
#         [10, 15, 20, 25, 30],
#         [20, 23, 26, 29, 32],
#         [22, 26, 29, 33, 36]]

# colors = ["#FEC9D8","#FD5F8B","#0095FF","#1D2026","#5C33F6","#8566F8"]
# titles = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6']
# boxPlot2_graph(data, titles, colors, title='Title',xlabel='xlabel',ylabel='ylabel')



def boxPlot3_graph(data, colors,**optional_params):
    fig, ax = plt.subplots(figsize=(10, 6))
    medians = [np.median(dataset) for dataset in data]
    sorted_data = sorted(zip(data, medians,  colors), key=lambda x: x[1])
    sorted_values, sorted_medians,  sorted_colors = zip(*sorted_data)
    box_plots = ax.boxplot(sorted_values, patch_artist=True, vert=True, widths=0.5)
    theme="black"
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig, ax, box_plots=box_plots,theme=theme)

    for patch, color in zip(box_plots['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('white')

    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
    legend_labels = [f'{i+1}' for i in range(len(data))]
    legend =ax.legend(legend_handles, legend_labels, loc='upper right', bbox_to_anchor=(1.1, 1), facecolor='black' if theme == 'black' else 'white')

    if theme == 'black':
        for text in legend.get_texts():
            text.set_color('white')
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel']) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if('legend' in optional_params):
        legend.set_title(optional_params['legend'])

    name = str(random.random())
    plt.savefig(name + '.png', facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()


# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2",
#           "#FD93B1", "#FC2964", "#FEC9D8"]
# data=[[10, 15, 20, 25, 30],
#       [20, 25, 29, 33, 35],
#       [22, 26, 29, 33, 36],
#       [22, 26, 29, 33, 36],
#       [22, 26, 29, 33, 36],
#       [20, 23, 26, 29, 32],
#       [20, 23, 26, 29, 32],
#       [10, 12, 14, 16, 18],
#       [20, 21, 22, 23, 24],
#       [20, 21, 22, 23, 24],
#       [25, 26, 27, 28, 29],
#       [20, 21, 22, 23, 24]
# ] 
# boxPlot3_graph(data, colors, title='BoxPlot3',xlabel='xlabel',ylabel='ylabel', legend='legends')



def dot_plot(categories,data,**optional_params):
    fig, ax = plt.subplots()
    theme="black"
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)

    ax.set_aspect('equal')
    ax.scatter(np.arange(len(categories)), data, s=100, c='#8566F8', alpha=0.7)
    ax.set_xticks(np.arange(len(categories)))
    ax.set_xticklabels(categories)

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel']) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])

    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# categories = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
# values = ['Option 1','Option 2','Option 3','Option 4','Option 5','Option 6','Option 7','Option 8','Option 9','Option 10','Option 11','Option 12','Option 13','Option 14','Option 15','Option 16']
# dot_plot(categories,values, xlabel='xlabel', ylabel='ylabel',title='title')



def dot_plot_grouped(categories, data, **optional_params):
    colors = ["#FD93B1", "#FC2964", "#8566F8", "#5C33F6", "#E0E0E0", "#F2F2F2","#FD93B1", "#FC2964", "#FEC9D8"]
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    theme="black"
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)

    grouped_categories = [categories[i:i+4] for i in range(0, len(categories), 4)]
    group_count = len(grouped_categories)
    index=0

    for i, group_cats in enumerate(grouped_categories):
        ax.scatter(group_cats, data[i*4:(i+1)*4], s=100, c=colors[index], alpha=0.7)
        index=index+1

    ax.set_xticks(np.arange(len(categories)))
    ax.set_xticklabels(categories)
    ax.set_yticks(np.arange(len(categories)))
    y_labels = ax.set_yticklabels(data)
    ax.legend(np.arange(group_count)+1,title='legend',loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol = 4)

    for i, label in enumerate(y_labels):
        if i < 4:
            label.set_color("#FD93B1")
        elif i < 8:
            label.set_color("#FC2964")
        elif i < 12:
            label.set_color("#8566F8")
        else:
            label.set_color("#5C33F6")

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel']) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])

    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png')
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# categories = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# values = ['Option 0', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5', 'Option 6', 'Option 7',
#           'Option 8', 'Option 9', 'Option 10', 'Option 11', 'Option 12', 'Option 13', 'Option 14', 'Option 15']
# dot_plot_grouped(categories, values, xlabel='xlabel', ylabel='ylabel', title='title')


def scatter_plot_with_dotted_line(data,**optional_params):
    fig, ax = plt.subplots() 
    shapes = ["o", "v", "^", ".", ",", "<", ">", "1", "2", "3", "4", "8", "s", "p"]
    color = ["#8566F8","#8566F8","#666666","#BDBDBD","#FD93B1","#FEC9D8","#393939"]
    theme="black"
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)
    index=0

    for y in data:
        res = random.sample(range(1, len(y)+1), len(y))
        ax.scatter(res, y,color=color[index],marker=shapes[index])
        index=index+1

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
        # ax.xaxis.label.set_color('white') 
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
        # ax.yaxis.label.set_color('white') 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])

    # if ('handles' in optional_params):
    #     ax.legend(handles=optional_params['handles'],ncol = 1 ,loc='upper left', bbox_to_anchor= (0.0, 1.010))   
    ax.axhline(y = (len(data)*len(data[0]))/2, color = '#FC2964', linestyle = ':')
    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# data=[[2,4,6,8,10,3,6,9,12,15,5,8,11,13,17,7,14,17,16,19,21,23,18,19,31,25,27,24,26,30,32,41,33,25,35,41,]]
# handles=['Group 1']
# scatter_plot_with_dotted_line(data,title='Scatter plot with dotted line',xlabel='xlabel',ylabel='ylabel')



def scatter_plot_with_line(data,**optional_params):
    fig, ax = plt.subplots()
    theme="black"
    if 'theme' in optional_params:
        theme=optional_params['theme']
    if theme == 'black':
        set_graph_dark(fig,ax,theme=theme)

    shapes = ["o", "v", "^", ".", ",", "<", ">", "1", "2", "3", "4", "8", "s", "p"]
    color = ["#8566F8","#8566F8","#666666","#BDBDBD","#FD93B1","#FEC9D8","#393939"]
    index=0

    for y in data:
        res = random.sample(range(1, len(y)+1), len(y))
        ax.scatter(res, y,color=color[index],marker=shapes[index])
        index=index+1

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])   
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel']) 
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
        
    # ax.legend(handles=handles,ncol = 1 ,loc='upper left', bbox_to_anchor= (0.0, 1.010))
    x1=np.array([1,(len(data)*len(data[0]))-1])
    y1=np.array([1,(len(data)*len(data[0]))-1])
    ax.plot(x1,y1,label='line',color = '#FC2964')
    name = random.random()
    plt.savefig(str(name) + '.png' , facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()
    # plt.show()

# data=[[2,4,6,8,10,3,6,9,12,15,5,8,11,13,17,7,14,17,16,19,21,23,18,19,31,25,27,24,26,30,32,41,33,25,35,41,]]
# handles=['Group 1']
# scatter_plot_with_line(data,title='Scatter plot with line',xlabel='xlabel',ylabel='ylabel')



def explanability_chart(data, **optional_params):
    flattened_list =[]
    for sublist in  list(data["inputs"].values()):
        for item in sublist:
            flattened_list.append(item)
    answer =  insertion_sort(list(data['inputs'].keys()), flattened_list)
    fig, ax = plt.subplots()
    print(answer)
    theme ='black'
    if 'theme' in optional_params:
        theme= optional_params['theme']
    categories = [c for c, v in zip(answer['categories'],answer['values']) if v is not None]
    values = [v for v in answer['values'] if v is not None]
    print(values)
    if 'title' in optional_params:
        ax.set_title(optional_params['title'], fontdict={'fontsize': 15, 'color': ('black' if theme != 'black'else 'white')})
    bars = ax.barh(categories, values, align='center')

    ax.set_xlabel('Value', fontdict={'fontsize': 12, 'color':  ('black' if theme != 'black'else 'white')})
    ax.set_ylabel('Categories', fontdict={'fontsize': 8, 'color':  ('black' if theme != 'black'else 'white')})
    ax.set_title('FEATURE CONTRIBUTION', fontdict={'fontsize': 15, 'color':  ('black' if theme != 'black'else 'white')})
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    if theme == 'black':
        ax.spines['top'].set_visible(True) 
        ax.spines['right'].set_visible(True) 
        ax.spines['bottom'].set_visible(True) 
        ax.spines['left'].set_visible(True) 

        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white') 
        ax.spines['bottom'].set_color('white')  
        ax.spines['left'].set_color('white') 

        ax.spines['top'].set_linewidth(0.8)  
        ax.spines['right'].set_linewidth(0.8)  
        ax.spines['bottom'].set_linewidth(0.8) 
        ax.spines['left'].set_linewidth(0.8)  

    ax.set_axisbelow(True)
    color=('black' if theme != 'black'else 'white')
    ax.grid(axis='x', color=color  , linestyle='--', alpha=0.5)
    for bar, value in zip(bars, answer['values']):
        if value < 0:
            bar.set_color('#FC2964')
        else:
            bar.set_color('#0095FF')

    ax.set_yticklabels(categories, fontdict={'fontsize': 8, 'color': color })
    ax.set_xticklabels(ax.get_xticks(), fontdict={'fontsize': 8, 'color': color })
    print(data['outputs'][0])
    ax.set_ylim( data['outputs'][0])
    ax.set_facecolor('black' if theme == 'black'else 'white')
    fig.patch.set_facecolor('black' if theme == 'black'else 'white')
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = str(random.random())
    plt.savefig(name + '.png',  bbox_inches='tight',facecolor='black' if theme == 'black'else 'white' )
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()
    # plt.show()


# categories = ['Burger', 'Pizza', 'sandwich', 'pasta', 'momos', 'garlic']
# values = [-10, -5, -4, 4, 5, 10]
# data = {
# "inputs": { "age": [0.051], "capital-loss": [-0.006], "education": [-0.057], "education-num": [-0.034], "hours-per-week": [0.174], "native-country": [0.006], "occupation": [-0.03], "relationship": [0.163], "workclass": [0] }, "outputs": [0.267]
# }
# explanability_chart(data,title='Secondary text',xlabel='xlabel',ylabel='ylabel')















