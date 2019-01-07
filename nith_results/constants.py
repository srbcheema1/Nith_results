# set base_year as year of 1st year students
from srblib import SrbJson
from srblib import debug, on_travis


cache_path = '~/.config/nith_results/cache.json'

_limits_template = \
{
    'base_year' : None,
    'default_no_of_std' : 99,
    'iiitu_no_of_std' : 70,
    'dual_no_of_std' : 70,
    'max_seats' : 120,
}

_limits = SrbJson('~/.config/nith_results/limits.json',_limits_template)

base_year = _limits['base_year']
if(not base_year):
    if on_travis: base_year = 18
    else: base_year = input('Please enter base-year(year of 1st year student right now) ex:18 ')
    _limits['base_year'] = base_year

default_no_of_std = _limits['default_no_of_std']
iiitu_no_of_std = _limits['iiitu_no_of_std']
dual_no_of_std = _limits['dual_no_of_std']
max_seats = _limits['max_seats']

if (debug):
    default_no_of_std = 4
    iiitu_no_of_std = 4
    dual_no_of_std = 6
    max_seats = 4

def get_branch_set(roll):
    def get_batch(roll): # working with new one
        roll = str(roll)
        if(roll[0]=='i'):#iitu
            year = roll[5:7]
        else:
            year = roll[0:2]
        return year
    y = get_batch(roll)
    if(int(y) >= 18): # new style
        return [
            y+'1001',y+'2001',y+'3001',y+'4001',y+'5001',y+'6001',y+'7001',y+'8001',
            y+'4501',y+'5501',
            'iiitu'+y+'101','iiitu'+y+'201','iiitu'+y+'301'
        ]

    classes_set = {
            "14":[
                y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',
                y+'mi501',y+'mi401',
                'iiitu'+y+'101','iiitu'+y+'201'
                ],
            "15":[
                y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',
                y+'mi501',y+'mi401',
                'iiitu'+y+'101','iiitu'+y+'201'
                ],
            "16":[
                y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',
                y+'mi501',y+'mi401',
                'iiitu'+y+'101','iiitu'+y+'201'
                ],
            "17":[
                y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',y+'801',
                y+'mi501',y+'mi401',
                'iiitu'+y+'101','iiitu'+y+'201','iiitu'+y+'301'
                ],
            }
    return classes_set[y]
