import pandas as pd
import ipywidgets as widgets
import src
from IPython.display import clear_output
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.stats as sts

    

def show_tasks_dropdown(dropdown,df=src.get_raw_data()):
    
    display(dropdown)

    def dropdown_eventhandler(change):
        clear_output()
        display(dropdown)

        if change.new == "1. Checking the number of mice":
            df = src.get_raw_data()
            numMice = len(set(df["Mouse ID"]))
            display("Number of mice => " + str(numMice))
        elif change.new == "2. Generate a  summary table":
            display(generate_a_summary_table())
        elif change.new == "3a. Generate a plot using Panda's dataframe .plot() that shows the total mice for each treatment regimen":
            drug_grp = src.get_last_instance_data().groupby(by="Drug Regimen")
            display(
                drug_grp['Mouse ID'].count().plot(kind="bar", title="Total mice for each treatment regimen")
            )
        elif change.new == "3b. Generate a plot using Matplotlib's pyplot that shows the total mice for each treatment regimen":
            drug_grp = src.get_last_instance_data().groupby(by="Drug Regimen")
            plt.bar(drug_grp.groups.keys(),drug_grp['Mouse ID'].count())
            plt.xticks(rotation=45)
            plt.title("Total mice for each treatment regimen")
            display()    
        elif change.new == "4a. Generate a pie plot using Panda's dataframe .plot() that shows the distribution of female or male mice in the study":
            drug_grp = src.get_last_instance_data().groupby(by="Sex")
            display(
                drug_grp['Mouse ID'].count().plot(kind='pie', title="Distribution of female or male mice in the study")
            )
        elif change.new == "4b. Generate a pie plot using Matplotlib's pyplot that shows the distribution of female or male mice in the study":
            drug_grp = src.get_last_instance_data().groupby(by="Sex")
            plt.pie(drug_grp['Mouse ID'].count(),labels=drug_grp.groups.keys(),explode = [0,0.2],shadow=True, startangle=-30)
            plt.title("Distribution of female or male mice in the study")
            display()
        elif change.new == "5a. Calculate the final tumor volume of each mouse across four of the most promising treatment regimens: Capomulin, Ramicane, Infubinol, and Ceftamin":
            df = src.get_four_promising_treatments()
            display(df)
        elif change.new == "6a. Calculate the quartiles and IQR and quantitatively determine if there are any potential outliers across all four treatment regimens.":
            df = src.get_four_promising_treatments()
            [Q1, Q3] = sts.mstats.idealfourths(df['Final Tumor Volume (mm3)'])
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            filt = ((df['Final Tumor Volume (mm3)']<lower_bound)|(df['Final Tumor Volume (mm3)']>upper_bound))
            print(df['Final Tumor Volume (mm3)'][filt])

            plt.hist(df['Final Tumor Volume (mm3)'],color="grey",label="histogram of 4 treatment group's final tumor volume",alpha=0.5)
            plt.axvline(x=Q1,ymax=20,label=f"Q1: {Q1:.1f}",color='black')
            plt.axvline(x=Q3,ymax=20,label=f"Q3: {Q3:.1f}",color='black')
            plt.hlines(y=2.5,xmin=Q1,xmax=Q3,label=f"IQR: {IQR:.1f}",color='orange')
            plt.axvline(x=lower_bound,ymax=20,label=f"lower_bound: {lower_bound:.1f}",color='blue')
            plt.axvline(x=upper_bound,ymax=20,label=f"upper_bound: {upper_bound:.1f}",color='red')
            plt.legend()
            plt.show()

            display(
                pd.DataFrame({
                    "LowerB": [lower_bound],
                    "Min" : [df['Final Tumor Volume (mm3)'].min()],
                    "Q1" : [Q1],
                    "Median" : [df['Final Tumor Volume (mm3)'].median()],
                    "Q3" : [Q3],
                    "Max" : [df['Final Tumor Volume (mm3)'].max()],
                    "UpperB" : [upper_bound]
                }).style.format({"LowerB":"{:.1f}",
                                "Min":"{:.1f}",
                                "Q1":"{:.1f}",
                                "Median":"{:.1f}",
                                "Q3":"{:.1f}",
                                "Max":"{:.1f}",
                                "UpperB": "{:.1f}"})
            )
        elif change.new == "6b. Using Matplotlib, generate a box and whisker plot of the final tumor volume for all four treatment regimens and highlight any potential outliers in the plot by changing their color and style.":
            exercise6b()
            display()
        elif change.new == "7. Select a mouse that was treated with Capomulin and generate a line plot of time point versus tumor volume for that mouse.":
            df = src.get_raw_data()
            filt = df["Drug Regimen"] == "Capomulin"
            mouse = df[filt].iloc[0,:]["Mouse ID"]
            filt = df["Mouse ID"] == mouse
            mouse_data = df[filt][["Timepoint","Tumor Volume (mm3)"]].set_index("Timepoint")

            plt.plot(mouse_data)
            plt.title(f"Capomulin treated mouse '{mouse}' data: Tumor volume over time")
            plt.xlabel("Timepoint")
            plt.ylim(0,50)
            plt.ylabel("Tumor size (mm3)")
            plt.show()
            display()
        elif change.new == "8. Generate a scatter plot of mouse weight versus average tumor volume for the Capomulin treatment regimen.":
            df = src.get_mouse_metadata()
            filt = df["Drug Regimen"] == "Capomulin"
            df_weight = df[filt][["Mouse ID", "Weight (g)"]]

            df = src.get_raw_data()
            filt = df["Drug Regimen"] == "Capomulin"
            df = df[filt][['Mouse ID',"Tumor Volume (mm3)"]]
            df_avg_tumor_volume = df.groupby(by="Mouse ID").mean()
            df = df_weight.merge(df_avg_tumor_volume,on="Mouse ID",how='left')

            plt.scatter(df['Tumor Volume (mm3)'],df["Weight (g)"])
            plt.ylabel("Mouse Weight (g)")
            plt.xlabel("Average tumor volume (mm3)")
            plt.xlim(34,47)
            plt.ylim(10,28)
            plt.show()
            display()
        elif change.new == "9. Calculate the correlation coefficient and linear regression model between mouse weight and average tumor volume for the Capomulin treatment. Plot the linear regression model on top of the previous scatter plot.":
            exercise9()
            display()
        elif change.new == "10a. Observation 1":
            print("Observation 1: Rat tumor size correlates with mouse weight, and it's statistically signficant")
            exercise9()
            display()
        elif change.new == "10b. Observation 2":
            print("Observation 2: Capomulin and Ramicane were the only treatments that on average decreased tumor size.")
            display(generate_a_summary_table())
        elif change.new == "10c. Observation 3":
            print("Mouse c326 was an outlier in the Infubinol group. It looks like it's last timepoint was 5.. Did the mouse die?")
            exercise6b()
            df = src.get_last_instance_data()
            filt = df["Drug Regimen"]=="Infubinol"
            df = df[filt].rename(columns={"Tumor Volume (mm3)":"Final Tumor Volume (mm3)"})
            
            display(df.loc[669])
    dropdown.observe(dropdown_eventhandler, names='value')

def exercise6b():
    df = src.get_four_promising_treatments()
    grp_names = ["Capomulin", "Ramicane", "Infubinol", "Ceftamin"]
    grps = [df.groupby(by="Drug Regimen").get_group(grp_name).reset_index()['Final Tumor Volume (mm3)'].rename(grp_name) for grp_name in grp_names] 

    fig, ax = plt.subplots()
    plt.boxplot(grps,labels=grp_names,sym='ob')
    ax.set_title("Box and whisker plot for 4 promising treatments")
    plt.show()

def exercise9():
                df = src.get_mouse_metadata()
                filt = df["Drug Regimen"] == "Capomulin"
                df_weight = df[filt][["Mouse ID", "Weight (g)"]]

                df = src.get_raw_data()
                filt = df["Drug Regimen"] == "Capomulin"
                df = df[filt][['Mouse ID',"Tumor Volume (mm3)"]]
                df_avg_tumor_volume = df.groupby(by="Mouse ID").mean()
                df = df_weight.merge(df_avg_tumor_volume,on="Mouse ID",how='left')

                x = df['Tumor Volume (mm3)']
                y = df["Weight (g)"]

                plt.scatter(x,y)
                plt.ylabel("Mouse Weight (g)")
                plt.xlabel("Average tumor volume (mm3)")
                plt.xlim(34,47)
                plt.ylim(10,28)

                import numpy as np
                from scipy.stats.stats import pearsonr
                from scipy.stats import linregress
                plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
                plt.annotate(f"R = {pearsonr(x,y)[0]:.2f}\nslope = {linregress(x,y)[0]:.2f}\np-value = {pearsonr(x,y)[1]:.7f}",(36,24))
                plt.show()

def generate_a_summary_table():
    # Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen
    df = src.get_raw_data()
    drug_regimens = df['Drug Regimen'].unique().tolist()
    df_first = df.drop_duplicates('Mouse ID',keep='first') 
    df_last = df.drop_duplicates('Mouse ID',keep='last')
    drug_grp = df_last.groupby(by="Drug Regimen")

    np.set_printoptions()

    summary_df = pd.DataFrame({
    "Drug Regimen" : drug_regimens,
    "Starting Volume" : df_first.groupby(by="Drug Regimen").mean()["Tumor Volume (mm3)"],
    "Mean" : drug_grp['Tumor Volume (mm3)'].mean(),
    "Median" : drug_grp['Tumor Volume (mm3)'].median(),
    "Variance" : drug_grp['Tumor Volume (mm3)'].var(),
    "Standard Deviation" : drug_grp['Tumor Volume (mm3)'].std(),
    "SEM" : drug_grp['Tumor Volume (mm3)'].sem()
    })

    summary_df.insert(3,"% Change",(summary_df["Mean"]-summary_df["Starting Volume"])/summary_df["Mean"]*100)

    styler = summary_df.style.background_gradient(cmap=cm.get_cmap('coolwarm', 12),subset=['% Change'])
    styler.format({'Starting Volume': "{:.1f}", 'Mean': "{:.1f}", '% Change': "{:.1f}%", 'Median': "{:.1f}", 'Variance': "{:.1f}", 'Standard Deviation': "{:.2f}", 'SEM': "{:.2f}"})    

    return styler