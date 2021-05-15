import React, {Component} from "react";
import { connect } from "react-redux";
import { TiArrowRightThick } from "react-icons/ti";

import DataTable from "./data-table.component";

var blueColor = "linear-gradient(to right, rgb(233, 100, 67)";
var redColor = "linear-gradient(to right, rgb(41, 128, 185), rgb(44, 62, 80))"
class MonitorComponent extends Component {
 
    
    state = {
        isRunning:false,
        elapsedTime:0,
        isMonitoring:false,
        rows: [],
    };

    
    componentDidMount() {
        this.intervalId = setInterval(() => this.tick(), 1000);
        this.spreadId = setInterval(() => this.feed_spread(), 5000);
        window.addEventListener("beforeunload", (event) => {
            event.preventDefault();
            this.stop_monitor();
        });
    } 


    componentWillUnmount() {
        clearInterval(this.intervalId);
        clearInterval(this.spreadId);
        this.props.action("stop").then().catch();
    }


    handleStopWatch = () => {
        this.setState({isRunning : !this.state.isRunning});
        if (!this.state.isRunning) {
            this.setState({ previousTime: Date.now() });
            if (!this.state.isMonitoring) {
                this.start_monitor();
            }
        } else {
            this.stop_monitor();
        }
    };


    start_monitor() {
        this.setState({ isMonitoring: true });
        this.props.action("start");
    }


    stop_monitor() {
        this.props.action("stop");
        this.setState({ isMonitoring: false});
    }


    tick = () => {
        if (this.state.isRunning) {
            const now = Date.now();
            this.setState({
                previousTime: now,
                elapsedTime: (
                    this.state.elapsedTime + (now - this.state.previousTime)
                )
            })
        }
    };


    reset = () => this.setState({isRunning: false, elapsedTime: 0});


    feed_spread = () => {
        if (this.state.isMonitoring) {
            this.props.service()
                .then(response => {
                    this.setState({
                        rows: response.data['tri_spreads']
                    });
                    console.log(this.state.rows);
                })
                .catch(error => {
                    console.log(error);
                })
        }
    };


    render() {
        return (
            <div className="monitor-wrapper" >
                <table className="monitor-stats-table d-flex flex-row" style={{margin:"5px"}}>
                    <thead>
                        <tr>
                            <th>
                                <ul style={{listStyle:"none",textAlign: "justify",margin:"0",padding:"0"}}>
                                <li>
                                    <button className="monitor-timer-button"
                                        style={{
                                            background: this.state.isRunning ? blueColor : redColor,
                                            color: 'white'
                                        }} 
                                        onClick={this.handleStopWatch}>
                                        {this.state.isRunning ? 'Stop' : 'Start'}
                                    </button>
            </li>
            <li>
                                    <button className="monitor-timer-button"
                                        color="primary"
                                        style={{background:"linear-gradient(to right, rgb(247, 151, 30), rgb(255, 210, 0))"}}
                                        onClick={this.reset}>
                                        Reset
                                    </button>
            </li>
            </ul>
                            </th>
                        </tr>
                    </thead>
                    <tbody style={{ marginLeft:"10px", color: "white",marginTop:"15px"}}>
                        <tr className="mt-1" style={{ background:"linear-gradient(to right, rgb(35, 7, 77), rgb(204, 83, 51))",borderRadius: "5px"}}>
                            <td className="pl-2">Time <TiArrowRightThick /></td>
                            <td>
                                <span 
                                    className="monitor-time">
                                    <span style={{ fontSize:"2em",background: this.state.isMonitoring ? 'royalblue' : 'crimson', color: "white"}}>
                                    {Math.floor(this.state.elapsedTime / 1000)}
                                </span></span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <DataTable rows={this.state.rows} columns={this.props.columns} />
            </div>
        )
    }
}


function mapStateToProps(state) {
    const { user } = state.auth;
    return {
      user
    }
}


export default connect(mapStateToProps)(MonitorComponent);
