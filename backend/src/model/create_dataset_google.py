from time_series_analysis.time_series import TimeSeries
import pandas as pd
import numpy as np
from tensorflow.keras.utils import to_categorical
from datetime import datetime


def generate_dataset(four_classes=True, spread=0.01, sliding_window=1):
    input_csv_text = '../../data/google_news_headlines_en.csv'
    csv = pd.read_csv(input_csv_text)
    texts = csv[['title', 'date']].values
    print(len(texts))

    time_series = TimeSeries()
    labels = time_series.get_residuums_dates(spread=spread, four_cat=four_classes)


    def filter_dates(texts):
        result_list = []
        date_format = '%d %b %Y'
        date_output = '%m.%Y'
        date_format_default = '%d.%m.%Y'
        for item in texts:
            try:
                date = item[1]
                if '.' in date:
                    new_date = datetime.strptime(date, date_format_default)
                    result_list.append([item[0], new_date.strftime(date_output)])
                else:
                    new_date = datetime.strptime(date, date_format)
                    result_list.append([item[0], new_date.strftime(date_output)])
            except:
                continue
        return result_list


    texts = filter_dates(texts)
    #print(len(texts))


    def merge_data(texts, labels, sliding_window=0):
        final_texts = []
        final_labels = []
        for text_id in range(len(texts)):
            for label_id in range(len(labels) - sliding_window):
                if texts[text_id][1] == labels[label_id + sliding_window][1][3:]:
                    final_texts.append(texts[text_id][0])
                    final_labels.append(labels[label_id + sliding_window][0])
        return final_texts, final_labels


    texts, labels = merge_data(texts, labels, sliding_window=sliding_window)
    #print(len(texts))

    labels = to_categorical(labels)

    i = 0
    with open('../../data/auto_generated_gridsearch.csv', 'w') as output_file:
        if four_classes:
            output_file.write('headline,least,less,more,most')
        else:
            output_file.write('headline,less,equal,more')
        output_file.write('\n')
        for text, label in zip(texts, labels):
            i = i + 1
            t = text.replace(',', '').replace('"', '').replace("'", '')
            if four_classes:
                output_file.write(f'{t},{int(label[0])},{int(label[1])},{int(label[2])},{int(label[3])}\n')
            else:
                output_file.write(f'{t},{int(label[0])},{int(label[1])},{int(label[2])}\n')

