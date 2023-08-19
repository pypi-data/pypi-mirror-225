import os
import streamlit.components.v1 as components


_RELEASE = True

if not _RELEASE:
    _Pie_Chart_Nivo = components.declare_component(
       
        "Pie_Chart_Nivo",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend-react/build")
    _Pie_Chart_Nivo = components.declare_component("Pie_Chart_Nivo", path=build_dir)

def Pie_Chart_Nivo(ChartData=None, largeScreenLayout=None, smallScreenLayout=None, styles=None, key=None):

    component_value = _Pie_Chart_Nivo(ChartData=ChartData, largeScreenLayout=largeScreenLayout, smallScreenLayout=smallScreenLayout, styles=styles, key=key, default=0)

    return component_value

if not _RELEASE:
    import streamlit as st
    st.set_page_config(layout="wide")

    slideOneMoreDetailsData = [
        {
        "index": 0,
        "indexName": "category",
        "data": [
            {
            "id": "scala",
            "label": "scala",
            "value": 393,
            "color": "hsl(148, 70%, 50%)"
            },
            {
            "id": "elixir",
            "label": "elixir",
            "value": 579,
            "color": "hsl(142, 70%, 50%)"
            },
            {
            "id": "rust",
            "label": "rust",
            "value": 340,
            "color": "hsl(189, 70%, 50%)"
            },
            {
            "id": "php",
            "label": "php",
            "value": 482,
            "color": "hsl(263, 70%, 50%)"
            },
            {
            "id": "haskell",
            "label": "haskell",
            "value": 515,
            "color": "hsl(72, 70%, 50%)"
            }
        ]
        },
        {
        "index": 1,
        "indexName": "features",
        "data": [
            {
            "id": "scala",
            "label": "scala",
            "value": 393,
            "color": "hsl(148, 70%, 50%)"
            },
            {
            "id": "elixir",
            "label": "elixir",
            "value": 579,
            "color": "hsl(142, 70%, 50%)"
            },
            {
            "id": "rust",
            "label": "rust",
            "value": 340,
            "color": "hsl(189, 70%, 50%)"
            },
            {
            "id": "php",
            "label": "php",
            "value": 482,
            "color": "hsl(263, 70%, 50%)"
            },
            {
            "id": "haskell",
            "label": "haskell",
            "value": 515,
            "color": "hsl(72, 70%, 50%)"
            }
        ]
        },
    ]
    largeScreenLayout = {
              "margin":{ "top": 20, "right": 80, "bottom": 60, "left": 80 },
              "innerRadius":0.5,
              "padAngle":0.7,
              "cornerRadius":3,
              "activeOuterRadiusOffset":8,
              "borderWidth":1,
              "borderColor":{
                "from": "color",
                "modifiers": [["darker", 0.2]]
              },
              "arcLinkLabelsSkipAngle":10,
              "arcLinkLabelsTextColor":"#333333",
              "arcLinkLabelsThickness":2,
              "arcLinkLabelsColor":{ "from": "color" },
              "arcLabelsSkipAngle":10,
              "arcLabelsTextColor":{
                "from": "color",
                "modifiers": [["darker", 2]]
              },
              "defs":[
                {
                  "id": "dots",
                  "type": "patternDots",
                  "background": "inherit",
                  "color": "rgba(255, 255, 255, 0.3)",
                  "size": 4,
                  "padding": 1,
                  "stagger": True
                },
                {
                  "id": "lines",
                  "type": "patternLines",
                  "background": "inherit",
                  "color": "rgba(255, 255, 255, 0.3)",
                  "rotation": -45,
                  "lineWidth": 6,
                  "spacing": 10
                }
              ],
              "fill":[
                {
                  "match": {
                    "id": "ruby"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "c"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "go"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "python"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "scala"
                  },
                  "id": "lines"
                },
                {
                  "match": {
                    "id": "lisp"
                  },
                  "id": "lines"
                },
                {
                  "match": {
                    "id": "elixir"
                  },
                  "id": "lines"
                },
                {
                  "match": {
                    "id": "javascript"
                  },
                  "id": "lines"
                }
              ],
              "legends":[
                {
                  "anchor": "bottom",
                  "direction": "row",
                  "justify": False,
                  "translateX": 0,
                  "translateY": 45,
                  "itemsSpacing": 0,
                  "itemWidth": 50,
                  "itemHeight": 18,
                  "itemTextColor": "#999",
                  "itemDirection": "left-to-right",
                  "itemOpacity": 1,
                  "symbolSize": 18,
                  "symbolShape": "circle",
                  "effects": [
                    {
                      "on": "hover",
                      "style": {
                        "itemTextColor": "#000"
                      }
                    }
                  ]
                }
              ]
    }
    smallScreenLayout = {
              "margin":{ "top": 40, "right": 80, "bottom": 70, "left": 80 },
              "innerRadius":0.5,
              "padAngle":0.7,
              "cornerRadius":3,
              "activeOuterRadiusOffset":8,
              "borderWidth":1,
              "borderColor":{
                "from": "color",
                "modifiers": [["darker", 0.2]]
              },
              "arcLinkLabelsSkipAngle":10,
              "arcLinkLabelsTextColor":"#333333",
              "arcLinkLabelsThickness":2,
              "arcLinkLabelsColor":{ "from": "color" },
              "arcLabelsSkipAngle":10,
              "arcLabelsTextColor":{
                "from": "color",
                "modifiers": [["darker", 2]]
              },
              "defs":[
                {
                  "id": "dots",
                  "type": "patternDots",
                  "background": "inherit",
                  "color": "rgba(255, 255, 255, 0.3)",
                  "size": 4,
                  "padding": 1,
                  "stagger": True
                },
                {
                  "id": "lines",
                  "type": "patternLines",
                  "background": "inherit",
                  "color": "rgba(255, 255, 255, 0.3)",
                  "rotation": -45,
                  "lineWidth": 6,
                  "spacing": 10
                }
              ],
              "fill":[
                {
                  "match": {
                    "id": "ruby"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "c"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "go"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "python"
                  },
                  "id": "dots"
                },
                {
                  "match": {
                    "id": "scala"
                  },
                  "id": "lines"
                },
                {
                  "match": {
                    "id": "lisp"
                  },
                  "id": "lines"
                },
                {
                  "match": {
                    "id": "elixir"
                  },
                  "id": "lines"
                },
                {
                  "match": {
                    "id": "javascript"
                  },
                  "id": "lines"
                }
              ],
              "legends":[
                {
                  "anchor": "bottom",
                  "direction": "row",
                  "justify": False,
                  "translateX": 0,
                  "translateY": 55,
                  "itemsSpacing": 0,
                  "itemWidth": 50,
                  "itemHeight": 18,
                  "itemTextColor": "#999",
                  "itemDirection": "left-to-right",
                  "itemOpacity": 1,
                  "symbolSize": 18,
                  "symbolShape": "circle",
                  "effects": [
                    {
                      "on": "hover",
                      "style": {
                        "itemTextColor": "#000"
                      }
                    }
                  ]
                }
              ]
    }

    chart_columns = st.columns([1,5,1])
    with chart_columns[1]:
        Pie_Chart_Nivo(ChartData=slideOneMoreDetailsData, largeScreenLayout=largeScreenLayout, smallScreenLayout=smallScreenLayout)
