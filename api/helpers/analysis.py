from zipfile import ZipFile
from os import walk
import pandas as pd
import numpy as np
import json
import re

from collections import Counter
from .analysis_exceptions import NoActivityLogFile, NoStudentResultsFile, InvalidDataInFile


ALLOWED_FILE_EXTENTIONS = ('.xls', '.xlsx', '.ods', '.odf', '.odt', '.csv')


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class PlatformDataAnalyser():

    def __init__(self, upload_path):
        self.upload_path = upload_path

        self.student_results = None
        self.system_logs = None
        self.list_ex = None

        self.results_df = []
        self.logs_df = []

        self.correlation_data = None
        self.corr_freq_distrib = None
        self.statistical_data = {}

        self.event_context = 'Assignment: Качване на Упр.'
        self.event_name = 'Submission created.'

        self.init_data_from_file()

    def init_data_from_file(self):
        for content in walk(self.upload_path):

            # Check if there are any files in the current dir
            if content[2]:
                # if there are files, loop through all and check if they are of the allowed types
                for item in content[2]:
                    data_file = f'{content[0]}/{item}'

                    if item.endswith('.zip'):
                        self.handle_zip_file(data_file)
                    elif item.endswith(ALLOWED_FILE_EXTENTIONS):
                        self.handle_data_file(data_file)

        if not self.results_df and not self.logs_df:
            raise InvalidDataInFile
        elif not self.results_df:
            raise NoStudentResultsFile
        elif not self.logs_df:
            raise NoActivityLogFile

        if self.results_df and self.logs_df:
            self.student_results = pd.concat(
                self.results_df).sort_values(by='ID', ascending=True)
            self.system_logs = pd.concat(self.logs_df)

            filtered_data = self.system_logs[self.system_logs['Event context'].str.contains(
                self.event_context) & (self.system_logs['Event name'] == self.event_name)]

            self.list_ex = list(filtered_data.groupby('Event context').groups.keys())

            for x in (self.event_context, *self.list_ex):
                self.statistical_data[x] = {}

            del self.results_df
            del self.logs_df

    def handle_zip_file(self, path_to_file):
        with ZipFile(path_to_file) as input_archive:
            for item in input_archive.namelist():
                if item.endswith(ALLOWED_FILE_EXTENTIONS):
                    with input_archive.open(item) as data_file:
                        self.handle_data_file(data_file)

    def handle_data_file(self, path_to_file):
        df = pd.read_csv(path_to_file) if str(path_to_file).endswith(
            '.csv') else pd.read_excel(path_to_file)

        try:
            if 'ID' and 'Result' in df.columns:
                self.results_df.append(df)
            elif 'Event' and 'Component' and 'Description' in df.columns:
                df['User ID'] = df['Description'].apply(
                    lambda x: np.int32(re.sub(r"[\D]+", ' ', x).strip().split()[0]))
                self.logs_df.append(df)
            else:
                raise InvalidDataInFile
        except:
            print("Invalid file uploaded!")

    def freq_dist_analysis(self):

        frequency = {}

        filtered_data = self.system_logs[self.system_logs['Event context'].str.contains(
            self.event_context) & (self.system_logs['Event name'] == self.event_name)]

        # self.list_ex = list(filtered_data.groupby('Event context').groups.keys())

        f_description = filtered_data['Description']

        uploads = np.empty_like(f_description, dtype=int)

        for index, item in enumerate(f_description):
            val = re.sub(r"[\D]+", ' ', item).strip()
            uploads[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

        frequency[self.event_context] = {
            'abs_freq': uploads.sum().item(), 'rel_freq': 1.0}

        total = frequency[self.event_context]['abs_freq']

        for ex in self.list_ex:
            f = filtered_data[filtered_data['Event context'].str.contains(
                ex)]['Description']
            uploads = np.empty_like(f, dtype=int)

            for index, item in enumerate(f):
                val = re.sub(r"[\D]+", ' ', item).strip()
                uploads[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

            abs_f = uploads.sum().item()
            rel_f = np.round(abs_f / total * 100, 2).item()
            frequency[ex] = {'abs_freq': abs_f, 'rel_freq': rel_f}

        for key in frequency.keys():
            self.statistical_data[key].update(frequency[key])

    def trend_analysis(self):

        def calc_mode(itterable):
            counter = Counter(itterable)
            mod = tuple(k for k, v in counter.items()
                        if v == counter.most_common(1)[0][1])
            return ', '.join(map(str, mod))

        trend = {}

        filtered_data = self.system_logs[self.system_logs['Event context'].str.contains(
            self.event_context) & (self.system_logs['Event name'] == self.event_name)]

        # self.list_ex = list(filtered_data.groupby('Event context').groups.keys())

        f_description = filtered_data['Description']

        uploads = np.empty_like(f_description, dtype=int)

        for index, item in enumerate(f_description):
            val = re.sub(r"[\D]+", ' ', item).strip()
            uploads[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

        trend[self.event_context] = {}

        trend[self.event_context]['mode'] = calc_mode(uploads)
        trend[self.event_context]['mean'] = np.round(
            np.mean(uploads), 3).item()
        trend[self.event_context]['median'] = np.round(
            np.median(uploads), 3).item()

        for ex in self.list_ex:
            f = filtered_data[filtered_data['Event context'].str.contains(
                ex)]['Description']
            uploads = np.empty_like(f, dtype=int)

            for index, item in enumerate(f):
                val = re.sub(r"[\D]+", ' ', item).strip()
                uploads[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

            moda = calc_mode(uploads)
            mean = np.round(np.mean(uploads), 3).item()
            median = np.round(np.median(uploads), 3).item()

            trend[ex] = {'mode': moda, 'median': median, 'mean': mean}

        for key in trend.keys():
            self.statistical_data[key].update(trend[key])

    def spread_analysis(self):

        spread = {}

        filtered_data = self.system_logs[self.system_logs['Event context'].str.contains(
            self.event_context) & (self.system_logs['Event name'] == self.event_name)]

        # self.list_ex = list(filtered_data.groupby('Event context').groups.keys())

        f_description = filtered_data['Description']

        uploads = np.empty_like(f_description, dtype=int)

        for index, item in enumerate(f_description):
            val = re.sub(r"[\D]+", ' ', item).strip()
            uploads[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

        uploads.sort()

        spread[self.event_context] = {}

        spread[self.event_context]['spread'] = uploads[-1].item() - \
            uploads[0].item()
        spread[self.event_context]['variance'] = np.round(
            np.var(uploads), 4).item()
        spread[self.event_context]['stdev'] = np.round(
            np.std(uploads), 4).item()

        for ex in self.list_ex:
            f = filtered_data[filtered_data['Event context'].str.contains(
                ex)]['Description']
            uploads = np.empty_like(f, dtype=int)

            for index, item in enumerate(f):
                val = re.sub(r"[\D]+", ' ', item).strip()
                uploads[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

            uploads.sort()

            spr = uploads[-1].item() - uploads[0].item()
            var = np.round(np.var(uploads), 4).item()
            std = np.round(np.std(uploads), 4).item()

            spread[ex] = {'spread': spr, 'variance': var, 'stdev': std}

        for key in spread.keys():
            self.statistical_data[key].update(spread[key])

    def correlation_analysis(self):
        df = self.system_logs
        self.student_results['view_count'] = self.student_results['ID'].apply(lambda uid: df[df['Event name'].str.contains(
            'Course viewed') & (df['User ID'] == uid)]['User ID'].count())

        correlation = np.round(self.student_results[['Result', 'view_count']].corr()[
                               'view_count']['Result'], 4)

        corr_data = {}
        corr_data['quotient'] = correlation

        corr = abs(correlation)
        if corr == 0:
            corr_data['dependency'] = 'липсва зависимост'
        elif 0 > corr <= 0.3:
            corr_data['dependency'] = 'зависимостта е слаба'
        elif 0.3 > corr <= 0.5:
            corr_data['dependency'] = 'умерена зависимост'
        elif 0.5 > corr <= 0.7:
            corr_data['dependency'] = 'значителна зависимост'
        elif 0.7 > corr <= 0.9:
            corr_data['dependency'] = 'силна зависимост'
        elif 0.9 > corr < 1:
            corr_data['dependency'] = 'много силна зависимост'
        elif corr == 1:
            corr_data['dependency'] = 'зависимостта е функционална'

        if correlation >= 0:
            corr_data['direction'] = 'положителна'
        else:
            corr_data['direction'] = 'отрицателна'

        self.correlation_data = [corr_data]

    def correlation_freq_dist_analysis(self):
        total_vc = self.student_results['view_count'].sum()

        self.student_results['result_rel_freq'] = self.student_results['view_count'].apply(
            lambda vc: np.round(vc / total_vc * 100, 2))
        correl_df = self.student_results.rename(
            columns={'Result': 'result', 'ID': 'id'}, inplace=False)

        self.corr_freq_distrib = correl_df.to_dict(orient='records')

    def save_all(self):
        self.freq_dist_analysis()
        self.trend_analysis()
        self.spread_analysis()
        self.correlation_analysis()
        self.correlation_freq_dist_analysis()

    def calculate_all(self):
        result = {}
        result['status'] = 200
        result['central_tendency'] = (json.loads(
            self.calculate_central_tendency("all")))
        return json.dumps(result, cls=NpEncoder)
