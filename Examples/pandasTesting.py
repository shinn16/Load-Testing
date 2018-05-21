# @author Patrick Shinn
# @version 5/21/18

from pandas import read_csv
from matplotlib import pyplot as plt

# reading in the data
df = read_csv("/home/patrick/Github/research/Load-Testing/LoadTest/n1/linux_bare/test1/Driver-2017-07-19_16:15:26.csv",
              sep='\t')
print(type(df))    # shows that df is a pandas data frame
print(df.head(5))  # prints the first 5 entries
print(df.dtypes)   # prints data types of columns

df.reset_index().plot(y=" write_bytes", x="index")
plt.show()
