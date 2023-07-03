#NEEDED LIBRARIES
import pandas as pd
import streamlit as st
import json
import requests
from streamlit_option_menu import option_menu
import mysql.connector as sql
import plotly.express  as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#ESTABLSIHING DB CONNECTION
mydb=sql.connect(host="localhost",
                           user="root",
                           password="Jakan1997@",
                           database="phonepepulse")
mycursor=mydb.cursor()








#CREATING PAGESETUP
st.set_page_config(page_title="PHONEPE")
with st.sidebar:
         selected=option_menu(menu_title="PHONEPE DATA VISUALISATION",
                  options=["HOME","GEO VISUALISATION","OVERALL ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS","TOP CHARTS & TABLES"],
                  icons=["house","map-fill","unlock-fill","cash","people-fill","sort-up"],
                  menu_icon="menu-app",
                  default_index=0)
#--------------------------------------------------HOME PAGE-----------------------------------------------------------------------------------------#
if selected=="HOME":
    st.header("  :bar_chart: WELCOME TO PHONEPE DATA VISUSALISATION")
    st.info(""" - UPI (Unified Payments Interface) is making strides towards global expansion.
                - By analyzing PhonePe Pulse data, we can glean valuable insights and observations.
                - This knowledge can contribute significantly to our understanding of its potential impact on the global stage.""")
    st.info("""
            - In India, Liquid cash has been virtually been replaced by the QR  code-based UPI payment system.
            - UPI used  closely by 300 Million indivuduals and 50 Million Merchants""")
    st.info("""
            STRENGTHS:
            - Interoperability between different banks and different systems
            - Reliability""")
    st.info("""
            FACTS:
            - In JAN 2023 Transactions happened was 8 billion and Money transfered was nearly $200 Billion(source-New York Times)
            - In semi-urban & rural stores, usage spike was 650% in 2022
            - India did more  Digital Dransacions than U.S, U.K, Germany and France combined.
            - UPI is now used in neighbouring countries like bhutan,nepal.
            - NRI's from  U.S, U.K, Canada, Singapore, Australia, UAE, Qatar, Saudi Arabia, Oman can make Payments through UPI""")
    
            


#-----------------------------------------------------GEO VISUALISATION--------------------------------------------------------------------------------#
if selected=="GEO VISUALISATION":
    st.header("DATA VISUALISATION USING MAP")
    col1,col2=st.columns(2)
    with col1:
            year=st.slider("SELECT YEAR",min_value=2018,max_value=2022,value=2020,step=1)
    with col2:
            quarter=st.slider("SELECT QUARTER",min_value=1,max_value=4,value=1,step=1)
    
    tab1,tab2,tab3,tab4=st.tabs(["TOTAL TRANSACTION AMOUNT","TOTAL TRANSACTION COUNT","TOTAL REGISTERED USERS","TOTAL APP OPENINGS"])
    #total transaction amount
    with tab1:
            mycursor.execute("""SELECT state,
                                SUM(transactionamount) AS total_transactionamount
                                FROM aggtransaction
                                WHERE year = %s AND quarter=%s
                                GROUP BY  state,year, quarter""", (year,quarter,))
            chart=mycursor.fetchall()
            chart1=pd.DataFrame(chart,columns=["state","total_transactionamount"])
        
            chart1.drop(columns=['state'], inplace=True)
            #url for map
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            trdata = json.loads(response.content)
            trstate = [feature['properties']['ST_NM'] for feature in trdata['features']]
            trstate.sort()
            trstatemap= pd.DataFrame({'state': trstate})
            trstatemap['Transaction_amount']=chart1
            trstatemap.to_csv('trstatemap.csv', index=False)
            df_trstatemap = pd.read_csv('trstatemap.csv')
            #using choropleth 
            fig = px.choropleth(
            df_trstatemap,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='state',color='Transaction_amount',color_continuous_scale='thermal',title = 'Amount Transacted')
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig,use_container_width=True)
            st.info(" we can identify where the transaction amount is higher and lower in the map  for choosen year and quarter with the help of color scaling")


    


    #total transaction count
    with tab2:
            mycursor.execute("""SELECT state,
                                SUM(transactioncount) AS total_transactioncount
                                FROM aggtransaction
                                WHERE year = %s AND quarter=%s
                                GROUP BY  state,year, quarter""", (year,quarter,))
            chart=mycursor.fetchall()
            chart1=pd.DataFrame(chart,columns=["state","total_transactioncount"])
            
            chart1.drop(columns=['state'], inplace=True)
            #using url for map
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            trdata = json.loads(response.content)
            trstate = [feature['properties']['ST_NM'] for feature in trdata['features']]
            trstate.sort()
            trstatemap= pd.DataFrame({'state': trstate})
            trstatemap['Transaction_count']=chart1
            trstatemap.to_csv('trstatemap.csv', index=False)
            df_trstatemap = pd.read_csv('trstatemap.csv')
            #using choropleth
            fig = px.choropleth(
            df_trstatemap,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='state',color='Transaction_count',color_continuous_scale='thermal',title = 'Total Transactions')
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig,use_container_width=True)
            st.info(" we can identify where the transaction count is higher and lower in the map  for choosen year and quarter with the help of color scaling")

    #total registered users
    with tab3:
            mycursor.execute("""SELECT state,
                                SUM(Registeredusers) AS total_Registeredusers
                                FROM mapuser
                                WHERE year = %s AND quarter=%s
                                GROUP BY  state,year, quarter""", (year,quarter,))
            chart=mycursor.fetchall()
            chart1=pd.DataFrame(chart,columns=["state","total_Registeredusers"])
            chart1.drop(columns=['state'], inplace=True)
            #url for map
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            userdata = json.loads(response.content)
            userstate = [feature['properties']['ST_NM'] for feature in userdata['features']]
            userstate.sort()
            userstatemap= pd.DataFrame({'state': userstate})
            userstatemap['Total_Registeredusers']=chart1
            userstatemap.to_csv('userstatemap.csv', index=False)
            df_userstatemap = pd.read_csv('userstatemap.csv')
            #using choropleth
            fig = px.choropleth(
            df_userstatemap,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='state',color='Total_Registeredusers',color_continuous_scale='thermal',title = 'Registered users')
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig,use_container_width=True)
            st.info(" we can identify where the user registration is higher and lower in the map  for choosen year and quarter with the help of color scaling")




    #total app openings
    with tab4:
            mycursor.execute("""SELECT state,
                                SUM(Appopens) AS total_Appopenings
                                FROM mapuser
                                WHERE year = %s AND quarter=%s
                                GROUP BY  state,year, quarter""", (year,quarter,))
            chart=mycursor.fetchall()
            chart1=pd.DataFrame(chart,columns=["state","total_Appopenings"])
            chart1.drop(columns=['state'], inplace=True)
            #url for map
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            userdata = json.loads(response.content)
            userstate = [feature['properties']['ST_NM'] for feature in userdata['features']]
            userstate.sort()
            userstatemap= pd.DataFrame({'state': userstate})
            userstatemap['Total_Appopenings']=chart1
            userstatemap.to_csv('userstatemap.csv', index=False)
            df_userstatemap = pd.read_csv('userstatemap.csv')
            #using choropleth
            fig = px.choropleth(
            df_userstatemap,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='state',color='Total_Appopenings',color_continuous_scale='thermal',title = 'App Openings')
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig,use_container_width=True)
            st.info(" we can identify where the App Openings is higher and lower in the map  for choosen year and quarter with the help of color scaling")









#-----------------------------------------------------OVERALL ANALYSIS------------------------------------------------------------------------------------------#





if selected=="OVERALL ANALYSIS":
    st.header("Overall Analysis")
    tab1,tab2,tab3,tab4=st.tabs(["TOTAL TRANSACTION AMOUNT","TOTAL TRANSACTION COUNT","TOTAL REGISTERED USERS","TOTAL APP OPENINGS"])
    mycursor.execute("""SELECT year,
                               quarter,
                               SUM(transactioncount) AS total_transactioncount,
                               SUM(transactionamount) AS total_transactionamount
                               FROM maptr
                               GROUP BY  state,year, quarter""")

    chart = mycursor.fetchall()
    chart1 = pd.DataFrame(chart, columns=['year', 'quarter', 'total_transactioncount', 'total_transactionamount'])
    chart1['year_quarter'] = chart1['year'].astype(str) + ' Q' + chart1['quarter'].astype(str)
    #total transaction amount
    with tab1:
                        fig = px.bar(chart1, x='year_quarter', y='total_transactionamount',color='total_transactionamount', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_transactionamount': 'Transaction Amount'},
                                            title='Transaction Amount by Year and Quarter',color_continuous_scale='cividis')
                        fig.update_layout(xaxis_tickangle=90)
                        fig.update_layout(title_x=0.3)
                        st.plotly_chart(fig)

                     
    #total transaction count                    
    with tab2:
                        fig = px.bar(chart1, x='year_quarter', y='total_transactioncount',color='total_transactioncount', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_transactioncount': 'Transaction Count'},
                                            title='Transaction Count by Year and Quarter',color_continuous_scale='cividis')
                        fig.update_layout(xaxis_tickangle=90)
                        fig.update_layout(title_x=0.3)
                        st.plotly_chart(fig)


                        #total transaction count by brands
                        with st.expander(" Percentage share of Total Transaction Count by Top 10 Brands"):
                                mycursor.execute("""SELECT brand, SUM(transactioncount) AS total_transactioncount
                                  FROM agguser
                                  GROUP BY brand
                                  LIMIT 10""")
                                sql=mycursor.fetchall()
                                df = pd.DataFrame(sql, columns=['brand', 'total_transactioncount'])
                                fig = px.pie(df, names='brand', values='total_transactioncount', title='Total Transaction Count by  10 Brands')
                                st.plotly_chart(fig)


                        
    

    mycursor.execute("""SELECT year,
                               quarter,
                               SUM(Registeredusers) AS total_Registeredusers,
                               SUM(Appopens) AS total_Appopens
                               FROM mapuser
                               GROUP BY  state,year, quarter""")
    chart_=mycursor.fetchall()
    chart2=pd.DataFrame(chart_,columns=['year','quarter','total_Registeredusers','total_Appopens'])
    chart2['year_quarter'] = chart2['year'].astype(str) + ' Q' + chart2['quarter'].astype(str)
    #total registered users
    with tab3:                  

                        fig = px.bar(chart2, x='year_quarter', y='total_Registeredusers',color='total_Registeredusers',
                                     labels={'year_quarter': 'Year and Quarter', 'total_Registeredusers': 'Registered users'},
                                     title='Registered users by Year and Quarter',color_continuous_scale='inferno')
                        fig.update_layout(xaxis_tickangle=90)
                        fig.update_layout(title_x=0.3)
                        st.plotly_chart(fig)

    #total app openings
    with tab4:                  

                        fig = px.bar(chart2, x='year_quarter', y='total_Appopens',color='total_Appopens',
                                     labels={'year_quarter': 'Year and Quarter', 'total_Appopens': 'App openings'},
                                     title='App openings by Year and Quarter',color_continuous_scale='inferno')
                        fig.update_layout(xaxis_tickangle=90)
                        fig.update_layout(title_x=0.3)
                        st.plotly_chart(fig)





#---------------------------------------------------TRANSACTION ANALYSIS---------------------------------------------------------------------#



if selected=="TRANSACTION ANALYSIS":
    st.header("TRANSACTION ANALYSIS OVER A PERIOD OF TIME")
    mycursor.execute("SELECT DISTINCT state FROM aggtransaction")
    result=mycursor.fetchall()
    state_list = [state[0] for state in result]
    state=st.selectbox("CHOOSE A STATE TO ANALYSE",(state_list))
    if state:
            tab1,tab2=st.tabs(["TRANSACTIONTYPE","DISTRICT ANALYSIS"])
            #transaction type
            with tab1:
                  col1, col2,col3= st.columns(3)
                  with col1:
                        trtype = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
                                       'Merchant payments','Financial Services','Others'))
                        mycursor.execute("""SELECT year,
                                      quarter,
                                      transactiontype,
                                      SUM(transactioncount) AS total_transactioncount,
                                      SUM(transactionamount) AS total_transactionamount
                                      FROM aggtransaction
                                      WHERE transactiontype = %s AND state=%s
                                      GROUP BY  state,year, quarter""", (trtype,state,))

                        chart = mycursor.fetchall()
                        chart1 = pd.DataFrame(chart, columns=['year', 'quarter', 'transactiontype', 'total_transactioncount', 'total_transactionamount'])
                        # BAR CHART
                        chart1['year_quarter'] = chart1['year'].astype(str) + ' Q' + chart1['quarter'].astype(str)
                        selected_option = st.radio("Select an Option", ["TRANSACTION AMOUNT","TRANSACTION COUNT"],key="option_selection")
                        if selected_option=="TRANSACTION AMOUNT":
                               fig = px.bar(chart1, x='year_quarter', y='total_transactionamount',color='total_transactionamount', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_transactionamount': 'Transaction Amount'},
                                            title='Transaction Amount by Year and Quarter',color_continuous_scale='cividis')
                        if selected_option=="TRANSACTION COUNT":
                               fig = px.bar(chart1, x='year_quarter', y='total_transactioncount',color='total_transactioncount', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_transactioncount': 'Transaction Count'},
                                            title='Transaction Count by Year and Quarter',color_continuous_scale='cividis')
                        
                        fig.update_layout(xaxis_tickangle=90)
                        fig.update_layout(title_x=0.3)
                        st.plotly_chart(fig) 




            #district wise analysis
            with tab2:
                  col1, col2,col3= st.columns(3)
                  with col1:
                        mycursor.execute("SELECT DISTINCT District FROM maptr WHERE state=%s",(state,))
                        result=mycursor.fetchall()
                        District_list = [i[0] for i in result]
                        District_list.sort()
                        #District=st.selectbox("CHOOSE A STATE TO ANALYSE",(District_list)) 
                    


                        disttr = st.selectbox('**Select District**', (District_list))
                        if disttr:
                             mycursor.execute("""SELECT year,
                                      quarter,
                                      SUM(transactioncount) AS total_transactioncount,
                                      SUM(transactionamount) AS total_transactionamount
                                      FROM maptr
                                      WHERE District = %s AND state=%s
                                      GROUP BY  state,year, quarter""", (disttr,state,))

                             chart = mycursor.fetchall()
                             chart1 = pd.DataFrame(chart, columns=['year', 'quarter', 'total_transactioncount', 'total_transactionamount'])
                             # BAR CHART
                             chart1['year_quarter'] = chart1['year'].astype(str) + ' Q' + chart1['quarter'].astype(str)
                             selected_option = st.radio("Select an Option", ["TRANSACTION AMOUNT","TRANSACTION COUNT"])
                             if selected_option=="TRANSACTION AMOUNT":
                                         fig = px.bar(chart1, x='year_quarter', y='total_transactionamount', color='total_transactionamount',
                                            labels={'year_quarter': 'Year and Quarter', 'total_transactionamount': 'Transaction Amount'},
                                            title='Transaction Amount by Year and Quarter',color_continuous_scale='cividis')
                             if selected_option=="TRANSACTION COUNT":
                                         fig = px.bar(chart1, x='year_quarter', y='total_transactioncount',color='total_transactioncount', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_transactioncount': 'Transaction Count'},
                                            title='Transaction Count by Year and Quarter',color_continuous_scale='cividis')
                        
                             fig.update_layout(xaxis_tickangle=90)
                             fig.update_layout(title_x=0.3)
                             st.plotly_chart(fig) 



#-----------------------------------------------------USER ANALYSIS----------------------------------------------------------------------------#


if selected=="USER ANALYSIS":
    st.header("USER ANALYSIS OVER A PERIOD OF TIME")
    mycursor.execute("SELECT DISTINCT state FROM mapuser")
    result=mycursor.fetchall()
    state_list = [state[0] for state in result]
    state=st.selectbox("CHOOSE A STATE TO ANALYSE",(state_list))
    if state:
            tab1,tab2=st.tabs(["STATEWISE","DISTRICTWISE"])
            #statewise
            with tab1:
                  col1, col2,col3= st.columns(3)
                  with col1:
                        usertype = st.radio('**Select type**', ('Registeredusers', 'Appopens' ),key="statewise")
                        mycursor.execute("""SELECT year,
                                      quarter,
                                      SUM(Registeredusers) AS total_Registeredusers,
                                      SUM(Appopens) AS total_Appopens
                                      FROM mapuser
                                      WHERE  state=%s
                                      GROUP BY  state,year, quarter""", (state,))
                        chart=mycursor.fetchall()
                        chart2=pd.DataFrame(chart,columns=['year','quarter','total_Registeredusers','total_Appopens'])
                        chart2['year_quarter'] = chart2['year'].astype(str) + ' Q' + chart2['quarter'].astype(str)
                        if usertype=="Registeredusers":
                                      fig = px.bar(chart2, x='year_quarter', y='total_Registeredusers',color='total_Registeredusers', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_Registeredusers': 'Registered users'},
                                            title='Registered users by Year and Quarter',color_continuous_scale='cividis')
                        if usertype=="Appopens":
                                      fig = px.bar(chart2, x='year_quarter', y='total_Appopens',color='total_Appopens', 
                                            labels={'year_quarter': 'Year and Quarter', 'total_Appopens': 'Appopens'},
                                            title='Appopens by Year and Quarter',color_continuous_scale='cividis')
                                                          
                        fig.update_layout(xaxis_tickangle=90)
                        fig.update_layout(title_x=0.3)
                        st.plotly_chart(fig) 
            #districtwise                     
            with tab2:
                        mycursor.execute("SELECT DISTINCT District FROM mapuser WHERE state=%s",(state,))
                        result=mycursor.fetchall()
                        District_list = [i[0] for i in result]
                        District_list.sort()
                        #District=st.selectbox("CHOOSE A STATE TO ANALYSE",(District_list)) 
                    


                        distuser = st.selectbox('**Select District**', (District_list))
                        if distuser:  
                                col1, col2= st.columns(2)
                                with col1:
                                     usertype = st.radio('**Select type**', ('Registeredusers', 'Appopens' ),key="districtwise")
                                     mycursor.execute("""SELECT year,
                                      quarter,
                                      SUM(Registeredusers) AS total_Registeredusers,
                                      SUM(Appopens) AS total_Appopens
                                      FROM mapuser
                                      WHERE  state=%s AND District=%s
                                      GROUP BY  state,year, quarter""", (state,distuser))
                                     chart=mycursor.fetchall()
                                     chart2=pd.DataFrame(chart,columns=['year','quarter','total_Registeredusers','total_Appopens'])
                                     chart2['year_quarter'] = chart2['year'].astype(str) + ' Q' + chart2['quarter'].astype(str)
                                     if usertype=="Registeredusers":
                                              fig = px.bar(chart2, x='year_quarter', y='total_Registeredusers',color='total_Registeredusers', 
                                                           labels={'year_quarter': 'Year and Quarter', 'total_Registeredusers': 'Registered users'},
                                                           title='Registered users by Year and Quarter',color_continuous_scale='cividis')
                                     if usertype=="Appopens":
                                              fig = px.bar(chart2, x='year_quarter', y='total_Appopens', color='total_Appopens',
                                                           labels={'year_quarter': 'Year and Quarter', 'total_Appopens': 'Appopens'},
                                                              title='Appopens by Year and Quarter',color_continuous_scale='cividis')
                                                          
                                     fig.update_layout(xaxis_tickangle=90)
                                     fig.update_layout(title_x=0.3)
                                     st.plotly_chart(fig) 


#--------------------------------------------------TOP CHARTS AND TABLES-------------------------------------------------------------------------------#

if selected=="TOP CHARTS & TABLES":
       st.header("Top Charts & Tables")
       col1,col2=st.columns(2)
       with col1:
           year=st.selectbox("choose a year",['2018','2019','2020','2021','2022'])
       with col2:
           quarter=st.selectbox("choose a quarter",['1','2','3','4'])
           
       tab1,tab2=st.tabs(["TOTAL TRANSACTION COUNT & TOTAL TRANSACTION AMOUNT","TOTAL REGISTERED USERS & TOTAL APP OPENINGS"])
       sql = """SELECT state, SUM(transactioncount) AS total_transactioncount, 
                SUM(transactionamount) AS total_transactionamount
                FROM toptransaction
                WHERE year = %s AND quarter = %s
                GROUP BY state, year, quarter
                ORDER BY total_transactioncount DESC, total_transactionamount DESC
                LIMIT 3
             """
       #total transaction count and total transaction amount
       with tab1:
       
                 mycursor.execute(sql, (year, quarter))
                 result = mycursor.fetchall()
                 chart3=pd.DataFrame(result,columns=["state","total_transactioncount","total_transactionamount"])
                 fig = make_subplots(rows=1, cols=2,subplot_titles=[" Transaction Count", " Transaction Amount"])
                 fig.add_trace(go.Bar(x=chart3["state"], y=chart3["total_transactionamount"], marker=dict(color='green'), name='TOTAL AMOUNT'), row=1, col=2)
                 fig.add_trace(go.Bar(x=chart3["state"], y=chart3["total_transactioncount"], marker=dict(color='blue'),name='TOTAL COUNT'), row=1, col=1)
                 fig.update_layout(height=300, width=800, title_text="TOP 3 STATES")
                 st.plotly_chart(fig)
                 st.subheader("Top 3 States by Transaction Count & Transaction Amount")
                 trace=go.Table(header=dict(values=list(chart3.columns),
                                            fill=dict(color='#C2D4FF'),
                                            align=['left']*5),
                                cells=dict(values=[chart3.state,chart3.total_transactioncount,chart3.total_transactionamount],
                                                   fill=dict(color='#F5F8FF'),
                                           align=['left']*5))
                 data=[trace]
                 st.plotly_chart(data)
                 
                 
       
       #total registered users and total app openings
       with tab2:
                
                 mycursor.execute("""SELECT state, SUM(Registeredusers) AS total_Registeredusers
                          FROM topuser
                          WHERE year = %s AND quarter = %s
                          GROUP BY state, year, quarter
                          ORDER BY total_Registeredusers DESC
                          LIMIT 3
                          """,(year,quarter,))
 
                
                 #mycursor.execute(sql1, (year, quarter))
                 result1 = mycursor.fetchall()
                 chart4=pd.DataFrame(result1,columns=["state","total_Registeredusers"])
                 
                 sql2 = """SELECT state, SUM(Appopens) AS total_AppOpenings
                          FROM mapuser
                          WHERE year = %s AND quarter = %s
                          GROUP BY state, year, quarter
                          ORDER BY total_AppOpenings DESC
                          LIMIT 3
             """
 
                
                 mycursor.execute(sql2, (year, quarter))
                 result2 = mycursor.fetchall()
                 chart5=pd.DataFrame(result2,columns=["state","total_AppOpenings"])
                 fig = make_subplots(rows=1, cols=2,subplot_titles=[" Registered users", " App openings"])
                 fig.add_trace(go.Bar(x=chart4["state"], y=chart4["total_Registeredusers"], marker=dict(color='green'), name='TOTAL REGISTERED USERS'), row=1, col=1)
                 fig.add_trace(go.Bar(x=chart5["state"], y=chart5["total_AppOpenings"], marker=dict(color='blue'),name='TOTAL APP OPENINGS'), row=1, col=2)
                 fig.update_layout(height=300, width=800, title_text="TOP 3 STATES")
                 st.plotly_chart(fig)
                 #plotly tables
                 st.subheader("Top 3 States by Registered users")
                 trace=go.Table(header=dict(values=list(chart4.columns),
                                            fill=dict(color='#C2D4FF'),
                                            align=['left']*5),
                                cells=dict(values=[chart4.state,chart4.total_Registeredusers],
                                                   fill=dict(color='#F5F8FF'),
                                           align=['left']*5))
                 data=[trace]
                 st.plotly_chart(data)

                 st.subheader("Top 3 States by  App Openings")
                 trace=go.Table(header=dict(values=list(chart5.columns),
                                            fill=dict(color='#C2D4FF'),
                                            align=['left']*5),
                                cells=dict(values=[chart5.state,chart5.total_AppOpenings],
                                                   fill=dict(color='#F5F8FF'),
                                           align=['left']*5))
                 data=[trace]
                 st.plotly_chart(data)



                

                 
















