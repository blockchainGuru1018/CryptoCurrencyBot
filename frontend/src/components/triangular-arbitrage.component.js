import React, {Component} from "react";
import {connect} from "react-redux";

import { Col } from "react-bootstrap";

import ArbitrageService from "../services/arbitrage.service";
import PageTitle from "./page-title.component";
import AnimationComponent from "./animation.component";
import MonitorStart from "./monitor-start.component";
import MonitorService from "../services/monitor.service";
import LoadingScreen from "./loading-screen.component";
const columns =  [
    { field: "tri_spread", headerName: "Spread", width: 200},
    { field: "recorded_date", headerName: "Recorded Date", width: 160},
    { field: "tri_exchange_buy1_id", headerName: "Buy1 ID", width: 100},
    { field: "tri_exchange_buy2_id", headerName: "Buy2 ID", width: 100},
    { field: "tri_exchange_sell_id", headerName: "Sell ID", width: 100},

    { field: "tri_xchange_buy1_name", headerName: "Buy1 Name", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy1.name},
    { field: "tri_xchange_buy1_currency_pair", headerName: "Buy1 Currency Pair", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy1.currency_pair},
    { field: "tri_xchange_buy1_last_ask_price", headerName: "Buy1 Last Price", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy1.last_ask_price},
    { field: "tri_xchange_buy1_last_bid_price", headerName: "Buy1 Bid Price", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy1.last_bid_price},

    { field: "tri_xchange_buy2_name", headerName: "Buy2 Name", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy2.name},
    { field: "tri_xchange_buy2_currency_pair", headerName: "Buy2 Currency Pair", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy2.currency_pair},
    { field: "tri_xchange_buy2_last_ask_price", headerName: "Buy2 Last Price", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy2.last_ask_price},
    { field: "tri_xchange_buy2_last_bid_price", headerName: "Buy2 Bid Price", width: 160, valueFormatter: ({ data }) => data.tri_xchange_buy2.last_bid_price},

    { field: "tri_xchange_sell_name", headerName: "Sell Name", width: 160, valueFormatter: ({ data }) => data.tri_xchange_sell.name},
    { field: "tri_xchange_sell_currency_pair", headerName: "Sell Currency Pair", width: 160, valueFormatter: ({ data }) => data.tri_xchange_sell.currency_pair},
    { field: "tri_xchange_sell_last_ask_price", headerName: "Sell Last Price", width: 160, valueFormatter: ({ data }) => data.tri_xchange_sell.last_ask_price},
    { field: "tri_xchange_sell_last_bid_price", headerName: "Sell Bid Price", width: 160, valueFormatter: ({ data }) => data.tri_xchange_sell.last_bid_price},
];

class TriangularComponent extends Component {
    state = {loading: true}
    componentDidMount(){
        this.loadData();
      }
    constructor(props) {
        super(props);
    }
    loadData(){
        var self = this;
        setTimeout(function(){
            self.setState({ loading: false }); //Here its supposed to load some data and set loading to false later so we use the loading screen
        },5000);
    }
    
    render() {
        if(this.state.loading){
          return ( <LoadingScreen /> );
        } else {
            return (
                <>
                    <Col lg={12}>
                        <PageTitle title={"Triangular Monitor"}/>
                    </Col>
                    <Col lg={12}>
                        <MonitorStart
                            columns={columns}
                            action={MonitorService.triangular_exchange_monitor}
                            service={ArbitrageService.get_triangular_exchange_arbitrage}/>
                    </Col>
                <div style={{ display: "flex", justifyContent: "center", width:"100%"}}>
                    <Col >
                        <div id="animationWrapper">
                        <AnimationComponent />
                        </div>
                    </Col>
                </div>
                  <bouncingCoin />
                </>
            )
        }
    }
}



function mapStateToProps(state) {
    const { user } = state.auth;
    return {
      user,
    };
}


export default connect(mapStateToProps)(TriangularComponent);
