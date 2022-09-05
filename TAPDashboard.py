#!/usr/bin/env python
# coding: utf-8

# In[110]:


#Calling Libraries and dash packages
import textwrap
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from plotly.colors import DEFAULT_PLOTLY_COLORS   # chart default colors


# In[111]:


#Calling Data
path = 'data/'
df_post = pd.read_excel(path+'post.xlsx')
df_pre = pd.read_excel(path+'pre.xlsx')



# In[112]:


# App structure
app = dash.Dash(__name__)
app.title = ("Dashboard | Survey Data")
server = app.server
def customwrap(s,width=15):
    return "<br>".join(textwrap.wrap(s,width=width))


# In[113]:


#Pie chart

##Gender
fig_gender=px.pie(df_pre, names='Gender', color='Gender', title= 'Gender')

##Ethnicity
fig_ethnicity=px.pie(df_pre, names='Ethnicity', color='Ethnicity',title='Ethnicity')


# In[114]:


#Radar Chart(rad)

##If...else (IE) Question comparison by groups 
df_radIE=df_post.loc[:,['Are you a musician?', 'If Else']].groupby(by=['Are you a musician?'], as_index=False).mean()
df_radIE['Score'] = 0
df_radIE['If Else']=df_radIE['If Else']*100
df_radIE.loc[df_radIE['If Else']<21, 'Score'] = 1
df_radIE.loc[(df_radIE['If Else']>=21) & (df_radIE['If Else']<41), 'Score'] = 2
df_radIE.loc[(df_radIE['If Else']>=41) & (df_radIE['If Else']<61), 'Score'] = 3
df_radIE.loc[(df_radIE['If Else']>=61) & (df_radIE['If Else']<81), 'Score'] = 4
df_radIE.loc[(df_radIE['If Else'])>=81, 'Score'] = 5

#to connect first and the last dot
ranges=list(df_radIE['Score'])
ranges.append(ranges[0])
thetas=list(df_radIE['Are you a musician?'])
thetas.append(thetas[0])

#wrapping theta string because the string is too long
wrapped_theta = list(map(customwrap, thetas))
radIE = go.Scatterpolar(r=ranges, theta=wrapped_theta, fill='toself')
data=[radIE]
layout=go.Layout(margin=dict(l=100, r=100, b=40, t=40), title='If...else Score Comparison')
fig_radIE=go.Figure(data, layout)

##While loop(WL) Question comparison by groups
df_radWL=df_post.loc[:,['Are you a musician?', 'While Loop']].groupby(by=['Are you a musician?'], as_index=False).mean()
df_radWL['Score'] = 0
df_radWL['While Loop']=df_radWL['While Loop']*100
df_radWL.loc[df_radWL['While Loop']<11, 'Score'] = 1
df_radWL.loc[(df_radWL['While Loop']>=11) & (df_radWL['While Loop']<22), 'Score'] = 2
df_radWL.loc[(df_radWL['While Loop']>=22) & (df_radWL['While Loop']<33), 'Score'] = 3
df_radWL.loc[(df_radWL['While Loop']>=33) & (df_radWL['While Loop']<44), 'Score'] = 4
df_radWL.loc[(df_radWL['While Loop'])>=44, 'Score'] = 5

#to connect first and the last dot
ranges=list(df_radIE['Score'])
ranges.append(ranges[0])
thetas=list(df_radIE['Are you a musician?'])
thetas.append(thetas[0])

#wrapping theta string because the string is too long
wrapped_theta1 = list(map(customwrap, thetas))
radWL = go.Scatterpolar(r=ranges, theta=wrapped_theta1, fill='toself')
data=[radWL]
layout=go.Layout(margin=dict(l=100, r=100, b=40, t=40), title='While Loop Score Comparison', autosize=True)
fig_radWL=go.Figure(data, layout)


# In[115]:


#Line Graph(L)

##Students' Grade Average Pre&Post Survey Comparison
df_post['PostGrade']=df_post['Grade']*100
df_pre['PreGrade']=df_pre['Grade']*100
df_combine=df_pre.merge(df_post, left_on='First name', right_on="First name", how='left')
df_combine['Index'] = df_combine.index
df_combine=df_combine.loc[:,['Index','PreGrade','PostGrade']].groupby(by=['Index'], as_index=False).sum()
Lpre=go.Scatter(x=df_combine['Index'], y=df_combine['PreGrade'], mode='lines+markers', marker=dict(size=5), name="Pre Survey")
Lpost=go.Scatter(x=df_combine['Index'], y=df_combine['PostGrade'], mode='lines+markers', marker=dict(size=5), name="Post Survey")
data=[Lpre,Lpost]
layout=go.Layout(title='Individual Student\'s Improvement ', xaxis=dict(title='Students'), yaxis=dict(title='Grade Average'))
fig_L=go.Figure(data,layout)
fig_L.show()


# In[116]:


#Sankey Diagram(San)

##Students' Feedback on workshop
df_San=df_post.sort_values(by=['Are you a musician?','Did you enjoy learning the new technology?','How difficult did you find learning the new technology?'])

### First, Change NaN values as a category in order to recognize non existing/missing values (important to recognize missing data and filling in)
df_San.loc[df_San['Are you a musician?'] != df_San['Are you a musician?'], 'Are you a musician?'] = 'No response' #NaN values changed as 'No Response'

###changing type to category in order to add in non existing value as 0 (when data is missing, source and target match got messed up ,and resuiting values shifted)
#values
df_San['Are you a musician?']=df_San['Are you a musician?'].astype('category')
df_San['Did you enjoy learning the new technology?']=df_San['Did you enjoy learning the new technology?'].astype('category')
df_San['How difficult did you find learning the new technology?']=df_San['How difficult did you find learning the new technology?'].astype('category')
value1=df_San.groupby(by=['Are you a musician?','Did you enjoy learning the new technology?']).count().fillna(0).astype(int).reset_index() #fill in not available with 0, change the new value as integer, and reset the data index to fill in the gaps in the data frame
value2=df_San.groupby(by=['Did you enjoy learning the new technology?','How difficult did you find learning the new technology?']).count().fillna(0).astype(int).reset_index()
values=list(value1['First name'])+list(value2['First name'])

#labels
lis1=list(value1['Are you a musician?'].unique()) #using the changed category, make the list of data
lis2=list(value1['Did you enjoy learning the new technology?'].unique())#can be from value1 or value2 as selected column is included in both
lis3=list(value2['How difficult did you find learning the new technology?'].unique())
labels=lis1+lis2+lis3

#sources - np.repeat(range(start value,end value), repeating time(number of target)) repeating each value like (1,1,2,2,3,3)
source1=list(np.repeat(range(0,len(lis1)),len(lis2)))
source2=list(np.repeat(range(len(lis1),len(lis1)+len(lis2)),len(lis3)))
sources=source1+source2

#targets - list(range(start value, endv value))*repeating time(number of source)  repeating the whole list again like (1,2,3,1,2,3)
target1=list(range(len(lis1),len(lis1)+len(lis2)))*len(lis1)
target2=list(range(len(lis1)+len(lis2),len(lis1)+len(lis2)+len(lis3)))*len(lis2)
targets=target1+target2

#Graphing
San=go.Sankey(
            node=dict(
                    label=labels,
                    pad=15,
                    thickness=20,
                    line = dict(color='black', width=0.5),
                    color = '#3078b4'
                     ),
            link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color='#CCC'
                    )
                )
data=[San]
layout=go.Layout(
                title = dict(text='Participants Flow', font_size=16),
                font_size=15, height=420, margin=dict(l=50, r=50, b=20, t=50)
                )
fig_San=go.Figure(data,layout)

###In order to label each column with question
cols = ["Are you a musician?","Did you enjoy the learning?","How difficult was the learning?"]
for x_coordinate, column_name in enumerate(cols):
    wrapped_cols = list(map(customwrap, cols))
    fig_San.add_annotation(
        x=x_coordinate/(len(cols)-1),
        y=1.05,
        xref="paper",
        yref="paper",
        text=column_name,
        showarrow=False,
        font=dict(
            family="Tahoma",
            size=13,
            color="black"
            ),
        align="left",
        )


# In[117]:


#Bar Graph (B)
df_B = df_post.loc[:,['Are you a musician?','Grade']].groupby(by = ['Are you a musician?'], as_index = False).mean()
df_B = df_B.sort_values(by = ['Grade'], ascending=False)
df_B['GradePerc'] = df_B['Grade']*100
Bar = go.Bar(x = df_B['Are you a musician?'], # x axis - Are you a musician?
               y = df_B['GradePerc'], # y - Grade
               text = df_B['GradePerc'], 
               texttemplate = '%{text}', 
               hoverinfo = 'text',
               textposition = 'none' # option for bar
                   )
data = [Bar] # save as a list in the data object
layout = go.Layout(title = 'Grade Average in Each Group', height=600, xaxis=dict(title='Groups'), yaxis=dict(title='Grade Average')) # set title
fig_B = go.Figure(data, layout)


# In[ ]:


#App Layout
app.layout = html.Div([
    
    # Main Title
    html.H2('Musical Abilities and Coding Skills: Is There a Correlation?', style={'textAlign': 'center', 'marginBottom':10, 'marginTop':10}),
    
    #Diving-left section
    html.Div([
        
        #Pie Charts-Gender and Ethnicity
        html.Div(className='Pie',
            children=[
                html.Div(dcc.Graph(figure=fig_gender), style={'float':'left', 'display':'inline-block','width':'50%'}),
                html.Div(dcc.Graph(figure=fig_ethnicity), style={'float':'right', 'width':'50%'})
            ]),
       
        #Radar Charts-If Else & While loop Questions
        html.Div(className='Radar',
            children=[
                html.Div(dcc.Graph(figure=fig_radIE), style={'float':'left', 'display':'inline-block','width':'50%'}),
                html.Div(dcc.Graph(figure=fig_radWL), style={'float':'right', 'width':'50%'})
            ]),
        
        #Line Graph-Students' GradeAverage Pre-Post
        html.Div(      
            children=[
                html.Div(dcc.Graph(figure=fig_L),style={'float':'left', 'width':'100%'})
            ])
        
    ], style={'float':'left', 'display':'inline-block', 'width':'50%'}),
    
    #Dividing-right section
    html.Div(
            children=[
                #Sankey Diagram-workshop feedback
                html.Div(dcc.Graph(figure=fig_San),style={'float':'left', 'width':'100%'}),
                #Bar graph-grade comparison of musicians vs. non musicians
                html.Div(dcc.Graph(figure=fig_B),style={'float':'left', 'width':'100%'}),
                html.Div(
                    children=[html.H1('Conclusion', style={'textAlign':'center'}
                                ),
                         html.P('Not all musicians outperformed non-musicians, but musicians who can read music scores performed the best among all students on average. While students had the most difficulty with "If...else" statements and "While Loop" questions (less than 20% of improvement compared to pre-survey), most of the correct answers came from the musicians group who can read music. This study revealed that programming is not directly related to the music itself but the score structures that musicians learn to read. For example, the "While loop" and "If...else" from coding share similarities to repeat signs and coda symbols from music scores, respectively. Through the dashboard, we can predict the possible success of students who studies or knows how to read music scores. Encouraging band or orchestra students in middle and high school to take programming courses, especially talented musicians who do not consider music as their future career, will help to bring more art and creativity to the IT field.'
                               )
                             ])
            ], 
            style={'float':'right', 'width':'50%'})
 
])

    #Run App
if __name__=='__main__': app.run_server(debug=False)
    
    
    
    


# In[ ]:





# In[ ]:




