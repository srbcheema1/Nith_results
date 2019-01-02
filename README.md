# Nith results

## A commandline tool to check your result of last semester.

 * Requirements

   * requests
   * beautiful-soup


 * Steps to Use

   * Clone this repo using `git clone https://github.com/srbcheema1/Nith_results`.
   * Create virtual environment (optional) using `python3 -m venv env`. To activate the virtual environment, use `source env/bin/activate`, `deactivate` to deactivate.
   * Install the requirements using `pip3 install -r requirements.txt`.
   * Now run the command `python3 nith_results.py -h`.
   * Example `python3 nith_results.py -cydr 15mi535`.
   * OR you may also use `make` command.


 * Available stats

   * You can check out already calculated data in folder `data`.
   * Also you can find out `final_list.json` containing data for 3rd year students.


 * Available results

   * You can check out already downloaded results in `result` folder.
   * Results are organised in folders for each branch.
   * Folders contain results in `branch_name_xx_xgpi.txt`.
   * Also you can find out `full_year_xx_xgpi.txt` containing data for whole year.
