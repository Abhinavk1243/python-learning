from pptx.enum.dml import MSO_COLOR_TYPE, MSO_THEME_COLOR_INDEX
from scripts.webscrapping.test_webscrap import get_blog_data
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData ,ChartData
from pptx.enum.chart import XL_CHART_TYPE,XL_TICK_MARK,XL_LEGEND_POSITION,XL_DATA_LABEL_POSITION

from pptx.util import Inches,Pt
import pandas as pd
from scripts.pandas_files.itter_rows import get_tuple_list
# title_id=[]
# slide=[]
# placeholders_id=[]
prs=Presentation("scripts/ppt_generation/ppts/input_4.pptx")
# for i in range(len(prs.slides)):
#   for shape in prs.slides[i].placeholders:
#     print('%d %d %s' % (i,shape.placeholder_format.idx, shape.name))
    
# for index,slide in enumerate(prs.slides):
# for shape in prs.slides[5].shapes.placeholders:
#   print('%d %s' % (shape.placeholder_format.idx, shape.name))

shape_name={}
funct_dict={}
for index,i in  enumerate(prs.slides[24].shapes):
  # print(f"id:{index} , name : {i.name}, shape_type :{i.shape_type} ")
  shape_name.update({i.name:[index,str(i.shape_type)]})
  funct_dict.update({i.name:index})
  
  
print(shape_name)

# print(table.cell(1,1).text)

# print(funct_dict)
# data={"Addition":["145","190","133","94","179","206","78"],
# "Removals":["-1.24%","-11.3%","-4.5%","-1.21%","-1.05%","-9.0%","-5.1%"]}
# df=pd.DataFrame(data)
# print(df["Addition"].dtype)

# print(prs.slides[19].shapes[6])
  
# for shape in prs.slides[19].placeholders:
#   print('%d %s' % ( shape.placeholder_format.idx, shape.name))

  
  
# slide=prs.slides[5].shapes[8].name
# for chart in prs.slides[12].shapes:
#   print(chart)
# print(slide)


# prs.save("slide5.pptx")

# slide=prs.slides[19]
# shape=slide.shapes[10]
# chart=shape.chart
# chart_data = ChartData()
# chart_data.categories =["A","B","C","D","E"]
# chart_data.add_series("sales1",(234,453,100,600,540))
# chart_data.add_series("sales2",(560,290,680,220,320))
# chart.replace_data(chart_data)

# prs.save("slide13.pptx")


# df=pd.read_csv("scripts/ppt_generation/chart.csv")

# print(df.to_dict("list"))
# df= pd.read_csv('scripts/pandas_files/csvfiles/uscities.csv')


# os.path.join(os.path.expanduser("~"),'config/sqlcred.cfg
from pptx.enum.dml import MSO_COLOR_TYPE, MSO_THEME_COLOR
print( MSO_THEME_COLOR.ACCENT_1)