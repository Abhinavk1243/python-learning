import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import os
import plotly.express as px 

def main():
    mapbox_access_token = "pk.eyJ1Ijoia3Jpc2hydXN0aWMiLCJhIjoiY2ttOGJuNXYzMTZvZjJ1b2YwczVhaWcyaSJ9.kXEEoZ9Vt_lvQRdsy2v5hg"
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox( 

            lat=['38.91427','40.6943','34.1139',
                '38.92239','32.7936','42.3188',
                '25.7839','27.9942','40.6501',
                '45.4779','39.5032','32.6619',
                '38.91275'],
            lon=['-77.02827','-73.9249','-118.4068',
                '-77.04227','-96.7662','-71.0846',
                '-80.2102','-82.4451','-73.9496',
                '-122.8168','-84.366','-97.2662',
                '-77.01239'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                color='rgb(255, 0, 0)',
                opacity=0.7,
                size=14
            ),
            text=["The coffee bar","Bistro Bohem","Black Cat",
                "Snap","Columbia Heights Coffee","Azi's Cafe",
                "Blind Dog Cafe","Le Caprice","Filter",
                "Peregrine","Tryst","The Coupe",
                "Big Bear Cafe"],
        ))
    # pio.kaleido.scope.mapbox_access_token=mapbox_access_token
    
    fig.update_layout(
        title='Bubble Size',
        autosize=True,
        hovermode='closest',
        showlegend=True,
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            style="outdoors",
            center=dict(
                lat=38,
                lon=-94
            ),
            pitch=0,
            zoom=2.5
        ),
    )
    fig.update_layout(legend_itemsizing='trace')
    #fig.update_traces(showlegend=True)
    fig.update_layout(legend_title='City<br>Point Layer<br><br><br><b> Bubble Size </b>')
    
    map_path="scripts/ppt_generation/ppts/image_1.png"
    fig.write_image('scripts/book.jpeg')
    fig.show()
    
if __name__=="__main__":
    print("main module")
    main()