import requests,os,pandas as pd

class apicall:
    def __init__(self,baselink,headers):
        self.baselink=baselink
        self.headers=headers
    def list(self,endpoint):
        final_d=[]
        for i in range(5):
           print('url: ', baselink+endpoint)
           response=requests.get(baselink+endpoint, headers= headers)
           r_data=response.json()
           data=r_data['data']
           final_d.extend(data)
           endpoint=r_data['next']
        return final_d
    
    def dataframe(Self,json):
        df=pd.json_normalize(json)
        return df

baselink = "https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws"
endpoint = "/mentorskool/v1/sales?offset=0&limit=100"
headers={"access_token" : "fe66583bfe5185048c66571293e0d358"}

apiobj=apicall(baselink=baselink,headers=headers)
data=apiobj.list(endpoint=endpoint)

Ddf=apiobj.dataframe(json=data)
Ddf.head()

cleaned_columns=[x if(len(x.split('.'))==1) else x.split('.')[-1] for x in Ddf.columns]
Ddf.columns=cleaned_columns

class orders:
    def __init__(self,df):
        self.df=Ddf
    def total_amt(self,order_id):
        return self.df[self.df["order_id"]==order_id]["sales_amt"].sum().round(2)
order=orders(Ddf)
idamt=order.total_amt("US-2014-106992")
print(idamt)

class discount(orders):
    def __init__(self,df):
        super().__init__(df)
    def new_total(self,order_id):
        self.df=self.df.assign(
            new_sales_amt= lambda x: x["sales_amt"]*(1-x["discount"])
        )
        new_df=self.df[self.df["order_id"]==order_id]
        return new_df["new_sales_amt"].sum().round(2)
amt=discount(Ddf)
amt2=amt.new_total(order_id="CA-2017-100111")
print(amt2)