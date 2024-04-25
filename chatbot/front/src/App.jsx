import { useState } from "react";
import image from "./assests/robo.jpg";
import "./App.css";
import axios from "axios"

function App() {
  const [botmessage, setBotMessage] = useState("");
  const [humanMessage, setHumanMessage] = useState("");
  const [input, setInput] = useState("");
  const [selectedImage, setSelectedImage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      const formData = new FormData();
      formData.append("image",selectedImage);
      formData.append("input",input);
      const res = await axios.post("http://127.0.0.1:5000/",formData,{
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })

      setHumanMessage(input);
      setBotMessage(res.data.message);


    }catch(err){
      console.log("Error: "+err);
    }
  }

  
  return (
    <div className="App">
      <div className="wrapper">
        <div className="content">
          <div className="header">
            <div className="img">
              <img src={image} alt="" />
            </div>
            <div className="right">
              <div className="name">ChatBot</div>
              <div className="status">Active</div>
            </div>
          </div>
          <div className="main">
            <div className="main_content">
              <div className="messages">
                <div className="bot-message" id="message1">
                  {botmessage}
                </div>
                <div className="human-message" id="message2">
                  {humanMessage}
                </div>
              </div>
            </div>
          </div>
          <div className="bottom">
            <div className="btm">
              <div className="input">
                <input
                  type="text"
                  id="input"
                  placeholder="Enter your message"
                  onChange={(e) => setInput(e.target.value)}
                  value={input}
                />
              </div>
              
              <div className="btn">
              <input
                  type="file"
                  name="myImage"
                  onChange={(event) => {
                    console.log(event.target.files[0]);
                    setSelectedImage(event.target.files[0]);
                  }}
                />
                <button onClick={handleSubmit}>
                  <i className="fa-solid fa-arrow-up"></i>Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
