import React, {useState} from 'react';

interface predictObject {
    breed: string;
    probability: number; // Assuming the percentage is represented as a number (0 to 100)
  };

const Dropdown = ({ items }: { items: predictObject[] }) => {
  const [isOpen, setOpen] = useState(false);
  
  const toggleDropdown = () => setOpen(!isOpen);
  
  
  return (
    <div className='dropdown'>
      <div className='dropdown-header' onClick={toggleDropdown}>
        Click to see detailed Predictions
        <i className={`fa fa-chevron-right icon ${isOpen && "open"}`}></i>
      </div>
      <div className={`dropdown-body ${isOpen && 'open'}`}>
        {items.map(item => {
          // Determine the color based on probability
          let colorClass;
          if (item.probability * 100 > 80) {
            colorClass = "green";
          } else if (item.probability * 100 >= 30 && item.probability * 100 <= 80) {
            colorClass = "yellow";
          } else {
            colorClass = "red";
          }
  
          return (
            <div className="dropdown-item" id={item.breed}>
              <i className={`fa fa-circle text-${colorClass}-glow`}></i>
              <p>{(item.probability * 100).toFixed(2)}% a {item.breed}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Dropdown;
