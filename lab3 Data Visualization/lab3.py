import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

app = dash.Dash()

df = pd.read_csv(
    'dataset/black-friday/BlackFriday.csv')

available_products = sorted(df['Product_ID'].unique())
available_cities = sorted(df['City_Category'].unique())

app.layout = html.Div(
    style={
        'position': 'fixed',
        'top': 0,
        'bottom': 0,
        'left': 0,
        'right': 0,
        'background': 'linear-gradient(to bottom, #00FFFF, #0000FF)',
    },
    children=[
        html.H1(
            children='Black Friday Products',
            style={
                'textAlign': 'center',
                'color': '#000000',
                'fontFamily': 'Comic Sans MS',
                'fontSize': '36px',
                'padding': '20px'
            }
        ),
        html.H2(
            children='Product ID:',
            style={
                'textAlign': 'left',
                'color': '#000000',
                'fontFamily': 'Comic Sans MS',
                'fontSize': '24px',
                'margin-left': '20px'
            }
        ),
        html.Div(
            style={'width': '95%', 'display': 'flex',
                   'border': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(190, 239, 234,0.5)',
                   'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)',
                   'padding': '10px 20px'},
            children=[
                dcc.Dropdown(
                    id='product-id-column',
                    options=[{'label': i, 'value': i} for i in available_products],
                    value='P00000142',
                    style={'width': '55%'}
                ),
                html.Span('City: '),
                dcc.RadioItems(
                    id='city-column',
                    options=[{'label': i, 'value': i} for i in ['A', 'B', 'C']],
                    value='A',
                    labelStyle={'display': 'inline-block'},
                    style={'width': '15%','display': 'inline-block'}
                ),
                html.Span('Age Groups:'),
                html.Div(style={'width': '30%'}, children=[dcc.RangeSlider(
                    id='age-range-slider',
                    min=0,
                    max=5,
                    marks={0: '0', 1: '17', 2: '25', 3: '35', 4: '45', 5: '55+'},
                    value=[0, 5]
                )])
            ]
        ),
        html.Div(
            style={'width': '110%','display': 'flex', 'justify-content': 'left', 'margin': '10px'},
            children=[
                dcc.Graph(id='stacked-bar-chart', style={'width': '30%'}),
                dcc.Graph(id='pie-chart', style={'width': '30%'}),
                dcc.Graph(id='city-occupation-chart', style={'width': '30%'})
            ]
        )
    ]
)


@app.callback(
    dash.dependencies.Output('stacked-bar-chart', 'figure'),
    [dash.dependencies.Input('product-id-column', 'value')])
def update_graph(product_id):
    dff = df[df['Product_ID'] == product_id]

    # 根据年龄、性别分组计算总购买量
    grouped_data = dff.groupby(['Age', 'Gender'], as_index=False)['Purchase'].sum()

    fig = go.Figure()

    # Add stacked bar chart for Purchase by Age and Gender
    for gender in ['M', 'F']:
        gender_data = grouped_data[grouped_data['Gender'] == gender]
        if gender == 'M':
            name = 'Male'
        else:
            name = 'Female'
        fig.add_trace(go.Bar(x=gender_data['Age'], y=gender_data['Purchase'], name=name))

    # Add line chart for total Purchase by Age
    total_data = grouped_data.groupby('Age', as_index=False)['Purchase'].sum()
    fig.add_trace(go.Scatter(mode='lines', x=total_data['Age'], y=total_data['Purchase'], name='Total'))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Age',
        yaxis_title='Purchase',
        title=f'Product <span style="color: grey">{product_id}</span> Purchase from different ages'
    )
    return fig


@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('city-column', 'value'), dash.dependencies.Input('product-id-column', 'value')])
def update_pie_chart(city, product_id):
    dff = df[(df['City_Category'] == city) & (df['Product_ID'] == product_id)]
    grouped_data = dff.groupby('Stay_In_Current_City_Years', as_index=False)['Purchase'].sum()

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=grouped_data['Stay_In_Current_City_Years'],
        values=grouped_data['Purchase'],
        hole=0.4,
        hoverinfo='label+percent',
        textinfo='value',
        textfont=dict(size=12),
        marker=dict(colors=['#FFA500', '#FFD700', '#FF6347', '#9ACD32', '#00BFFF'])
    ))

    fig.update_layout(
        title=f'Product <span style="color: grey">{product_id}</span> Purchase Distribution by <br> Stay Years in <span style="color: grey">{city}</span> city',
        title_x=0.5,
    )
    return fig


@app.callback(
    dash.dependencies.Output('city-occupation-chart', 'figure'),
    [dash.dependencies.Input('age-range-slider', 'value'),
     dash.dependencies.Input('product-id-column', 'value')]
)
def update_city_occupation_chart(age_range, product_id):
    filtered_df = df[(df['Age'].str[0].astype(int) >= age_range[0]) & (df['Age'].str[0].astype(int) <= age_range[1]) & (
            df['Product_ID'] == product_id)]
    # 根据职业和城市分组计算平均购买量
    grouped_data = filtered_df.groupby(['Occupation', 'City_Category'], as_index=False)['Purchase'].mean()
    # 创建柱状图的数据轴
    data = []
    for city in ['A', 'B', 'C']:
        city_data = grouped_data[grouped_data['City_Category'] == city]
        bar = go.Bar(x=city_data['Occupation'], y=city_data['Purchase'], name=f'City {city}')
        data.append(bar)
    # 设置图表布局和样式
    layout = go.Layout(
        title='Average purchase volume of by people of different <br> age groups, occupations, and cities ',
        title_x=0.5,
        xaxis=dict(title='Occupation'),
        yaxis=dict(title='Average Purchase Volume'),
        barmode='group'
    )
    # 创建图表对象
    fig = go.Figure(data=data, layout=layout)
    # 显示图表
    return fig


if __name__ == '__main__':
    app.run_server()
