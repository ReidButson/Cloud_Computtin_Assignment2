import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {width: props.innerWidth};
  }

  resize = () => this.forceUpdate()

  componentDidMount() {
    window.addEventListener('resize', this.resize)
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.resize)
  }

  render() {
    return (
      <div className="App">
        <img
          src={require("./images/danceboi.gif")}
          style={{width: window.innerWidth}}
          onClick={{}}/>
      </div>
    );
  }
}

export default App;
