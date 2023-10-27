import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine

# Connect to the Sakila database
engine = create_engine('mysql://root:FAYv9g4KHkusU66LNGDk@localhost/sakila')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Sakila Rental Data Over Time"),
    
    # Dropdown to select a category
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'Category 1', 'value': 1},
            {'label': 'Category 2', 'value': 2},
            # Add more options based on your data
        ],
        value=1  # Default selected option
    ),
    
    # Line chart to display data over time
    dcc.Graph(id='query-1'),
    dcc.Graph(id='query-2'),
    dcc.Graph(id='query-3'),
    dcc.Graph(id='query-4'),
    dcc.Graph(id='query-5')

])

# Define callback to update the line chart based on the selected category
@app.callback(
    Output('query-1', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    # SQL query to retrieve data for the selected category over time
    query = f"""
    SELECT title, SUM(payment.amount) AS total_revenue
    FROM film
    JOIN inventory ON film.film_id = inventory.film_id
    JOIN rental ON inventory.inventory_id = rental.inventory_id
    JOIN payment ON rental.rental_id = payment.rental_id
    group by film.title
    order by total_revenue desc
    limit 100;
    """

    rental_data = pd.read_sql(query, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['title'],
                'y': rental_data['total_revenue'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count for Category {selected_category}',
            'xaxis': {'title': 'Rental Day'},
            'yaxis': {'title': 'Rental Count'}
        }
    }

    return fig

@app.callback(
    Output('query-2', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    # SQL query to retrieve data for the selected category over time
    query2 = f"""
    select f.film_id, f.title, SUM(p.amount) as total_revenue
    from film f
    join inventory i on f.film_id = i.film_id
    join rental r on i.inventory_id = r.inventory_id
    join payment p on r.rental_id = p.rental_id
    group by f.film_id, f.title
    order by total_revenue DESC
    limit 5;
    """

    rental_data = pd.read_sql(query2, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['title'],
                'y': rental_data['total_revenue'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count for Category',
            'xaxis': {'title': 'Film Title'},
            'yaxis': {'title': 'Revenue'}
        }
    }

    return fig

@app.callback(
    Output('query-3', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    # SQL query to retrieve data for the selected category over time
    query3 = f"""
    select a.actor_id, a.first_name, a.last_name, COUNT(fa.film_id) as number_of_films
    from actor a
    join film_actor fa on a.actor_id = fa.actor_id
    group by a.actor_id, a.first_name, a.last_name
    having COUNT(fa.film_id) > 15
    order by number_of_films desc;
    """

    rental_data = pd.read_sql(query3, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['last_name'],
                'y': rental_data['number_of_films'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count for Category {selected_category}',
            'xaxis': {'title': 'Actor Last Name'},
            'yaxis': {'title': 'Number of Films'}
        }
    }

    return fig

@app.callback(
    Output('query-4', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    # SQL query to retrieve data for the selected category over time
    query4 = f"""
    select 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) as customer_name, 
    SUM(p.amount) as total_payments,
    rank() over (order by SUM(p.amount) desc) as payment_rank
    from customer c
    join payment p on c.customer_id = p.customer_id
    group by c.customer_id, c.first_name, c.last_name
    order by total_payments desc;
    """

    rental_data = pd.read_sql(query4, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['customer_name'],
                'y': rental_data['total_payments'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count for Category {selected_category}',
            'xaxis': {'title': 'Customer Name'},
            'yaxis': {'title': 'Total Payments'}
        }
    }

    return fig

@app.callback(
    Output('query-5', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    # SQL query to retrieve data for the selected category over time
    query5 = f"""
    select 
        a.actor_id, 
        concat(a.first_name, ' ', a.last_name) as actor_name, 
        count(distinct fa.film_id) as number_of_horror_films
    from actor a
    join film_actor fa on a.actor_id = fa.actor_id
    join film_category fc on fa.film_id = fc.film_id
    join category c on fc.category_id = c.category_id
    where c.name = 'Horror'
    group by a.actor_id, a.first_name, a.last_name
    order by number_of_horror_films desc
    limit 3;
"""

    rental_data = pd.read_sql(query5, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['actor_name'],
                'y': rental_data['number_of_horror_films'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count for Category {selected_category}',
            'xaxis': {'title': 'Actor Name'},
            'yaxis': {'title': 'Number of Horror Films'}
        }
    }

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)