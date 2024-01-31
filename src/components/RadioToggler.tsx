import React, { useEffect, useState } from "react";

function RadioToggler() {
  const description = document.querySelector(".description");
  const card = document.querySelector(".card");
  const pdf = document.querySelector(".pdf");
  console.log(pdf);
  const [radio, setRadio] = useState("radio1");

  const handleRadioChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRadio(event.target.id);
  };

  useEffect(() => {
    if (radio === "radio1") {
      description?.classList.remove("hide");
      card?.classList.remove("hide");
      pdf?.classList.add("hide");
    } else {
      description?.classList.add("hide");
      card?.classList.add("hide");
      pdf?.classList.remove("hide");
    }
  }, [radio, description, card, pdf]);

  return (
    <div className="container">
      <div className="selector">
        <div className="selector-item">
          <input
            type="radio"
            id="radio1"
            name="selector"
            onChange={handleRadioChange}
            className="selector-item_radio"
            defaultChecked
          />
          <label htmlFor="radio1" className="selector-item_label">
            ML Model
          </label>
        </div>
        <div className="selector-item">
          <input
            type="radio"
            id="radio2"
            name="selector"
            onChange={handleRadioChange}
            className="selector-item_radio"
          />
          <label htmlFor="radio2" className="selector-item_label">
            Documentation
          </label>
        </div>
      </div>
    </div>
  );
}

export default RadioToggler;