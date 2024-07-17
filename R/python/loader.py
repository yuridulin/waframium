import os
import warnings
import numpy as np # type: ignore
import pandas as pd
from datetime import datetime

from projects import ProjectSetup # type: ignore

warnings.filterwarnings("ignore")

class Settings:
	def __init__(self,
			observation_count: int = 0,
			output_path: str = 'output',) -> None:
		self.observation_count = observation_count
		self.output_path = output_path
		pass

class Constants:
	def __init__(self,
			var: str = 'VAR',
			precision: str = 'PRECISION',

			time: str = 'system_time',
			patient: str = 'system_patient_id',
			disabled_var: str = 'system_patient_disabled',
			death_var: str = 'system_patient_death',
			death_time_var: str = 'system_patient_death_time',

			type_var: str = 'VAR_TYPE',
			type_property: str = 'property',
			type_dynamic: str = 'dynamic',

			value_var: str = 'VALUE_TYPE',
			value_numeric: str = 'numeric',
			value_bool: str = 'boolean',
			value_factor: str = 'factor',
			value_date: str = 'date',

			dependency_var: str = 'DEPENDENCY_TYPE',
			dependency_original: str = 'original',
			dependency_collected: str = 'collected',
			dependency_results: str = 'results',
			dependency_system: str = 'system',
			):
		self.time = time
		self.patient = patient
		self.var = var
		self.type_var = type_var
		self.type_property = type_property
		self.type_dynamic = type_dynamic
		self.value_var = value_var
		self.value_numeric = value_numeric
		self.value_bool = value_bool
		self.value_factor = value_factor
		self.value_date = value_date
		self.precision = precision
		self.disabled_var = disabled_var
		self.death_var = death_var
		self.death_time_var = death_time_var
		self.dependency_var = dependency_var
		self.dependency_original = dependency_original
		self.dependency_collected = dependency_collected
		self.dependency_results = dependency_results
		self.dependency_system = dependency_system
		return


def convert_to_date(date_string):
		if date_string is None:
				return None  # Возвращаем None, если строка пустая
		expected_formats = ["%d.%m.%Y %I:%M", "%d.%m.%Y"]  # Список ожидаемых форматов
		for date_format in expected_formats:
				try:
						date_object = datetime.strptime(date_string, date_format)
						return date_object # Возвращаем только дату без времени
				except ValueError:
						pass
		return None  # Если ни один формат не подходит


def handle_numbers(value):
	try:
		return float(value)
	except:
		if isinstance(value, str):
			if value[0] == '>':
				return float(value[1:]) + 0.001
			elif value[0] == '>':
				return float(value[1:]) - 0.001
			elif value[-1] == '%':
				return 1 * float(value[:-1])
			else:
				return None
		else:
			return value




# Открытые функции

def loadSheet(project: ProjectSetup, sheet_name: str):
	try:
		sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/' + project.book_id + '/gviz/tq?tqx=out:csv&headers=1&sheet=' + sheet_name)
		sheet = sheet.replace({np.nan: None, np.NaN: None, np.NAN: None})
		return sheet
	except:
		raise 'Лист ' + sheet_name + ' не загружен'

def loadVariables(project: ProjectSetup):
	raw = loadSheet(project, 'VARIABLES')

	# создаем факторные (категориальные в python) переменные
	factor_variables = ['DEPENDENCY_TYPE', 'VAR_TYPE', 'VALUE_TYPE', 'LIST_TYPE',]
	for var in factor_variables:
		if var not in raw: continue
		raw[var] = raw[var].astype('category')

	# обработка не-числовых данных, введенных в переменные с числовым/логическим типом
	numeric_variables = ['PRECISION', 'SORT',]
	for var in numeric_variables:
		if var not in raw: continue
		raw[var] = raw[var].apply(handle_numbers)

	return raw


def loadList(project: ProjectSetup, list_name: str):

	# Загрузка общего описания переменных
	variables = loadVariables(project)

	# Загрузка сырых данных
	raw = loadSheet(project, list_name)

	# Получаем настройки
	CONST = Constants()

	# Оставляем в датасете только валидные переменныее
	all_vars = variables[CONST.var].tolist()
	raw = raw.loc[:, raw.columns.isin(all_vars)]

	# создаем булевские значения
	bool_variables = variables[variables[CONST.value_var] == CONST.value_bool][CONST.var].tolist()
	for var in bool_variables:
		if var not in raw: continue
		raw[var] = raw[var].apply(lambda x: x in ['1', 'TRUE', True])

	# создаем факторные (категориальные в python) переменные
	factor_variables = variables[variables[CONST.value_var] == CONST.value_factor][CONST.var].tolist()
	for var in factor_variables:
		if var not in raw: continue
		raw[var] = raw[var].astype('category')

	# обработка дат, приводим в POSIX формат
	date_variables = variables[variables[CONST.value_var] == CONST.value_date][CONST.var].tolist()
	for var in date_variables:
		if var not in raw: continue
		raw[var + '_RAW'] = pd.to_datetime(raw[var], format='mixed', dayfirst=True)
		raw[var] = pd.to_datetime(raw[var], format='mixed', dayfirst=True)

	# обработка не-числовых данных, введенных в переменные с числовым/логическим типом
	numeric_variables = variables[variables[CONST.value_var] == CONST.value_numeric][CONST.var].tolist()
	for var in numeric_variables:
		if var not in raw: continue
		raw[var] = raw[var].apply(handle_numbers)

	return raw

def loadDynamic(
	project: ProjectSetup,
	include_dead = False,
):
	print('Загружаем проект:', project.name)

	# загрузка сырых данных
	variables = loadVariables(project)
	settings = loadSheet(project, 'SETTINGS')
	raw = loadSheet(project, 'DATA')

	# Получаем настройки
	CONST = Constants()
	SETTINGS = Settings()

	for key in SETTINGS.__dict__:
		p = settings[settings['SETTING'] == key]['VALUE']
		if len(p) == 0:
			print('В таблице SETTINGS не задан параметр:', key)
			continue
		SETTINGS.__dict__[key] = p.iloc[0]
	SETTINGS.observation_count = int(SETTINGS.observation_count)

	# Оставляем в датасете только валидные переменныее
	all_vars = variables[CONST.var].tolist()
	raw = raw.loc[:, raw.columns.isin(all_vars)]

	# Проверяем достаточность служебных переменных в исходнике
	system_vars = variables[variables[CONST.dependency_var] == CONST.dependency_system][CONST.var].tolist()
	for var in system_vars:
		if var not in raw:
			raise AttributeError('В таблице DATA не задан служебный параметр: ' + var)

	# интерполируем статику
	for var in variables[variables[CONST.type_var] == CONST.type_property][CONST.var]:
		if var not in raw: continue
		raw[var] = raw[var].ffill(limit=SETTINGS.observation_count - 1)

	# чистим данные
	variables = variables.loc[~variables[CONST.var].isnull()]
	raw = raw.loc[~raw[CONST.patient].isnull()]
	variables[CONST.precision] = variables[CONST.precision].fillna(0)

	# создаем булевские значения
	bool_variables = variables[variables[CONST.value_var] == CONST.value_bool][CONST.var].tolist()
	for var in bool_variables:
		if var not in raw: continue
		raw[var] = raw[var].apply(lambda x: x in ['1', 'TRUE', True])

	# исключение не подходящих
	if CONST.disabled_var in raw:
		print('Исключены:', raw[raw[CONST.disabled_var]][CONST.patient].unique())
		raw = raw[~raw[CONST.disabled_var]]

	# создаем факторные (категориальные в python) переменные
	factor_variables = variables[variables[CONST.value_var] == CONST.value_factor][CONST.var].tolist()
	for var in factor_variables:
		if var not in raw: continue
		raw[var] = raw[var].astype('category')

	# обработка дат, приводим в POSIX формат
	date_variables = variables[variables[CONST.value_var] == CONST.value_date][CONST.var].tolist()
	for var in date_variables:
		if var not in raw: continue
		raw[var + '_RAW'] = pd.to_datetime(raw[var], format='mixed', dayfirst=True)
		raw[var] = pd.to_datetime(raw[var], format='mixed', dayfirst=True)

	# обработка не-числовых данных, введенных в переменные с числовым/логическим типом
	numeric_variables = variables[variables[CONST.value_var] == CONST.value_numeric][CONST.var].tolist()
	for var in numeric_variables:
		if var not in raw: continue
		raw[var] = raw[var].apply(handle_numbers)

	# создаем DataFrame со всеми возможными комбинациями пациентов и точек времени
	all_combinations = pd.MultiIndex.from_product([raw[CONST.patient].unique(), raw[CONST.time].unique()],
												names=[CONST.patient, CONST.time]).to_frame(index=False)

	# объединяем все комбинации с исходными данными
	raw = pd.merge(all_combinations, raw, on=[CONST.patient, CONST.time], how='outer')

	# интерполируем динамику, сохраняем оригинальные значения с постфиксом " REAL"
	time_max = raw[CONST.time].max()
	for var in variables[(variables[CONST.type_var] == CONST.type_dynamic) & (variables[CONST.value_var].isin([CONST.value_numeric, CONST.value_bool]))][CONST.var]:
		if var not in raw: continue
		if pd.isnull(var): continue
		if var == CONST.time: continue
		raw[var + ' REAL'] = raw[var]
		interpolated_row = pd.Series(dtype='float64')
		for patient, patient_raw in raw.groupby(CONST.patient):
			if pd.isnull(patient): continue
			real_index = patient_raw.index
			patient_is_alive = not patient_raw[CONST.death_var].iloc[0]
			patient_var_series: pd.Series = patient_raw[[var, CONST.time]].copy().set_index(CONST.time)[var]
			patient_var_series = patient_var_series.interpolate(method='index', limit_area='inside', limit_direction='both')
			patient_var_series = patient_var_series.bfill(limit_area='outside')
			# locf
			if patient_is_alive or include_dead:
				# если жив - тянем-потянем. если включаем мертвых - тоже
				patient_var_series = patient_var_series.ffill(limit=SETTINGS.observation_count)
			else:
				# если мертв и после смерти locf не нужно, то нужно ограничение по моменту, когда он стал мёртвым
				death_time: float = patient_raw[CONST.death_time_var].iloc[0]
				if death_time <= time_max:
					# делаем ограничение по времени смерти
					patient_var_series.loc[:death_time].ffill(inplace=True)
				else:
					# случай, когда умер когда-то в будущем. тогда тянем до конца
					patient_var_series = patient_var_series.ffill(limit=SETTINGS.observation_count)
			patient_var_series.index = real_index
			interpolated_row = pd.concat([interpolated_row, patient_var_series])
		raw[var] = interpolated_row

	if project.output_path != '':
		os.makedirs(project.output_path, exist_ok=True)
		raw.to_excel(project.output_path + '\\' + project.output_name + ' ' + ('locf' if include_dead else 'alive_only') + '.xlsx', index=False)

	return raw
