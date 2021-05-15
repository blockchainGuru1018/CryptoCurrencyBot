import React, {Component} from "react";
import "../animationStyles.css";
import disintegrate from "disintegrate"
class AnimationComponent extends Component {
    componentDidMount() {
        
        this.init();
           
    }
    constructor(props) {
        super(props);
        disintegrate.init(); 
        this.etheriumElem = React.createRef();
        this.bitcoinElem = React.createRef();
        this.rippleElem = React.createRef();
    }
    init() {
        var animCol = document.getElementById("animationWrapper").parentElement;
        animCol.style.maxWidth = "720px";
        animCol.style.minWidth = "250px";
        
        this.etheriumElem = document.getElementById("etherium");
        this.bitcoinElem = document.getElementById("bitcoin");
        this.rippleElem = document.getElementById("ripple");
        this.setupAnimation(0);
        this.setHeights();
    }
setHeights() {
    var countSpans = document.getElementsByClassName("count");
    for(var z=0; z<countSpans.length; z++) {
        countSpans[z].style.height = Math.trunc(Math.random()*100)+"%";//style="height: 49%;"
    }
    var coinContainers = document.getElementsByClassName("coinContainer");
    for(var i=0; i<coinContainers.length; i++) {
      var coinContainer = coinContainers[i];
      coinContainer.addEventListener('click', function (event) {
        var coin = event.currentTarget.children[0];
        var flipResult = Math.random();
          coin.classList.remove("heads")
          coin.classList.remove("tails")
        setTimeout(function(){
          if(flipResult <= 0.5){
            coin.classList.add("heads");
          }
          else{
            coin.classList.add("tails");
          }
        }, 100);
      });
    }
}
setupAnimation(num) {
    try {
        var elem1, elem2, name;
        var nextNum = num+1;
        if(nextNum >= 3) {
            nextNum = 0;
        }
        switch(num) {
            case 0: {
                elem1 = this.etheriumElem;
                elem2 = this.bitcoinElem;
                name = "Bitcoin";
                break;
            }
            case 1: {
                elem1 = this.bitcoinElem;
                elem2 = this.rippleElem;
                name = "Ripple";
                break;
            }
            case 2: {
                elem1 = this.rippleElem;
                elem2 = this.etheriumElem;
                name = "Etherium";
                break;
            }
            default: break;
        }
        this.recalculateAnimation(name,elem1,elem2,name.toLowerCase()+"Button",nextNum);
        document.getElementById(name.toLocaleLowerCase()+"CoinContainer").click();
    } catch(e) {
        console.log(e);
    }
    
}

recalculateAnimation(name, component1, component2, coinId,num) {
    if(coinId) {
        document.getElementById(coinId).animate([
            {transform: "translateX(50px)"}
        ], {
            duration:1000,
            iterations:1
        }
        );
    }
    var movement = this.calculateMovement(component1,component2);
    component1.animate([
      { opacity: '0.3' }, 
      { transform: "translate3d("+movement.left+"px, "+movement.top+"px, 0)" }
    ], {
        id: name,
        duration: 1000,
        iterations:1
    });
    var self = this;
    setTimeout(function(){ self.setupAnimation(num) }, 1000); 
}
calculateMovement(component1, component2) {
    var movement = {left:-(component1.getBoundingClientRect().left-component2.getBoundingClientRect().left), top: -(component1.getBoundingClientRect().top-component2.getBoundingClientRect().top)};
    return movement;
}
    render() {
        return <div><ul className="sparklist" id="binance">
      <li>
          <span>Binance</span>
        <span className="sparkline">
          <span className="index">
              <span className="count">(60,</span>
          </span>
          <span className="index"><span className="count">220,</span> </span>
          <span className="index"><span className="count">140,</span> </span>
          <span className="index"><span className="count">80,</span> </span>
          <span className="index"><span className="count">110,</span> </span>
          <span className="index"><span className="count">90,</span> </span>
          <span className="index"><span className="count">180,</span> </span>
          <span className="index"><span className="count">140,</span> </span>
          <span className="index"><span className="count">120,</span> </span>
          <span className="index"><span className="count">160,</span> </span>
          <span className="index"><span className="count">175,</span> </span>
          <span className="index"><span className="count">225,</span> </span>
          <span className="index"><span className="count">175,</span> </span>
          <span className="index"><span className="count">125)</span> </span>
        </span>
          <div className="spinMoveCoins">
          <div data-dis-container id="etheriumCoinContainerFix" className="coin-container">
            <button data-dis-type="contained" id="etheriumButton" className="CSS-animation-2">
              <div className="coinContainerSpin">
                <div className="miniEtherium"></div>
              </div>
            </button>
        </div>
          <div id="etheriumCoinContainer" className="coinContainer">
                <div className="coin">
                  <div className="side-a">
                      <div className="side-a-back"></div>
                    </div>
                  <div className="side-b">
                    <div className="side-a-back"></div>
                  </div>
                </div>
            </div>
          </div>
      </li>
    </ul>
    <div data-dis-container id="animationContainer" className="middle-container section-container">
        <div data-dis-type="contained" ref="etheriumAnimation" className="CSS-animation second-animation">
            <div id="etherium">
                <div className="animatedCoin">
                  <div className="side-a">
                      <div className="side-a-back"></div>
                    </div>
                  <div className="side-b">
                    <div className="side-a-back"></div>
                  </div>
                </div>
            </div>
        </div>
        <div data-dis-type="contained" className="CSS-animation third-animation">
            <div id="bitcoin">
                <div className="animatedCoin">
                  <div className="side-a">
                      <div className="side-a-back"></div>
                    </div>
                  <div className="side-b">
                    <div className="side-a-back"></div>
                  </div>
                </div>
            </div>
        </div>
        <div data-dis-type="contained" className="CSS-animation fourth-animation">
            <div id="ripple">
                <div className="animatedCoin">
                  <div className="side-a">
                      <div className="side-a-back"></div>
                    </div>
                  <div className="side-b">
                    <div className="side-a-back"></div>
                  </div>
                </div>
            </div>
        </div>
    </div>
        <ul className="sparklist" id="biitrex">
      <li>
          
        <span>Biitrex</span>
        <span className="sparkline">
          <span className="index">
              <span className="count">(60,</span>
          </span>
          <span className="index"><span className="count">220,</span> </span>
          <span className="index"><span className="count">140,</span> </span>
          <span className="index"><span className="count">80,</span> </span>
          <span className="index"><span className="count">110,</span> </span>
          <span className="index"><span className="count">90,</span> </span>
          <span className="index"><span className="count">180,</span> </span>
          <span className="index"><span className="count">140,</span> </span>
          <span className="index"><span className="count">120,</span> </span>
          <span className="index"><span className="count">160,</span> </span>
          <span className="index"><span className="count">175,</span> </span>
          <span className="index"><span className="count">225,</span> </span>
          <span className="index"><span className="count">175,</span> </span>
          <span className="index"><span className="count">125)</span> </span>
        </span>
          <div className="spinMoveCoins">
              <div data-dis-container className="coin-container">
            <button data-dis-type="contained" id="bitcoinButton" className="CSS-animation-2">
              <div className="coinContainerSpin">
                    <div className="miniBitcoin"></div>
              </div>
            </button>
        </div>
          <div id="bitcoinCoinContainer" className="coinContainer">
                <div className="coin">
                  <div className="side-a">
                      <div className="side-a-back"></div>
                    </div>
                  <div className="side-b">
                    <div className="side-a-back"></div>
                  </div>
                </div>
            </div>
          </div>
        
      </li>
    </ul>
    <ul className="sparklist" id="kucoin">
      <li>
        <span>kucoin</span>
        <span className="sparkline">
          <span className="index">
              <span className="count">(60,</span>
          </span>
          <span className="index"><span className="count">220,</span> </span>
          <span className="index"><span className="count">140,</span> </span>
          <span className="index"><span className="count">80,</span> </span>
          <span className="index"><span className="count">110,</span> </span>
          <span className="index"><span className="count">90,</span> </span>
          <span className="index"><span className="count">180,</span> </span>
          <span className="index"><span className="count">140,</span> </span>
          <span className="index"><span className="count">120,</span> </span>
          <span className="index"><span className="count">160,</span> </span>
          <span className="index"><span className="count">175,</span> </span>
          <span className="index"><span className="count">225,</span> </span>
          <span className="index"><span className="count">175,</span> </span>
          <span className="index"><span className="count">125)</span> </span>
        </span>
          <div className="spinMoveCoins">
          <div data-dis-container className="coin-container">
            <button data-dis-type="contained" id="rippleButton" className="CSS-animation-2">
              <div className="coinContainerSpin">
                <div className="miniRipple"></div>
              </div>
            </button>
        </div>
        <div id="rippleCoinContainer" className="coinContainer">
                <div className="coin">
                  <div className="side-a">
                      <div className="side-a-back"></div>
                    </div>
                  <div className="side-b">
                    <div className="side-a-back"></div>
                  </div>
                </div>
            </div>
          </div>
      </li>
        
    </ul>
    </div>
    }
}

export default AnimationComponent;