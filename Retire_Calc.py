

class retire():
    
    def __init__(self, age, retirement_year, cash, stocks, bonds, gender):
            self.age = age
            self.retirement_year = retirement_year
            self.cash = cash
            self.stocks = stocks
            self.bonds = bonds
            self.gender = gender

    def check_values(self):

        # Value Checks
        try:
            self.age = int(self.age)
            self.retirement_year = int(self.retirement_year) - (int(self.retirement_year) % 5)
            self.cash = int(self.cash)
            self.stocks = int(self.stocks)
            self.bonds = int(self.bonds)

        except:
            return "You've probably entered a character. Please confirm you only input numbers."



        # Age Checks
        if self.age <= 0:
            return "You put in an age less than 0. Please enter your age."
        elif self.age > 65:
            return "You should consult with a financial advisor about being a senior citizen saving for retirement"
        elif (self.retirement_year < 2025) | (self.retirement_year > 2070):
            return "Please enter a year between 2025 and 2070."

        # Making sure no money is negetive
        if self.cash < 0:
            return "Please enter a positive value for cash."
        elif self.stocks < 0:
            return "Please enter a positve value for stocks."
        elif self.bonds < 0:
            return "Please enter a positive value for bonds."
        else:
            return True

    def calc_death(self):
        import pandas as pd
        import matplotlib.pyplot as plt
        from datetime import date
        import os
        import sys

        os.chdir(sys._MEIPASS)
        death_csv= 'data\\life_expect.csv'


        deaths = pd.read_csv(death_csv)
        deaths['Death'] = deaths['Death'] * 100
        deaths['exp'] = deaths['age'] + deaths['Life']
        deaths = deaths.astype({'Death':int, 'exp':int})

        deaths_filtered = deaths[(deaths['Gender'] == self.gender) & (deaths['age'] == self.age)].reset_index(drop = True)

        self.return_death_age = deaths_filtered.at[0, 'exp']
        self.return_death_perc = deaths_filtered.at[0, 'Death']
        
        self.return_years_to_death = self.return_death_age - self.age
        self.death_year = (date.today().year) + self.return_years_to_death

        female_deaths = deaths[deaths['Gender'] == "Female"]
        male_deaths = deaths[deaths['Gender'] == "Male"]

        death_fig = plt.figure()
        plt.plot(female_deaths['age'], female_deaths['Death'], color = 'green', label = "Female Death Chance")
        plt.plot(male_deaths['age'], male_deaths['Death'], color = 'blue', label = "Male Death Chance")
        plt.xlabel("Current Age")
        plt.ylabel("Percent Chance of Death this Year")
        plt.plot(self.age, self.return_death_perc, color = 'red', marker = 'o', label = "Your Percent Chance of Death This Year")
        plt.legend(loc = 'upper center', bbox_to_anchor = (.5, -.13), framealpha = 1)
        plt.subplots_adjust(bottom = .25, left = .15, top = .95)

        return self.return_death_age, self.return_death_perc, self.return_years_to_death, plt.gcf()

    def retire_calc(self):
        import pandas as pd
        import numpy as np
        from datetime import date
        import matplotlib.pyplot as plt
        import os
        import sys

        os.chdir(sys._MEIPASS)
        asset_csv= 'data\\asset_allocation.csv'
        

        assets = [self.bonds, self.stocks, self.cash]
        col_names = ['Fixed Income', 'Equity', 'Cash']

        retirement = pd.read_csv(asset_csv)

        retirement_summary = pd.DataFrame(retirement.groupby('Asset Type')[str(self.retirement_year)].sum())

        #print(retirement_summary)
        
        total_assets = (self.bonds + self.stocks + self.cash)
        perc_assets = [((x/total_assets) * 100) for x in assets]
        years_after_retirement = self.death_year - self.retirement_year
        years_till_retirement = self.retirement_year - int(date.today().year)

        perc_df = pd.DataFrame(data = list(zip(perc_assets, col_names)), columns = ['perc', 'asset'])

        y_axis = np.arange(len(col_names))

        asset_dist = plt.figure()
        plt.barh(y = y_axis + .2, width = retirement_summary[str(self.retirement_year)], height = .4, label = "Optimal Strategy")
        plt.barh(y = y_axis - .2, width = perc_df['perc'], height = .4, label = "Current Strategy")
        plt.yticks(y_axis, retirement_summary.index, rotation = 45)
        plt.xlabel("Percent of Portfolio")
        plt.subplots_adjust(bottom = .23, left = .17)
        plt.legend(loc = 'lower right')
        

        retirement_melt = retirement.melt(id_vars = ['Asset Type', 'Asset'], var_name = "Year", value_name = "perc")
        retirement_melt['holder'] = int(date.today().year)
        retirement_melt = retirement_melt.astype({"Year":int})
        retirement_melt['yrs_to_retire'] = retirement_melt["Year"] - retirement_melt['holder']
        retirement_melt = retirement_melt.drop(labels = 'holder', axis = 1)
        
        
        retirement_melt.groupby('Year').cumsum()

        #glideslope = plt.figure()
        glideslope, ax = plt.subplots()

        retirement_melt.set_index('yrs_to_retire', inplace=True)
        retirement_melt.sort_values(by=["Year", "Asset"])

        retirement_melt['cumsum'] = retirement_melt.groupby('Year')['perc'].cumsum()

        for label, df in retirement_melt.groupby(['Asset']):
            df['cumsum'].plot(kind = 'line', ax = ax, label = label)
            #plt.fill_between(df.index, df['cumsum'])

        plt.ylabel("Allocation %")
        plt.xlabel("Years Until Retirement")
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':9})
        plt.subplots_adjust(bottom = .3, right = .6, top = .9)
        ax.invert_xaxis()
        plt.vlines(years_till_retirement, ymin = 0, ymax = 100, color = 'red')



        return years_after_retirement, years_till_retirement, asset_dist, glideslope