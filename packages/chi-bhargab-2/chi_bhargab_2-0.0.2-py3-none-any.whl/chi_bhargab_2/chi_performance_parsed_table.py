import pandas as pd
from scipy import stats
import math


class data_feed:
  def __init__(self,n,df,good_table,bad_table,column1, column2, column3):
        self.n=n
        self.df=df
        self.good_table=good_table
        self.bad_table=bad_table
        self.column1=column1
        self.column2=column2
        self.column3=column3
  def interpret(self):
        desc={}
      
        cat=self.df[self.column3].unique()

          
        desc[f'Associates Good in both']=list(pd.merge(self.good_table[cat[0]],self.good_table[cat[1]],on='Salesman_id')['Salesman_id'])
        desc[f'Associates Good in both']=list(pd.merge(self.bad_table[cat[0]],self.bad_table[cat[1]],on='Salesman_id')['Salesman_id'])
        desc[f'Associates Good in both Good in {cat[0]} but bad in {cat[1]}']=list(pd.merge(self.good_table[cat[0]],self.bad_table[cat[1]],on='Salesman_id')['Salesman_id'])
        desc[f'Associates Good in both Good in {cat[1]} but bad in {cat[0]}']=list(pd.merge(self.good_table[cat[1]],self.bad_table[cat[0]],on='Salesman_id')['Salesman_id'])
          
        desc[f'Top {self.n}% Associates Good in both in {cat[1]}']=list(self.good_table[cat[1]]['Salesman_id'].head(math.ceil(len(self.good_table[cat[1]])*(self.n/100))))
        desc[f'Top {self.n}% Associates Good in both in {cat[0]}']=list(self.good_table[cat[0]]['Salesman_id'].head(math.ceil(len(self.good_table[cat[0]])*(self.n/100))))
        desc[f'Bottom {self.n}% Associates Good in both in {cat[1]}']=list(self.bad_table[cat[1]]['Salesman_id'].head(math.ceil(len(self.bad_table[cat[1]])*(self.n/100))))
        desc[f'Bottom {self.n}% Associates Good in both in {cat[0]}']=list(self.bad_table[cat[0]]['Salesman_id'].head(math.ceil(len(self.bad_table[cat[0]])*(self.n/100))))
         
        return desc

  def output_table(self):
    parsed_tbl={}
          
    for val in self.df[self.column3].unique():
      parsed_tbl[f'good performers {val}']=self.good_table[val].to_json(orient="split")
      parsed_tbl[f'bad performers {val}']=self.bad_table[val].to_json(orient="split")

    return parsed_tbl