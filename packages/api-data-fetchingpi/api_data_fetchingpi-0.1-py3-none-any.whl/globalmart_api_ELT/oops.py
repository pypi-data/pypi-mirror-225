
import pandas as pd
import requests


class fetchapi:
    def __init__(self, base_url,end_point,access_token):
        self.base_url = base_url
        self.end_point=end_point
        self.access_token = access_token
    def get_api(self):
        final_data = []
        headers =  {'access_token':self.access_token}
        final_list=[]
        for i in range(5):
            try:
                response = requests.get(self.base_url+self.end_point,headers=headers)
                response_data = response.json()
                data=response_data['data']
                final_list.extend(data)
                end_point= response_data['next']
                self.end_point=end_point
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTPError:",{http_err})
            except Exception as err:
                print(f"Error:", {err})
        return final_list
    def convert_df(self,info):
        df = pd.json_normalize(info)
        df.replace('null',None,inplace=True)
        return df


class orders:
    def __init__(self,df):
        self.df=df
    def calculate_total(self,order_id):
        order_transactions = self.df[self.df['order.order_id'] == order_id]['sales_amt'].sum()
        return order_transactions


class OrderDiscount(orders):
    def __init__(self, df):
        super().__init__(df)
    def calculate_total(self, order_id):
        order_transactions = self.df[self.df['order.order_id'] == order_id]
        total_discounted_amount = 0
        for _, transaction in order_transactions.iterrows():
            discount_percentage = transaction['discount']
            discounted_amount = transaction['sales_amt']*(1 - discount_percentage)
            total_discounted_amount += discounted_amount
        return total_discounted_amount



globalmart_api = fetchapi("https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws","/mentorskool/v1/sales?offset=0&limit=100","fe66583bfe5185048c66571293e0d358")

api_data = globalmart_api.get_api()


sales_df = globalmart_api.convert_df(api_data)

transaction = orders(sales_df)
total_transacTion = transaction.calculate_total( "US-2014-106992")
print(total_transacTion)

discount = OrderDiscount(sales_df)
total_discounted_transaction = discount.calculate_total("CA-2017-100111")
print(total_discounted_transaction)


