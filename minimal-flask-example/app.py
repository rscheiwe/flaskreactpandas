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

@app.route("/df")
def dataframe():
    template = render_template('df2.html.j2', dataframe = df.head(30).to_html())
    df_pubs = []
    if not df.empty:
        # use .tolist() so that nparray is JSON serializable
        df_pubs = df.name.unique().tolist()

    response_object = {
        'state':'success',
        'message':'dataframe successfully processed',
        'data': [{
                'data': df.to_json(),
                'df_stats':df.shape,
                'df_pubs':df_pubs,
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
