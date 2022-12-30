import streamlit as st
import pandas as  pd
import plotly.graph_objects as go

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
    fig1 = go.Figure(
        data=[go.Bar(x=data['Area'], y=data['Export Value'])],
        layout_title_text="Export Value analysis for each country"
    )
    st.plotly_chart(fig1)
    
    fig2 = go.Figure(
        data=[go.Bar(x=data['Area'], y=data['Import Value'])],
        layout_title_text="Import Value analysis for each country"
    )
    st.plotly_chart(fig2)
    
    
def Quantity():
    st.subheader('Analysis of Export and Import Quantity')
    
    



sidebar = st.sidebar.radio('Select one:', ['Home', 'Export and Import Values', 'Export and Import Quantity', 'Years of trade'])

if sidebar == 'Home':
    Home()
elif sidebar == 'Export and Import Values':
    Values()
elif sidebar == 'Export and Import Quantity':
    Quantity()