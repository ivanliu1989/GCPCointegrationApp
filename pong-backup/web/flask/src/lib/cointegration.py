import statsmodels.api as sm
import statsmodels.tsa.stattools as ts

def adftest(df):
    

    df[df.columns[0]] = df[df.columns[0]].fillna(0)
    df[df.columns[1]] = df[df.columns[1]].fillna(0)
    # Calculate optimal hedge ratio "beta"
    # Ordinary Least Squares (OLS) regression
    res = sm.OLS(df[df.columns[0]], df[df.columns[1]])
    res = res.fit()
    beta_hr = res.params[df.columns[1]]

    # Calculate the residuals of the linear combination
    df["res"] = df[df.columns[0]] - beta_hr*df[df.columns[1]]

    #Cointegrated Augmented Dickey-Fuller Test
    adf,pvalue,usedlag,nobs,criticalvalues,icbest = ts.adfuller(df["res"])
    return pvalue
