import React, {Component} from "react";
import "../bouncingCoin.css";
class BouncingCoin extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return <div class="stage">
            <div class="bitcoin bounce-7"></div>
    </div>
    }
}

export default BouncingCoin;