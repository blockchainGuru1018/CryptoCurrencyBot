import React, {Component} from "react";
import {connect} from "react-redux";
import { Redirect } from "react-router-dom";

import { Col } from "react-bootstrap";

import ArbitrageService from "../services/arbitrage.service";
import PageTitle from "./page-title.component";
import MonitorStart from "./monitor-start.component";
import MonitorService from "../services/monitor.service";


class InterExchangeDataTable extends Component {
    
     
    render() {
        
        const columns = [{}, {}]

        const { user: current_user } = this.props;
        if (!current_user) {
            return <Redirect to="/login" />;
        }

        return (
            <>
                <Col lg={12}>
                    <PageTitle title={"Inter Exchange Monitor"}/>
                </Col>
                <Col lg={12}>
                    <MonitorStart
                        columns={columns}
                        action={MonitorService.inter_exchange_monitor} 
                        service={ArbitrageService.get_inter_exchange_arbitrage}>
                    </MonitorStart>
                </Col>
            </>
        )
    }
}


function mapStateToProps(state) {
    const { user } = state.auth;
    return { user };
}

export default connect(mapStateToProps)(InterExchangeDataTable);
