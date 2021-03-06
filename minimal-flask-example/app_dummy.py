from bokeh.embed import components
from flask import Flask, render_template
from flask import jsonify
# added
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from io import BytesIO
import base64
# done added
import bokeh
import pandas as pd
from util import make_plot
import json

# df = pd.read_csv(
#     "https://data.boston.gov/dataset/c8b8ef8c-dd31-4e4e-bf19-af7e4e0d7f36/resource/29e74884-a777-4242-9fcc-c30aaaf3fb10/download/economic-indicators.csv",
#     parse_dates=[["Year", "Month"]],
# )
df = pd.read_csv('static/tribunedigital_pv_data.csv')
length = len(df)
app = Flask(__name__)

# added
html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
'''


@app.route("/")
def home():
    return render_template("index.html.j2")

@app.route("/bokehplot")
def bokehplot():
    figure = make_plot()
    fig_script, fig_div = components(figure)
    template=render_template(
        "bokeh.html.j2",
        fig_script=fig_script,
        fig_div=fig_div,
        bkversion=bokeh.__version__,
    )
    response_object = {
        'state':'success',
        'message':'dataframe plot successfully processed',
        'data': [{
                'data': df.to_json(),
                'plot_html':template
                }]
    }
    return jsonify(response_object)
    # return render_template(
    #     "bokeh.html.j2",
    #     fig_script=fig_script,
    #     fig_div=fig_div,
    #     bkversion=bokeh.__version__,
    # )

@app.route("/df")
def dataframe():
    # figure = make_plot()
    # fig_script, fig_div = components(figure)
    # print(df)
    # return df[df.columns[:4]].head().to_json()
    # return jsonify(render_template("df2.html.j2", 
            # fig_script=fig_script,
            # fig_div=fig_div,
            # bkversion=bokeh.__version__,
            # length=length, 
            # dataframe=df.to_html()
            # ))
            # Might just be able to send this forward and render it
            # dataframe=df.head().to_html()
    template = render_template('df2.html.j2', dataframe = df.head(30).to_html())
    response_object = {
        'state':'success',
        'message':'dataframe successfully processed',
        'data': [{
                'data': df.to_json(),
                'df_stats':df.shape,
                'df_html':template
                }]
    }
    return jsonify(response_object)

@app.route("/dfstats")
def dfstats():
    template = render_template('df2.html.j2', dataframe = df.describe()
                                                            .astype(object)
                                                            .transpose()
                                                            .to_html())
    response_object = {
        'state':'success',
        'message':'dataframe statistics successfully processed',
        'data': [{
                'data': df.describe().to_json(),
                'df_html':template
                }]
    }
    return jsonify(response_object)


@app.route("/dfplot")
def dfplot():
    df = pd.DataFrame(
        {'y':np.random.randn(10), 'z':np.random.randn(10)},
        index=pd.period_range('1-2000',periods=10),
    )
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df.plot(ax=ax)

    io = BytesIO()
    fig.savefig(io, format='png')
    data = base64.encodestring(io.getvalue()).decode('utf-8')
    html = 'data:image/png;base64,{}'
    return jsonify(html.format(data))

@app.route("/dfcustom")
def dfcustom():
    data = df.to_dict(orient="records")
    headers = df.columns
    print(headers)
    return render_template("dfcustom.html.j2", data=data, headers=headers)


if __name__ == "__main__":
    app.run(debug=True, port=5957)
