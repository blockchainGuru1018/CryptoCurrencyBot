import React from "react";
import { Link } from "react-router-dom";
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';

import MenuOpenIcon from '@material-ui/icons/MenuOpen';

import { CgArrowsExchangeV } from "react-icons/cg";
import { BsClockHistory } from "react-icons/bs";
import { GiTriangleTarget } from "react-icons/gi";
import { GiDiamondsSmile } from "react-icons/gi";
import { RiLogoutCircleRLine } from "react-icons/ri";


const useStyles = makeStyles({
  list: {
    width: 250,
    background: "linear-gradient(to right, rgb(75, 121, 161), rgb(40, 62, 81))",
    height: "100%",
    borderRight: "1px solid grey"
  },
  fullList: {
    width: 'auto',
    background: "linear-gradient(to right, rgb(20, 30, 48), rgb(36, 59, 85))"
  },
});


export default function TemporaryDrawer(props) {

  const classes = useStyles();
  const [state, setState] = React.useState({
    top: false,
    left: false,
    bottom: false,
    right: false,
  });
  const list_items = [
    ["Triangular Arbitrage", "/triangular-exchange-arbitrage", <GiTriangleTarget/>],
    ["Inter-exchange Arbitrage", "/inter-exchange-arbitrage", <CgArrowsExchangeV />],
    ["Backtest Arbitrage", "/backtest-exchange-arbitrage", <BsClockHistory />]
  ]

  const toggleDrawer = (anchor, open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setState({ ...state, [anchor]: open });
  };


  const navTitle = (current_user) => {
    return (
      <nav className="navbar navbar-expand">
      <Link to={current_user ? "/dashboard" : "/login"} className="navbar-brand" style={{color: "white"}}>
          <GiDiamondsSmile style={{ color: "white"}}></GiDiamondsSmile> <span className="ml-1">Pages</span>
      </Link>
      </nav>
    )
  }


  const list = (anchor) => (
    <div 
      className={clsx(classes.list, {[classes.fullList]: anchor === 'top' || anchor === 'bottom',})}
      role="presentation"
      onClick={toggleDrawer(anchor, false)}
      onKeyDown={toggleDrawer(anchor, false)}
    >
      {/* Nav Title */}
      {navTitle(props.current_user)}

      {/* List item */}
      <List>
        {list_items.map((text, index) => (
            <ListItem button key={text}>
              <Link 
                to={text[1]} 
                style={{color: "white"}}> {text[2]} {text[0]} 
              </Link>
            </ListItem>
        ))}
        <ListItem button key={"logout"}>
            <Link
              to="/login" 
              onClick={props.log_out} 
              style={{color: "white"}}>
               <RiLogoutCircleRLine/> Logout
            </Link>
        </ListItem>
      </List>
  
    </div>
  );

  
  return (
    <div>
      {['left'].map((anchor) => (
        <React.Fragment key={anchor}>
          <Button onClick={toggleDrawer(anchor, true)}>
             <MenuOpenIcon style={{color: "white"}}/>
          </Button>
          <Drawer anchor={anchor} open={state[anchor]} onClose={toggleDrawer(anchor, false)}>
            {list(anchor)}
          </Drawer>
        </React.Fragment>
      ))}
    </div>
  );
}
