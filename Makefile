RESULT_SCRIPT=python3 nith_result.py -cydr

all: year_1 year_2 year_3 year_4

year_1:
	$(RESULT_SCRIPT) 17mi535
	echo "done year_1"

year_2:
	$(RESULT_SCRIPT) 16mi535
	echo "done year_2"

year_3:
	$(RESULT_SCRIPT) 15mi535
	echo "done year_3"

year_4:
	$(RESULT_SCRIPT) 14mi535
	echo "done year_4"
