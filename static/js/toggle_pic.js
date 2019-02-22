'use strict';

const e = React.createElement;



class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      liked: true,
    };
    this.toggle = this.toggle.bind(this);
  }

  toggle(){
    this.setState({liked: !this.state.liked})
  }

  render() {
    if (this.state.liked) {
      return e(
        'button',
        { onClick: this.toggle },
        'No Like'
      );
    }

    return e(
      'button',
      { onClick: this.toggle },
      this.props.word
    );
  }
}

alert("woo")
const script = document.querySelector('#pic_script')
var word = script.getAttribute("data-word")
const domContainer = document.querySelector('#pic_toggle');
ReactDOM.render(e(LikeButton, {word: word}), domContainer);
