import React, {useState} from 'react';

interface predictObject {
    breed: string;
    probability: number; // Assuming the percentage is represented as a number (0 to 100)
  };

const Dropdown = ({ items }: { items: predictObject[] }) => {
  const [isOpen, setOpen] = useState(false);
  
  const toggleDropdown = () => setOpen(!isOpen);
  
  
  return (
    <div className='dropdown' >
      <div className='dropdown-header' onClick={toggleDropdown}>
        Click to see detailed Predictions
        <i className={`fa fa-chevron-right icon ${isOpen && "open"}`}></i>
      </div>
      <div className={`dropdown-body ${isOpen && 'open'}`}>
        {items.map(item => (
          <div className="dropdown-item" id={item.breed}>
            {Math.round(item.probability * 100)}% a {item.breed}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dropdown;
