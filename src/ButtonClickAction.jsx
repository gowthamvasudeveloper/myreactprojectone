import {createPortal} from 'react-dom';

function ButtonClickAction ({ onClick, children }) {
    return createPortal(
        <button 
        onClick={onClick}
        style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            padding: '10px',
            background: 'blue',
            color: 'white'
        }}>
        {children}
        </button>,
        document.body
    )
} 

export default ButtonClickAction;