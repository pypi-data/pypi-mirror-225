import pandas as pd
from scipy import stats

class test:
    def __init__(self,df,column_name,column_name1,column_name2):
        self.df = df
        self.column_name=column_name
        self.column_name1=column_name1
        self.column_name2=column_name2

    def result(self):
        final_tbl_good_performer={}
        final_tbl_bad_performer={}
        for i in self.df[self.column_name2].unique():
            tables= pd.crosstab(self.df.loc[self.df[self.column_name2]==i][self.column_name], self.df.loc[self.df[self.column_name2]==i][self.column_name1])
            tables.rename(columns={0: 'unfulfiled', 1: 'fulfiled'}, inplace=True)

            stat, p, dof, expected = stats.chi2_contingency(tables)
            exp_tbl = pd.DataFrame(expected)
            exp_tbl.rename(columns={0: 'unfulfiled', 1: 'fulfiled'}, inplace=True)
            exp_tbl.index=tables.index
            
            
            
            final_tbl=pd.DataFrame(index=tables.index)
            final_tbl["Salesman_id"] = tables.index
            #final_tbl.index=table.index
            final_tbl["Actual unfulfiled"] = tables["unfulfiled"]
            final_tbl["Actual fulfiled"] = tables["fulfiled"]
            final_tbl["Expected fulfiled"] = exp_tbl["fulfiled"]
            final_tbl["Chi_fulfiled"] = (((final_tbl["Actual fulfiled"] - final_tbl["Expected fulfiled"]) ** 2) / final_tbl["Expected fulfiled"]) 
            final_tbl["sale_percentage"] = (final_tbl["Actual fulfiled"] / (final_tbl["Actual fulfiled"] + final_tbl["Actual unfulfiled"])) * 100

            final_tbl_good_performer[i]=final_tbl[final_tbl["Actual fulfiled"]>final_tbl["Expected fulfiled"]].sort_values("Chi_fulfiled",ascending=False,)
            final_tbl_bad_performer[i]=final_tbl.drop(final_tbl_good_performer[i].index)
            final_tbl_bad_performer[i].sort_values("Chi_fulfiled",ascending=False,inplace=True)
        return final_tbl_good_performer,final_tbl_bad_performer #returns good performers and bad performers on the two market types: rural and urban
        