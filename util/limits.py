# set base_year as year of 1st year students
from srblib import SrbJson
from srblib import debug

_limits_template = \
{
    'base_year' : 18,
    'default_no_of_std' : 99,
    'iiitu_no_of_std' : 60,
    'dual_no_of_std' : 65,
}

_limits = SrbJson('~/.config/nith_results/limits.json',_limits_template)

base_year = _limits['base_year']
default_no_of_std = _limits['default_no_of_std']
iiitu_no_of_std = _limits['iiitu_no_of_std']
dual_no_of_std = _limits['dual_no_of_std']

if (debug):
    default_no_of_std = 4
    iiitu_no_of_std = 4
    dual_no_of_std = 6

def get_class_set(y):
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
                    ]
            }
    return classes_set[y]
