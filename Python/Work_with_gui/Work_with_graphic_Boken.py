# pip3 install pandas
# pip3 install bokeh  
# pip3 install IPython 

# Библиотеки Bokeh
import numpy as np

from bokeh.io import output_notebook
from bokeh.io import output_file

from bokeh.plotting import figure, show

# Мои данные о подсчете слов
day_num = np.linspace(1, 10, 10)
daily_words = [450, 628, 488, 210, 287, 791, 508, 639, 397, 943]
cumulative_words = np.cumsum(daily_words)

# Вывести визуализацию прямо в блокнот
output_file('first_glyphs.html', title='First Glyphs')

# Создаем фигуру с осью x типа datetime
fig = figure(title='My Tutorial Progress',
            plot_height=400, plot_width=700,
            x_axis_label='Day Number', y_axis_label='Words Written',
            x_minor_ticks=2, y_range=(0, 6000),
            toolbar_location=None)

# Ежедневные слова будут представлены в виде вертикальных полос (столбцов)
fig.vbar(x=day_num, bottom=0, top=daily_words, 
        color='blue', width=0.75, 
        name='Daily')

# Накопленная сумма будет линией тренда
fig.line(x=day_num, y=cumulative_words, 
        color='gray', line_width=1,
        name ='Cumulative')

show(fig)