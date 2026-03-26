import { useState } from 'react'
import App from './App.jsx'
import Mainpage from './Mainpage.jsx'
import Mycar from './Vehicle.jsx'
import PopupModel from './Popupmodel.jsx'
import ButtonClickAction from './ButtonClickAction.jsx'

export default function Root() {
  const [isOpen, setIsOpen] = useState(false)
  const [count1, setCount2] = useState(0)

  return (
    <>
      <App />
      <Mainpage color="Red" model="RED123" />
      <Mycar value1="BMW" value2="Audi" type="Cars" />
      <button className="counter" onClick={() => setIsOpen(true)}>
        Open Popup
      </button>
      <PopupModel isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <h2>The Model Test</h2>
        <div>The Model Content to show</div>
      </PopupModel>
      <div>This is count {count1}</div>
      <ButtonClickAction
        onClick={() => {
          // This runs first
          setCount2(c => c + 1);
        }}>
        Floating Button 
      </ButtonClickAction>

    </>
  )
}
