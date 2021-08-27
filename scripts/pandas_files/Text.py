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
prs=Presentation("scripts/ppt_generation/themes/sharecare_temp.pptx")
# for i in range(len(prs.slides)):
#   for shape in prs.slides[i].placeholders:
#     print('%d %d %s' % (i,shape.placeholder_format.idx, shape.name))
    
# for index,slide in enumerate(prs.slides):
#   for shape in slide.placeholders:
#     print('%d %d %s' % (index,shape.placeholder_format.idx, shape.name))


for i in  prs.slides[4].shapes:
  print(i.name)