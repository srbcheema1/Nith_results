# set base_year as year of 1st year students
base_year = 17
debug = False

default_no_of_std = 99
iiitu_no_of_std = 60
dual_no_of_std = 65

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
                    y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',y+'801'
                    y+'mi501',y+'mi401',
                    'iiitu'+y+'101','iiitu'+y+'201','iiitu'+y+'301'
                    ]
            }
    return classes_set[y]
