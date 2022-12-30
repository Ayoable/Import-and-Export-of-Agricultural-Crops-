import streamlit as st
import pandas as  pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

st.header('Ireland and Other Countries Agricultural')

df = pd.read_csv('live animal stock.csv')

def preprocessing(df):
    # Step 1
    imp = df[df['Element'].str.count('Import Value') == 1]
    print(len(imp['Value']))
    imp['id'] = [f'ID_{i+1}' for i in range(len(imp))]
    imp.columns = ['Domain Code', 'Domain', 'Area Code (M49)', 'Area', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit',
        'Import Value', 'Flag', 'Flag Description','id']
    imp = imp.drop(['Domain Code', 'Domain', 'Item Code (CPC)','Area Code (M49)','Area','Element Code', 'Element','Year Code',  'Flag', 'Flag Description'],axis=1)


    # step 2
    exp = df[df['Element'].str.count('Export Value') == 1]
    exp['id'] = [f'ID_{i+1}' for i in range(len(exp))]
    exp.columns = ['Domain Code', 'Domain', 'Area Code (M49)', 'Area', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit',
        'Export Value', 'Flag', 'Flag Description','id']
    exp = exp.drop(['Domain Code', 'Domain', 'Area Code (M49)', 'Area', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit','Flag', 'Flag Description'],axis=1)
    
    # step 3
    exp_q = df[df['Element'].str.count('Export Quantity') == 1]
    exp_q['id'] = [f'ID_{i+1}' for i in range(len(exp_q))]
    exp_q.columns = ['Domain Code', 'Domain', 'Area Code (M49)', 'Area', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit',
        'Export Quantity', 'Flag', 'Flag Description','id']
    exp_q = exp_q.drop(['Domain Code', 'Domain', 'Area Code (M49)', 'Area', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit','Flag', 'Flag Description'],axis=1)
    
    # step 4
    imp_q = df[df['Element'].str.count('Import Quantity') == 1]
    imp_q['id'] = [f'ID_{i+1}' for i in range(len(imp_q))]
    imp_q.columns = ['Domain Code', 'Domain', 'Area Code (M49)', 'Area', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit',
        'Import Quantity', 'Flag', 'Flag Description','id']
    imp_q = imp_q.drop(['Domain Code', 'Domain', 'Area Code (M49)', 'Element Code',
        'Element', 'Item Code (CPC)', 'Item', 'Year Code', 'Year', 'Unit','Flag', 'Flag Description'],axis=1)

    # step 5
    #merging data on unique id using inner join
    data = pd.merge(imp,exp,on='id',how='inner')
    data = pd.merge(data,imp_q,on='id',how='inner')
    data = pd.merge(data,exp_q,on='id',how='inner')
    
    # step 6
    data['Net Export Value'] = data['Export Value'] - data['Import Value']
    
    return data


data = preprocessing(df)


def Home():
    st.subheader('The Dataset')
    st.dataframe(data)

def Values():
    st.subheader('Analysis of Export and Import Values')
    fig1 = px.bar(x=data['Area'], y=data['Export Value'], title="Export Value analysis for each country")
    st.plotly_chart(fig1)
    
    fig4 = px.bar(y=data['Export Value'], x=data['Year'], color=data['Area'], title='Yearly Export Value of all Countries specified')
    st.plotly_chart(fig4)
    
    
    fig2 = px.bar(x=data['Area'], y=data['Import Value'], title="Import Value analysis for each country")
    st.plotly_chart(fig2)
    
    fig3 = px.bar(y=data['Import Value'], x=data['Year'], color=data['Area'], title='Yearly Import Value of all Countries specified')
    st.plotly_chart(fig3)
    
    
def Quantity():
    st.subheader('Analysis of Export and Import Quantity')
    fig1 = px.bar(x=data['Area'], y=data['Export Quantity'], title="Export Quantity analysis for each country")
    st.plotly_chart(fig1)
    
    fig4 = px.bar(y=data['Export Quantity'], x=data['Year'], color=data['Area'], title='Yearly Export Quantity of all Countries specified')
    st.plotly_chart(fig4)
    
    
    fig2 = px.bar(x=data['Area'], y=data['Import Quantity'], title="Import Quantity analysis for each country")
    st.plotly_chart(fig2)
    
    fig3 = px.bar(y=data['Import Quantity'], x=data['Year'], color=data['Area'], title='Yearly Import Quantity of all Countries specified')
    st.plotly_chart(fig3)
 
 
def NetProfit():
    st.subheader('Analysis of all Net Export Value for Ireland and Other Countries')

    table_data = pd.DataFrame()
    table_data['Items'] = data.groupby('Area')['Net Export Value'].mean().index
    table_data['Total Frequency'] = data.groupby('Area')['Net Export Value'].mean().values
        
    
    fig = ff.create_table(table_data, height_constant=60)

    Items = data.groupby('Area')['Net Export Value'].mean().index
    Total_Frequency = data.groupby('Area')['Net Export Value'].mean().values

    trace1 = go.Bar(x=Items, y=Total_Frequency,
                        marker=dict(color='#0099ff'),
                        name='Total frequency of all crops',
                        xaxis='x2', yaxis='y2')
    

    fig.add_traces([trace1])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': 'Net Export Value'})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t':75, 'l':50})


    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height':800})


    st.plotly_chart(fig)
     
   

def Items():
    st.subheader('Analysis of all crops Items')

    table_data = pd.DataFrame()
    table_data['Items'] = data['Item'].value_counts().index
    table_data['Total Frequency'] = data['Item'].value_counts().values
        
    
    fig = ff.create_table(table_data, height_constant=60)

    Items = data['Item'].value_counts().index
    Total_Frequency = data['Item'].value_counts().values

    trace1 = go.Bar(x=Items, y=Total_Frequency,
                        marker=dict(color='#0099ff'),
                        name='Total frequency of all crops',
                        xaxis='x2', yaxis='y2')
    

    fig.add_traces([trace1])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': 'Total frequency of all crops'})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t':75, 'l':50})


    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height':800})


    st.plotly_chart(fig)
    


sidebar = st.sidebar.radio('Select one:', ['Home', 'Export and Import Values', 'Export and Import Quantity', 'Net Export Profit','All Crop Items'])

if sidebar == 'Home':
    Home()
elif sidebar == 'Export and Import Values':
    Values()
elif sidebar == 'Export and Import Quantity':
    Quantity()
elif sidebar == 'Net Export Profit':
    NetProfit()
elif sidebar == 'All Crop Items':
    Items()