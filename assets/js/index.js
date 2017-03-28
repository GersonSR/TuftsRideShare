var React = require('react')
var ReactDOM = require('react-dom')

var UsersList = React.createClass({
    loadUsersFromServer: function(){
        $.ajax({
            url: this.props.url,
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    },

    getInitialState: function() {
        return {data: []};
    },

    componentDidMount: function() {
        this.loadUsersFromServer();
        setInterval(this.loadUsersFromServer, 
                    this.props.pollInterval)
    }, 
    render: function() {
        if (this.state.data) {
            console.log('DATA!')
            var userNodes = this.state.data.map(function(user){
                return <li> {user.username} </li>
            })
        }
        return (
            <div>
                <h1>User List</h1>
                <ul>
                    {userNodes}
                </ul>
            </div>
        )
    }
})

var RidesList = React.createClass({
    loadRidesFromServer: function(){
        $.ajax({
            url: this.props.url,
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    },

    getInitialState: function() {
        return {data: []};
    },

    componentDidMount: function() {
        this.loadRidesFromServer();
        setInterval(this.loadRidesFromServer, 
                    this.props.pollInterval)
    }, 
    render: function() {
        if (this.state.data) {
            console.log('DATA!')
            var rideNodes = this.state.data.map(function(ride){
                return <li> {ride.destination_text} </li>
            })
        }
        return (
            <div>
                <h1>Destination List</h1>
                <ul>
                    {rideNodes}
                </ul>
            </div>
        )
    }
})



ReactDOM.render(<RidesList url='/rides/' pollInterval={1000} />, 
    document.getElementById('rides')
    )