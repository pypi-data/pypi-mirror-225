import pandas as pd
from pandas_datareader import wb
import country_converter as coco
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import imageio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt

def plot_data(df,variable_name, duration, output_dir='gifs'):
    # Создаем директорию для сохранения гифок
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Удаляем все предыдущие изображения из директории
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    pio.renderers.default = "png"
    png_files = []

    #numeric_cols = df.select_dtypes(include=np.number)
    numeric_cols = df.select_dtypes(include=[np.number, 'object'])
    numeric_cols = numeric_cols.apply(pd.to_numeric, errors='coerce')
    numeric_cols = df.loc[:, numeric_cols.notna().any()]
    # Преобразуем все ячейки в числа, игнорируя ошибки
    values = []
    for col in numeric_cols.columns:
        col_values = pd.to_numeric(numeric_cols[col], errors='coerce').dropna().tolist()
        if col_values:
            values.extend(col_values)

    # вычисляем квантили
    if values:
        q_min = np.quantile(values, 0.05)
        q_max = np.quantile(values, 0.95)
    else:
        q_min = 20
        q_max = 80

    years = range(1960, 2025)
    for year in tqdm(years, desc="Processing years"):
        year_str = str(year)
        col_name = f'{variable_name} {year_str}'
        if col_name not in df.columns:
            continue

        # Создать карту
        map_data = dict(
            type='choropleth',
            locations=df['Country Code'],
            z=df[col_name],
            text=df['Country'],
            zmin=q_min,
            zmax=q_max
        )

        map_layout = dict(title=col_name, geo=dict(showframe=True))
        map_actual = go.Figure(data=[map_data], layout=map_layout)
        filename = f"{col_name}.png"
        filepath = os.path.join(output_dir, filename)
        png_files.append(filepath)
        pio.write_image(map_actual, filepath)

    gif_filename = os.path.join(output_dir, f'{variable_name}.gif')
    with imageio.get_writer(gif_filename, mode='I', duration=duration) as writer:
        for filename in png_files:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove PNG files
    for filename in png_files:
        os.remove(filename)

        