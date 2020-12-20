#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:06:01 2020

@author: kelly
"""


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time


@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


#Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()


#---------TITLE OF DASHBOARD----------

st.title('A Deep Dive on Hospital Performance and Payments in NY Inpatient and Outpatient Facilities')
st.markdown('By: Kelly Chen')
st.markdown('Last updated: December 20th, 2020')
st.markdown('The purpose of this case study report is to compare hospital performance across New York utilizing Python programming language and Streamlit. The variables used in this case study report includes mortality rate, safety of care, and patient experience. In addition, average total payments for providers in inpatient and outpatient facilities will be compared. This report will also provide a deeper diver into the hospital performance of and total payments to Stony Brook University Hospital, Maimonides Medical Center, and Mount Sinai Hospital.')

#Creating Menu to look at the datasets used in this dashboard
st.markdown('Three national-level datasets were used in this report. To review each dataset, please click on the select bar below. Please note that due to the amount of observations in the inpatient and outpatient payments data, loading time may take 5-10 seconds. Please give it a moment. :smile:')
selectbar = st.selectbox('Select Dataset', ("Hospital Experience", "Inpatient Payments", "Outpatient Payments"))


def get_dataset(selectbar):
    if selectbar == 'Hospital Experience':
        st.write(df_hospital_2)
    if selectbar == 'Inpatient Payments':
        st.write(df_inpatient_2)
    if selectbar == 'Outpatient Payments':
        st.write(df_outpatient_2)

st.write(get_dataset(selectbar))


#-----------HOSPITALS IN NY-------------

st.markdown('---')
st.title('Hospitals in New York')
hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
hospitals_ny = hospitals_ny.sort_values('hospital_name')

#value count of hospitals
hospitaltypes = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(hospitaltypes)
st.markdown('The table above shows the number of different hospitals in NY, as based on the datasets used in this report. The majority of NY hospitals are acute care, followed by psychiatric.')

#pie chart of value counts with percentages
fig = px.pie(hospitaltypes, values='hospital_type', names='index')
st.plotly_chart(fig)
st.markdown('Above is a pie chart to better visualize the distribution of the types of hospitals in NY that are in the datasets used in this report. To view the counts of the hospitals, please hover over the percentages.')

#map of NY hospital locations
st.subheader('Map of NY Hospital Locations')
hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])
st.map(hospitals_ny_gps)
st.markdown('To explore the locations of these hospitals, please utilize the map above. You can zoom in and out of the map using the scroll button on your mouse. Based on the map, we see that there is a heavy concentration of hospitals within the NYC area. ')



#-----------HOSPITAL PERFORMANCE------------

st.markdown('---')
st.title('Hospital Performance')        
st.markdown('In this section, we will focus on comparing the hospital performance of Stony Brook University Hospital, Maimonides Medical Center, and Mount Sinai Hospital with their respective counties: Suffolk, Kings, and New York county.')

#creating dataframes for the counties
suffolk = hospitals_ny[hospitals_ny['county_name']=='SUFFOLK']
suffolk = suffolk[['provider_id','hospital_name','city','state','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]

kings = hospitals_ny[hospitals_ny['county_name']=='KINGS']
kings = kings[['provider_id','hospital_name','city','state','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]

newyork = hospitals_ny[hospitals_ny['county_name']=='NEW YORK']
newyork = newyork[['provider_id','hospital_name','city','state','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]




#------SUFFOLK COUNTY-------------
st.header('SUFFOLK COUNTY')

#Look at Stony
st.markdown('<font color=‘blue’>STONY BROOK UNIVERSITY HOSPITAL</font>', unsafe_allow_html=True)
st.markdown('The table below indicates hospital performance data for SUNY Stony Brook University Hospital. Please click on the drag bar to move to the left or right of this table. When compared at the national level, SBU Hospital is above average for mortality and safety of care. However, it is below the national average in patient experience. This could imply that improved safety of care does not necessarily decrease mortality rate in Stony Brook University Hospital. According to the dataset used and the pie charts below, most hospitals in Suffolk have an above average mortality rate. There is an equal amount of hospitals with above average and below average safety of care in Suffolk County. Most hospitals are below the national average in terms of patient experience. SBU Hospital follows the trends of most Suffolk County hospitals for mortality, safety of care, and patient experience.')

stony = hospitals_ny.loc[[2139]]
stony = stony[['provider_id','hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(stony)

#Look at Suffolk County
st.markdown('<font color=‘blue’>SUFFOLK COUNTY MORTALITY</font>', unsafe_allow_html=True)
suffolk_mortality = suffolk['mortality_national_comparison'].value_counts().reset_index()
suf_mort_pie = px.pie(suffolk_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(suf_mort_pie)


st.markdown('<font color=‘blue’>SUFFOLK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
suffolk_safety = suffolk['safety_of_care_national_comparison'].value_counts().reset_index()
suf_safety_pie = px.pie(suffolk_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(suf_safety_pie)


st.markdown('<font color=‘blue’>SUFFOLK COUNTY PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
suffolk_patient = suffolk['patient_experience_national_comparison'].value_counts().reset_index()
suffolk_patient_exp = px.pie(suffolk_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(suffolk_patient_exp)



#------KINGS COUNTY-------------
st.header('KINGS COUNTY')

#Look at Maimonides
st.markdown('<font color=‘green’>MAIMONIDES MEDICAL CENTER</font>', unsafe_allow_html=True)
st.markdown('The table below indicates hospital performance data for Maimonides Medical Center. Please click on the drag bar to move to the left or right of this table. When compared at the national level, Maimonides Medical Center has above average in mortality rate and below average in safety of care and patient experience. When compared to the rest of the hospitals in Kings County, Maimonides Medical Center is doing worse in terms of mortality rate. Most hospitals in this county have below the national average for safety of care and patient experience.')

maimonides = hospitals_ny.loc[[109]]
maimonides = maimonides[['provider_id','hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(maimonides)

#Look at Kings County
kings_mortality = kings['mortality_national_comparison'].value_counts().reset_index()

st.markdown('<font color=‘green’>KINGS COUNTY MORTALITY</font>', unsafe_allow_html=True)
kings_mortality = kings['mortality_national_comparison'].value_counts().reset_index()
kings_mort_pie = px.pie(kings_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(kings_mort_pie)


st.markdown('<font color=‘green’>KINGS COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
kings_safety = kings['safety_of_care_national_comparison'].value_counts().reset_index()
kings_safety_pie = px.pie(kings_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(kings_safety_pie)


st.markdown('<font color=‘green’>KINGS COUNTY PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
kings_patient = kings['patient_experience_national_comparison'].value_counts().reset_index()
kings_patient_exp = px.pie(kings_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(kings_patient_exp)




#------NEW YORK COUNTY-------------
st.header('NEW YORK COUNTY')

#Look at Mount Sinai
st.markdown('<font color=‘orange’>MOUNT SINAI HOSPITAL</font>', unsafe_allow_html=True)
st.markdown('The table below indicates hospital performance data for Mount Sinai Hospital. Please click on the drag bar to move to the left or right of this table. When compared at the national level, Mount Sinai Hospital is above the national average for mortality and safety of care. However, it is below the national average for patient experience. In New York County, most hospitals are above average in terms of mortality rate and below average in terms of patient experience. However, Mount Sinai is doing better compared to other hospitals in New York County in terms of safety of care.')

sinai = hospitals_ny.loc[[2491]]
sinai = sinai[['provider_id','hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(sinai)

#Look at New York County as a whole
ny_mortality = newyork['mortality_national_comparison'].value_counts().reset_index()

st.markdown('<font color=‘orange’>NEW YORK COUNTY MORTALITY</font>', unsafe_allow_html=True)
ny_mortality = newyork['mortality_national_comparison'].value_counts().reset_index()
ny_mort_pie = px.pie(ny_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(ny_mort_pie)


st.markdown('<font color=‘orange’>NEW YORK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
ny_safety = newyork['safety_of_care_national_comparison'].value_counts().reset_index()
ny_safety_pie = px.pie(ny_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(ny_safety_pie)


st.markdown('<font color=‘orange’>NEW YORK PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
ny_patient = newyork['patient_experience_national_comparison'].value_counts().reset_index()
ny_patient_exp = px.pie(ny_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(ny_patient_exp)



st.markdown('---')



#-------Inpatient Payments---------------
st.title('Inpatient Payments')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.markdown('Below you will find the total discharges for each type of DRG in NY inpatient hospitals. The most discharges involve septicemia or sever sepsis, while the least discharges involve O.R. procedures for multiple significant trauma. The total number of discharges from inpatient hospitals in NY is 425742.')
##Common D/C 
common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()
common_discharges = common_discharges.sort_values('total_discharges', ascending=False)

top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)

st.header('DRGs in Inpatient NY Hospitals')
st.dataframe(common_discharges)

col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)


#Bar Charts of the costs
#First filtering inpatient_ny to hospitals of interest
inpatient_3_hospitals = inpatient_ny.loc[(inpatient_ny['provider_name']=='MOUNT SINAI HOSPITAL') | (inpatient_ny['provider_name']=='UNIVERSITY HOSPITAL ( STONY BROOK )') | (inpatient_ny['provider_name']=='MAIMONIDES MEDICAL CENTER')]

costs = inpatient_3_hospitals.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_3_hospitals.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')

costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']
costs_sum = costs_sum.sort_values('average_total_payments', ascending=False)

st.header('Average Total Payments in Maimonides, Mount Sinai, and Stony Brook University Hospital')

bar1 = px.bar(costs_sum, x='provider_name', y='average_total_payments', color='provider_name')
bar1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(bar1)

st.markdown('This bar graph above represents the average total payments for Maimonides Medical Center, Mount Sinai Hospital, and Stony Brook University Hospital. Mount Sinai Hospital has almost 2 times more total payments than Maimonides and about 1/4 times more total payments than SBU Hospital.')

st.header("Hospital Average Payments")
st.dataframe(costs_sum)
st.markdown('The table above showcases the average total payments, average Medicare payments, and non-Medicare payments for the hospitals of interest. Mount Sinai has the largest non-Medicare total payment compared to Maimonides and Stony Brook.')

#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_3_hospitals.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)

st.markdown('The table above showcases the average total payments by DRG and hospital. The highest total payment for Maimonides Medical Center and Stony Brook University Hospital is for tracheostomy procedures. The highest total payment for Mount Sinai Hospital is for heart transplants. However, it is also noteworthy that the second highest payment in Mount Sinai also goes to tracheostomy procedures.')

st.markdown('---')




#---------Outpatient Payments-----------------
st.title('Outpatient Payments')
outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']
total_outpatient_count = sum(outpatient_ny['outpatient_services'])
print(total_outpatient_count) #1865023
st.markdown('Below you will find the total number of patient services by APC code in NY outpatient facilities. The top 3 most utilized services are hospital clinic visits, level 1 echocardiogram without contrast, and level III diagnostic and screening ultrasound. On the other hand, the 3 least utilized services includes level III endoscopy upper airway, level II noninvasion physiologic studies, and level IV endoscopy upper airway. The total amount of outpatient services is 1865023.')

common_services = outpatient_ny.groupby('apc')['outpatient_services'].sum().reset_index()
common_services = common_services.sort_values('outpatient_services', ascending=False)

top10 = common_services.head(10)
bottom10 = common_services.tail(10)

st.header('APCs in Outpatient NY Facilities')
st.dataframe(common_services)

col1, col2 = st.beta_columns(2)

col1.header('Top 10 APCs')
col1.dataframe(top10)

col2.header('Bottom 10 APCs')
col2.dataframe(bottom10)


#Drilling down to 3 facilities of interest
outpatient_3_facilities = outpatient_ny.loc[(outpatient_ny['provider_name']=='Mount Sinai Hospital') | (outpatient_ny['provider_name']=='University Hospital ( Stony Brook )') | (outpatient_ny['provider_name']=='Maimonides Medical Center')]

#Outpatient Average Payments
st.header('Average Total Payments in Maimonides, Mount Sinai, and Stony Brook University Hospital for Outpatient Services')

outpatient_sum = outpatient_3_facilities.groupby('provider_name')['average_total_payments'].sum().reset_index()
outpatient_sum['average_total_payments'] = outpatient_sum['average_total_payments'].astype('int64')
outpatient_sum = outpatient_sum.sort_values('average_total_payments', ascending=False)

bar2 = px.bar(outpatient_sum, x='provider_name', y='average_total_payments', color='provider_name')
bar2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(bar2)

st.markdown('This bar graph above represents the average total payments for Maimonides Medical Center, Mount Sinai Hospital, and Stony Brook University Hospital for outpatient services. Mount Sinai Hospital has about 2 times more total payments than Maimonides and almost 1/7 times more total payments than SBU Hospital.')

st.header("Outpatient Average Payments")
st.dataframe(outpatient_sum)
st.markdown('The table above showcases the average total payments for the facilities of interest. Likewise for inpatient services, Mount Sinai has the highest average total payments for outpatient services compared to Maimonides and Stony Brook.')

#Costs by Condition and Hospital / Average Total Payments
costs_service_outpatient = outpatient_3_facilities.groupby(['provider_name', 'apc'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Outpatient Facility - Average Total Payments")
st.dataframe(costs_service_outpatient)

temp = costs_service_outpatient.sort_values('average_total_payments', ascending=False)

st.markdown('The table above showcases the average total payments by APC and facility. The highest total payment for Mount Sinai and SBU Hospital is for level IV endoscopy for the upper airway. On the other hand, the highest total payment for Maimonides is for level II cardiac imaging.')

st.markdown('---')