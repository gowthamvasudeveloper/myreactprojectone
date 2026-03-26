import { useState } from "react";

function Mycar (props) {
    const cars = ['Audi', 'BMW',  'VolksWagon'] 
    const [name, setName] = useState("");
    const [txtarea, setTxtarea] = useState("");

    function handleChange (e) {
        // Controlled input: keep React state in sync with what the user types.
        setName(e.target.value);
    }
    function handleTxrChange (e) {
        setTxtarea(e.target.value);
    }
    function handleSubmit (e) {
        e.preventDefault()
        alert(name)
    }
    return (
    <>
    <Mytest type={props.type} />
      <ul>
        <li>{props.value1}</li>
        <li>{props.value2}</li>
      </ul>
      <div>Car Array List</div>
      <ul>
        {cars.map((car) => <li>{car}</li>)}
      </ul>      
      <form onSubmit={handleSubmit}>
        <label>Enter your name:
            <input type="text" value={name} onChange={handleChange} />
            <textarea value={txtarea} onChange={handleTxrChange} />
        </label>
        <input type="submit" />
      </form>
    <p>Current input: {name}</p>
    <p>Current textarea: {txtarea}</p>
    </>
      
    );
  }
  function Mytest (props) {
    return (
      <>
      <h1>My {props.type} are</h1>
      </>
    )
  }

  export default Mycar;