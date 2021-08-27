from scripts.webscrapping.test_webscrap import get_blog_data
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData ,XyChartData
from pptx.enum.chart import XL_CHART_TYPE,XL_TICK_MARK,XL_LEGEND_POSITION,XL_DATA_LABEL_POSITION

from pptx.util import Inches,Pt
import pandas as pd
from scripts.pandas_files.itter_rows import get_tuple_list


prs=Presentation("scripts/ppt_generation/themes/theme.pptx")

title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
slide.shapes.title.text = "PPT generation using python"
body_shape=slide.shapes.placeholders[11]
text_frame=body_shape.text_frame
text_frame.text="By Abhinav"

#remove placeholder of idx: 11
textbox =slide.shapes.placeholders[10]
sp = textbox.element
sp.getparent().remove(sp)

## table of content 
reporting_slide = prs.slide_layouts[2]
slide = prs.slides.add_slide(reporting_slide)
slide.shapes.title.text = "Table of Content"
textbox =slide.shapes.placeholders[10]
sp = textbox.element
sp.getparent().remove(sp)

left =Inches(1)
top=Inches(1) 
width=Inches(1)
height = Inches(1)
txBox = slide.shapes.add_textbox(left, top, width, height)

table_content={'Executive Summary':['Program Overview'],
   'Eligibility and Registration':['Eligibility Trends' ,'Demographics and Data Quality' , 'Registration and RealAge Completion', 'Registration and RealAge Completion by Group'], 
   'Health Insights':['RealAge Results', 'Risk Analysis Summary', 'Biometric Screening Participation', 'Biometric Screening Results'], 
   'Digital Engagement':['Overall Platform Activity', 'Feature Utilization', 'Content Consumption', 'Green Day Tracking', 'Challenge Participation', 'Challenge Details', 'Incentive Earning'], 
   'Program Engagement':['High-touch Lifestyle Management Participation​']}

left =Inches(1)
top=Inches(1) 
width=Inches(1.5)
height = Inches(0.5)
for index,key in enumerate(table_content.keys()):
    if index==3:
        left =Inches(7)
        top=Inches(1)
        width=Inches(1.5)
        height = Inches(0.5)
    
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.text =f"{index+1} {key}"
    for i in table_content[key]:
        
        if index >= 3:
            left =Inches(7.5)
            top=top+Inches(0.3)
            width=Inches(1.5)
            height = Inches(0.5)
        
        else:
            left =Inches(1.6)
            top=top+Inches(0.3)
            width=Inches(1.5)
            height = Inches(0.5)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.text =i
        tf.level=1
    
    
    
    if index>=3:
        left =Inches(7)
        top=top+Inches(0.4)
        width=Inches(1.5)
        height = Inches(0.5)
        
    
    elif index<3:
        left =Inches(1)
        top=top+Inches(0.4)
        width=Inches(1.5)
        height = Inches(0.5)
        

## sperator 
seperator_slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(seperator_slide_layout)
slide.shapes.title.text = "Summary"

## Graph
reporting_slide=prs.slide_layouts[2]
slide = prs.slides.add_slide(reporting_slide)
slide.shapes.title.text = "Graphical Representation"
textbox =slide.shapes.placeholders[10]
sp = textbox.element
sp.getparent().remove(sp)

graph_data=CategoryChartData()
graph_data.categories=["Jan","Feb","March"]
graph_data.add_series('Q1 Sales', (19.2, -21.4, 16.7))
graph_data.add_series('Q2 Sales', (2220, 2860, 152))
# graph_data.add_series('Q3 Sales', (20.4, 26.3, 14.2))
x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5) 
chart=slide.shapes.add_chart( XL_CHART_TYPE.COLUMN_STACKED, x,y, cx, cy, graph_data ).chart

# graph_data.add_series('Q2 Sales', (1452, 2044, 1687))
# x, y, cx, cy = Inches(5), Inches(2), Inches(6), Inches(4.5) 
# chart=slide.shapes.add_chart( XL_CHART_TYPE.LINE, x,y, cx, cy, graph_data ).chart


prs.save('scripts/ppt_generation/test_theme.pptx')