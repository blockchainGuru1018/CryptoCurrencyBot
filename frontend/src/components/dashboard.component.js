import React, { PureComponent } from "react";
import { Redirect } from 'react-router-dom';
import { connect } from "react-redux";

import {Col} from "react-bootstrap"; 


class Dashboard extends PureComponent {

    render() {
        const { user: current_user } = this.props;
        
        if (!current_user) {
            return <Redirect to="/login" />;
        }
        
        return (
            <Col lg={12}>
                <p>Hit the menu on the top right</p>
            </Col>
        );
    }
}


function mapStateToProps(state) {
    const { user } = state.auth;
    return {
      user,
    };
}
  
export default connect(mapStateToProps)(Dashboard);