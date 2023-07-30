import pandas as pd

class DataFrame():
    def __init__(self) -> None:
        self.df = pd.read_json('trial_task.json')
        self.exploted_df = self.df.explode('products',ignore_index=True)
        self.df = pd.concat([self.exploted_df.drop('products', axis=1), pd.json_normalize(self.exploted_df['products'])], axis=1)

class Tasks(DataFrame):
    def __init__(self) -> None:
        super().__init__()
        self.cost_rate_df = pd.DataFrame(columns=['warehouse_name','cost_rate'])
        self.product_info_df = pd.DataFrame(columns=['product', 'quantity', 'income', 'expenses', 'profit'])
        self.profit_order_df = pd.DataFrame(columns=['order_id', 'order_profit'])
        self.warehouse_profit_df = pd.DataFrame(columns=['warehouse_name', 'profit'])
        self.product_profit_percent_df = pd.DataFrame(columns=['warehouse_name' , 'product','quantity', 'profit', 'percent_profit_product_of_warehouse'])

    def cost_rate(self):
        for row in self.df.itertuples():
            if not (self.cost_rate_df['warehouse_name'] == row[2]).any():
                new_row = {'warehouse_name': row[2], 'cost_rate': abs(row[3])*row[6]}
                self.cost_rate_df = pd.concat([self.cost_rate_df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                self.cost_rate_df.loc[self.cost_rate_df['warehouse_name'] == row[2], 'cost_rate'] += abs(row[3])*row[6]
        self.cost_rate_df.to_excel('Task_1.xlsx', index=False)

    def product_info(self):
        for row in self.df.itertuples():
            income = row[5]*row[6]
            expenses = abs(row[3])*row[6]
            if not (self.product_info_df['product'] == row[4]).any():
                new_row = {'product':row[4], 'quantity':row[6], 'income': income, 'expenses': expenses, 'profit' : income - expenses}
                self.product_info_df = pd.concat([self.product_info_df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                self.product_info_df.loc[self.product_info_df['product'] == row [4], 'quantity'] += row[6]
                self.product_info_df.loc[self.product_info_df['product'] == row [4], 'income'] += income
                self.product_info_df.loc[self.product_info_df['product'] == row [4], 'expenses'] += expenses
                self.product_info_df.loc[self.product_info_df['product'] == row [4], 'profit'] += income - expenses
        self.product_info_df.to_excel('Task_2.xlsx', index=False)
    
    def profit_order(self):
        for row in self.df.itertuples():
            income = row[5]*row[6]
            expenses = abs(row[3])*row[6]
            profit = income - expenses
            if not (self.profit_order_df['order_id'] == row[1]).any():
                new_row = {'order_id':row[1], 'order_profit':profit}
                self.profit_order_df = pd.concat([self.profit_order_df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                self.profit_order_df.loc[self.profit_order_df['order_id'] == row [1], 'order_profit'] += profit
        self.profit_order_df.to_excel('Task_3.xlsx', index=False)   

    def average_profit_order (self) -> float:
        sum = 0 
        count = 0
        for row in self.profit_order_df.itertuples():
            count += 1
            sum += row[2]
        return sum/count
    
    def warehouse_profit(self):
        for row in self.df.itertuples():
            income = row[5]*row[6]
            expenses = abs(row[3])*row[6]
            profit = income - expenses
            if not (self.warehouse_profit_df['warehouse_name'] == row[2]).any():
                new_row = {'warehouse_name':row[2], 'profit': profit}
                self.warehouse_profit_df = pd.concat([self.warehouse_profit_df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                self.warehouse_profit_df.loc[self.warehouse_profit_df['warehouse_name'] == row [2], 'profit'] += profit

    def product_profit_percent(self):
        self.warehouse_profit()
        for row in self.df.itertuples():
            income = row[5]*row[6]
            expenses = abs(row[3])*row[6]
            profit = income - expenses
            profit_warehouse = self.warehouse_profit_df.loc[self.warehouse_profit_df['warehouse_name'] == row[2], 'profit'].values[0]
            profit_percent = profit/profit_warehouse*100
            if not ((self.product_profit_percent_df['warehouse_name'] == row[2]) & (self.product_profit_percent_df['product'] == row[4])).any():
                new_row = {
                    'warehouse_name': row[2], 
                    'product' : row[4], 
                    'quantity': row[6], 
                    'profit': profit, 
                    'percent_profit_product_of_warehouse': profit_percent
                    }
                self.product_profit_percent_df = pd.concat([self.product_profit_percent_df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                self.product_profit_percent_df.loc[(self.product_profit_percent_df['warehouse_name'] == row [2]) 
                                                    & (self.product_profit_percent_df['product'] == row [4]), 'quantity'] += row[6]
                self.product_profit_percent_df.loc[(self.product_profit_percent_df['warehouse_name'] == row [2]) 
                                                    & (self.product_profit_percent_df['product'] == row [4]), 'profit'] += profit
                self.product_profit_percent_df.loc[(self.product_profit_percent_df['warehouse_name'] == row [2]) 
                                                    & (self.product_profit_percent_df['product'] == row [4]), 'percent_profit_product_of_warehouse'] += profit_percent
        self.product_profit_percent_df.to_excel('Task_4.xlsx', index=False)  
    
    def accumulated_percent(self):
        self.accumulated_percent_df = self.product_profit_percent_df.sort_values(['warehouse_name','percent_profit_product_of_warehouse'], ascending=[True,False])
        warehouse_name = self.accumulated_percent_df.iloc[0]['warehouse_name']
        accumulated_values = []
        accumulated_value = 0
        for row in self.accumulated_percent_df.itertuples():
            if row[1] == warehouse_name:
                accumulated_value += row[5]
                accumulated_values.append(accumulated_value)
            else:
                accumulated_value = row[5]
                accumulated_values.append(accumulated_value)
                warehouse_name = row[1]
        self.accumulated_percent_df['accumulated_percent_profit_product_of_warehouse'] = accumulated_values
        self.accumulated_percent_df.to_excel('Task_5.xlsx', index=False)  

    def category_accumulated_percent(self):
        self.category_accumulated_percent_df = self.accumulated_percent_df 
        category_accumulated_values = []
        for row in self.category_accumulated_percent_df.itertuples():
            if row[6] <= 70:
                category_accumulated_values.append('А')
            elif row[6] > 70 and row[6] <= 90:
                category_accumulated_values.append('Б')
            else:
                category_accumulated_values.append('В')
        self.category_accumulated_percent_df['category'] = category_accumulated_values
        self.category_accumulated_percent_df.to_excel('Task_6.xlsx', index=False)  

def main():
    data_1 = Tasks()   
    data_1.cost_rate()
    data_1.product_info()
    data_1.profit_order()
    average = data_1.average_profit_order()
    data_1.product_profit_percent()
    data_1.accumulated_percent()
    data_1.category_accumulated_percent()
    print('-----------------------------------------\n','ЗАДАНИЕ: Найти тариф стоимости доставки для каждого склада\n\n', data_1.cost_rate_df, '\n-----------------------------------------')
    print('-----------------------------------------\n','ЗАДАНИЕ: Найти суммарное количество , суммарный доход , суммарный расход и суммарную прибыль для каждого товара\n\n', data_1.product_info_df, '\n-----------------------------------------')
    print('-----------------------------------------\n','ЗАДАНИЕ: Составить табличку co столбцами order_id (id заказа) и order_profit\n\n', data_1.profit_order_df, '\n', 'Средняя прибыль: ', average, '\n-----------------------------------------')
    print('-----------------------------------------\n','ЗАДАНИЕ: Составить табличку типа warehouse_name, product,quantity, profit, percent_profit_product_of_warehouse\n\n', data_1.product_profit_percent_df, '\n-----------------------------------------')
    print('-----------------------------------------\n','ЗАДАНИЕ: Взять предыдущую табличку и отсортировать percent_profit_product_of_warehouse по убыванию, после посчитать накопленный процент.\n\n', data_1.accumulated_percent_df, '\n-----------------------------------------')
    print('-----------------------------------------\n','ЗАДАНИЕ: Присвоить A,B,C - категории на основании значения накопленного процента\n\n', data_1.category_accumulated_percent_df, '\n-----------------------------------------')

if __name__ == '__main__':
    main()