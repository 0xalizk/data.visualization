## Massively parallel data analysis and visualization

The code in `crunchNplot` follows a master-slaves model whereby the master loads a config file describing the task at hand (e.g. where the raw data is, plotting parameters etc) and fires up the required number of workers to each work on a certain subplot. Ultimately the result is one or more PNG files each with >=1 subplots.

The workers can be fired up on seperate cores on a single machine or seperate nodes in a HPC (grid computing) environment using MPI.

## Example outputs

Typical output would a number of PNG files containing a dynamic number (specified in configs.txt) of subplots. Example subplots are below (if you just want to adopt the look and feel of these example subplots, click on it to see example code, tweak the corresponding configs.txt as desired):

|||
|:---:|:---:|
|<img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/one/wheel.png" alt="Pie" height="150"> | <img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/one/scatter.png" alt="Scatter" height="150"> |
|<img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/one/bars_single.png" alt="Single bars" height="150"> | <img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/one/bars_groups.png" alt="Grouped bars" height="150"> |
|||
|<img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/two/bars_with_text.png" alt="Pie" height="150"> | <img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/two/gradient_with_math_and_tex.png" alt="Scatter" height="150"> |
|<img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/two/degdist_bars.png" alt="Single bars" height="150"> | <img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/two/group_subplots.png" alt="Grouped bars" height="150"> |
|||
|<img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/two/log_dot.png" alt="Pie" height="150"> | <img src="https://raw.githubusercontent.com/aliatiia/data.visualization/master/thumbs/two/nested_groups.png" alt="Scatter" height="150"> |



## Usage

If you run massively parallel simulations that needs to be followed by data analysis / visualization, follow the instructions under crunchNplot/ directory. This is worth if:
1. You continously run HPC simulations and want to add an auto data crunching / visualization step at the end of each simulation job.
2. You do not want to tweak matplotlib parameters after every simulation in order to get a decent looking subplot file (e.g. not wanting to adjust font size every time the number of subplots in the figure increases or decreases).

If you just have data and want to get subplots similar to the examples above, see the Examples/ directory, you should be able to get going just by editing the `configs.txt` file
