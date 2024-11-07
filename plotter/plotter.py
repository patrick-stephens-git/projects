## Import Module Requirements:
import matplotlib.pyplot as plt
import pandas as pd

## Import Variables via Files from Directory:
from configurationVariables import input_csv_filename, ctrl_grp_name, test_grp_name

###################
# Function Library:
def get_ctrl_vs_test_cumulative_impact(df, ctrl_grp_name, test_grp_name):
    #################################
    # Get Cumulative Impact Calculation of Core Metrics for Plotting:
    cumsum_df = pd.DataFrame()
    cumsum_df['{0} cumImpact'.format(ctrl_grp_name)] = df['{0}'.format(ctrl_grp_name)].cumsum()
    cumsum_df['{0} cumImpact'.format(test_grp_name)] = df['{0}'.format(test_grp_name)].cumsum()
    cumsum_df['{0} vs {1} cumImpact'.format(test_grp_name, ctrl_grp_name)] = (cumsum_df['{0} cumImpact'.format(test_grp_name)] / cumsum_df['{0} cumImpact'.format(ctrl_grp_name)]) - 1
    # print(core_test_metrics_cumsum_df)
    df['{0} vs {1} cumImpact'.format(test_grp_name, ctrl_grp_name)] = cumsum_df['{0} vs {1} cumImpact'.format(test_grp_name, ctrl_grp_name)]
    return df

df = pd.read_csv('{0}'.format(input_csv_filename), names=['date','{0}'.format(ctrl_grp_name),'{0}'.format(test_grp_name)], header=None)
df = get_ctrl_vs_test_cumulative_impact(df, ctrl_grp_name, test_grp_name)

## Resize Plot:
plt.rcParams['figure.figsize'] = [15, 5] 

## Plot Settings
axis = plt.gca() # gca = get current axis
axis2 = axis.twinx()

## Series in Plot - Axis1:
df.plot(kind='line', 
        x='date', 
        y='{0}'.format(test_grp_name),
        linewidth = 2,
        ax = axis)

## Series in Plot - Axis1:
df.plot(kind='line', 
        x='date', 
        y='{0}'.format(ctrl_grp_name),
        linewidth = 2,
        ax = axis)

## Series in Plot - Axis2:
df.plot(kind='line', 
        x='date', 
        y='{0} vs {1} cumImpact'.format(test_grp_name, ctrl_grp_name),
        color = 'red',
        linewidth = 3,
        dashes = [3,3,2,2],
        ax = axis2)

## Plot Grid:
axis2.grid(True)
## Set Plot Legend:
axis.legend(bbox_to_anchor=(0.05, 0), loc='upper left', borderaxespad=0.)
axis2.legend(bbox_to_anchor=(0.05, 0), loc='lower left', borderaxespad=0.)
## Disable Scientific Notation:
axis.ticklabel_format(style='plain', axis='y')
axis2.ticklabel_format(style='plain', axis='y')
## Title of Plot:
plt.title('Test Group vs Ctrl Group')
## Y Axis Labels:
axis.set_ylabel('Metric')
axis2.set_ylabel('(Cumulative Impact)')
## Set Cumulative Impact Axis Set "0" at Middle (for Axix2):
yabs_max = abs(max(axis.get_ylim(), key=abs))
axis.set_ylim(ymin=-yabs_max, ymax=yabs_max)
yabs_max = abs(max(axis2.get_ylim(), key=abs))
axis2.set_ylim(ymin=-yabs_max, ymax=yabs_max)
axis2.axhline(0, color='black')
## Display Plot:
plt.savefig('plot.png') # Uncomment to save a .png image of the plot
# plt.close()
# plt.cla()
# plt.clf()
plt.show()


