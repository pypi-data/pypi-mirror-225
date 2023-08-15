import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CSV:
    def __init__(self, file):
        self.path = os.path.dirname(os.path.abspath(file))
        self.df = pd.read_csv(file)
        self.columns = self.df.select_dtypes(include=float).columns
#         print(self.df.info())
        
    def report(self):
        return self.df.describe(percentiles=[0.1,0.25,0.5,0.75,0.9]).transpose()
    
    def show(self, col=''):
        if col: self.df[col].plot(figsize=(5,3),title=col)
        else:
            cols = self.df.select_dtypes(include=float).columns
            self.df.plot(
                subplots=True,
                figsize=(5,len(cols)*3),
                title=cols.tolist()
            )
           
    def show2d(self, col1='', col2=''):
        if not col1 or not col2: raise ValueError('Need 2 columns to form 2d figure')
        df1 = self.df[col1]
        df2 = self.df[col2]
        vmax = int(max(max(df1),max(df2))//50+1)*50
        plt.hist2d(df1, df2, bins=100, vmax=vmax, cmap='gray')
        plt.colorbar()
        plt.savefig('test.png')

    def save_graph(self):
        cols = self.columns
        for i,col in enumerate(cols):
            fig = self.df[col].plot(figsize=(5,3),title=col).get_figure()
            fig.savefig(os.path.join(self.path,f'figure_{i+1:02d}.png'))
            plt.close(fig)
    
    def set_range(self, col, mini=np.nan, maxi=np.nan):
        if mini is np.nan or maxi is np.nan:
            return 'please give a exact range to set the range of data'
        for idx, value in enumerate(self.df[col]):
            if value > maxi:
                self[idx,col] = maxi
                continue
            if value < mini:
                self[idx,col] = mini
                continue
    
    def __getitem__(self, index):
        return self.df.at[index]
    
    def __setitem__(self, index, value):
        self.df.at[index] = value