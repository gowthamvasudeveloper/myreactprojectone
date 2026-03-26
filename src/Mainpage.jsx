import React from 'react'

class Mainpage extends React.Component {
    constructor(props) {
      super(props);
      this.state = {component: "Red",prof: "Redvkejk"}
    }
    changeComponent = () =>{
        this.setState({component: "Blue", prof: "BLuevkejk"})
    }
    render () {
      return (
      <>
      <h1> I am New {this.state.component} Component </h1>
      <h2>my color is {this.props.color}</h2>
      <h3>my model is {this.props.model}</h3>
      <h4>This proficient is {this.state.prof}</h4>
      <button className='counter' onClick={this.changeComponent}>Change Value</button>
      </>
      )
    }
  
  }

  export default Mainpage;