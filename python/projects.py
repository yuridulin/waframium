class ProjectSetup:
	def __init__(self,
			book_id: str,
			name: str,
			output_path: str = 'output',
			output_name: str = 'raw') -> None:
		self.book_id = book_id
		self.name = name
		self.output_path = output_path
		self.output_name = output_name
		pass

P_21EF05 = ProjectSetup(
	book_id='1q72LTSMFnw-bmzL0uBD6BL8COYON_8j-b2Y-oWGTf4Y',
	name='Акушерский сепсис',
	output_path='output',
	output_name='21ef05'
)

P_22EF02 = ProjectSetup(
	book_id='11bzoeYUQ7C7_oh-ReZcDsWA5ysvMDW3lnn7nvpceSyw',
	name='ЛАССО НЕО',
	output_path='output',
	output_name='22ef02'
)

P_22EF03 = ProjectSetup(
	book_id='1WwR01IPwPyG0lGntmwziOF6RDM6j4cN_vfLCCELg4_M',
	name='Панкреатит Демихово',
	output_path='output',
	output_name='22ef03'
)

P_22EF08 = ProjectSetup(
	book_id='1sbHxUWF5f6ZKft-wthiQkutqOBEDcx1-bdBNQbwjkDM',
	name='Сепсис Юдина',
	output_path='output',
	output_name='22ef08'
)

P_23EF02 = ProjectSetup(
	book_id='13ijyiXgbhe3lzP01-mYpLX_XtArPAWLVfj_iuQsPCvc',
	name='ОП Краснодар',
	output_path='output',
	output_name='22ef03'
)

P_COVID = ProjectSetup(
	book_id='1aswkDS-MVHWJyLDUQJFD77TivM6obRtmGFvODyEk8Z0',
	name='Ковид-19',
	output_path='output',
	output_name='22ef03'
)

P_KZ = ProjectSetup(
	book_id='1eTu154W-7csLyXxfvQpJYNjvX5moEQZ-9imAkivCgS8',
	name='Казахстан',
	output_path='output',
	output_name='22ef03'
)