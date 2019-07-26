const API_HOST='http://localhost:5000'

const Adapter = {

    readDf: function() {
        return fetch(`${API_HOST}/df`, {
            method: 'GET'
        }).then(res => res.json())
    },
    READ_STATS: function() {
        return fetch(`${API_HOST}/dfstats`, {
            method: 'GET'
        }).then(res => res.json())
    },
    READ_PLOT: function() {
        return fetch(`${API_HOST}/dfplot`, {
            method: 'GET'
        }).then(res => res.json())
    }
}

export default Adapter