import React from 'react';
import './App.css';
import Adapter from './Adapter.js';
import PubFormat from './Components/PubFormat'
import ReactHtmlParser, { processNodes, convertNodeToElement, htmlparser2 } from 'react-html-parser';

class App extends React.Component {

  state = {
    data:[],
    stats:[],
    plot:[],
    pubs:[]
  }

  _sendRequest = () => {
    Adapter.readDf()
      .then(res => {
        this.setState({
          data:res,
          pubs:res.data[0].df_pubs
      })
    })
  }

  _sendStatsRequest = () => {
    Adapter.READ_STATS()
      .then(res => {
        this.setState({
          stats:res
        })
      })
  }

  _sendPlotRequest = () => {
    Adapter.READ_PLOT()
      .then(res => {
        this.setState({
          plot:res
        })
      })
  }
  _renderPubs = () => {
    const { pubs } = this.state
    return pubs.map(pub =>  {
      return <PubFormat pub={pub} />
    })
  }

  render() {
    const { data,stats,plot,pubs } = this.state
    console.log(pubs)
    // data.data ? console.log(data.data[0].df_pubs) : console.log("not ready")

    return (
      <div className="App">
        <header className="App-header">
          <button
            className='btn btn-default'
            onClick={this._sendRequest}
            >
              PRESS
          </button>

        <div>
        {data.length == 0 ? 
          null :
          <span>
            <h3>
            {data.data[0].df_stats[0] + " rows X " + data.data[0].df_stats[1] + " columns"}
            </h3>
            <p>(Displaying first 30 rows)</p>
          </span>
        }
        </div>
        
        <div className='data-row'>
        <span id='dataDf'>
          {data.length == 0 ? 
            null :
            
             ReactHtmlParser(data.data[0].df_html)
          }
        </span>
        {data.length === 0 ? 
          null :
          <span className='publisher-list'>
            <p>Publishers in Network (if applicable)</p>
            <table>
            {this._renderPubs()}
            </table>
          </span>
        }
        </div>

        <button
            className='btn btn-default'
            onClick={this._sendStatsRequest}
            >
              PRESS
          </button>
          <span id='dataDfStats'>
          {stats.length === 0 ? 
            null :
            
             ReactHtmlParser(stats.data[0].df_html)
          }
        </span>
        <button
            className='btn btn-default'
            onClick={this._sendPlotRequest}
            >
              PRESS
          </button>
          <span id='dataDfPlot'>
          {plot.length === 0 ? (
            null
            ) : (
            <img src={plot}/>
            )
          }
        </span>
        </header>
      </div>
    )
  };
}


export default App;
