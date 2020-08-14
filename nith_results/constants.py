# set base_year as year of 1st year students
from srblib import SrbJson
from srblib import debug, on_travis


cache_path = '~/.config/nith_results/cache.json'

_limits_template = \
{
	'base_year' : None,
	'default_no_of_std' : 99,
	'dual_no_of_std' : 70,
	'max_seats' : 120,
	'base_url': ""
}

_limits = SrbJson('~/.config/nith_results/limits.json',_limits_template)

base_year = _limits['base_year'] # it can be None
base_url = _limits['base_url']
if(not base_year):
	if on_travis: base_year = 19
	else: base_year = int(input('Please enter base-year(year of 1st year student right now) ex:19 '))
	_limits['base_year'] = base_year

if(base_url == ""):
	if on_travis: base_url = "14.139.56.15"
	else: base_url = str(input('Please enter base-url(url in portal) ex: 14.139.56.15 '))
	_limits['base_url'] = base_url

base_year = int(_limits['base_year'])
default_no_of_std = int(_limits['default_no_of_std'])
dual_no_of_std = int(_limits['dual_no_of_std'])
max_seats = int(_limits['max_seats'])

if (debug):
	default_no_of_std = 4
	dual_no_of_std = 6
	max_seats = 4

def get_branch_set(roll):
	def get_batch(roll): # working with new one
		roll = str(roll)
		year = roll[0:2]
		return year
	y = get_batch(roll)
	if(int(y) >= 18): # new style
		return [
			y+'1001',y+'2001',y+'3001',y+'4001',y+'5001',y+'6001',y+'7001',y+'8001',
			y+'4501',y+'5501',
		]

	classes_set = {
			"14":[
				y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',
				y+'mi501',y+'mi401',
				],
			"15":[
				y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',
				y+'mi501',y+'mi401',
				],
			"16":[
				y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',
				y+'mi501',y+'mi401',
				],
			"17":[
				y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',y+'801',
				y+'mi501',y+'mi401',
				],
			}
	return classes_set[y]

def get_branch_set_mtech(roll):
	def get_batch(roll): # working with new one
		roll = str(roll)
		year = roll[0:2]
		return year
	y = get_batch(roll)
	if(int(y) >= 18): # new style
		return [
			y+'4501',y+'5501'
		]

	if(int(y)>=15):
		return [
			y+'mi501',y+'mi401'
		]

	return []
