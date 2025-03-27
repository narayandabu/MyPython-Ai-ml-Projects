import {createRoot} from "react-dom/client"
import React, { useState } from 'react';
import { useRef } from 'react';
import { useEffect } from "react";
import {typewritter_effect,to_server_api} from "./public_static/funcs.jsx"
import Side_bar from "./public_static/side_bar.jsx";


const container = document.getElementById("root")
const root = createRoot(container)
let chathist = [];
function enter_to_submit(){
    useEffect(() => {
        const handleKeyPress = (event) => {
          if (event.key === "Enter") {
            if(event.shiftKey){
                return;
            }
            else {
                event.preventDefault();
                document.getElementById("submit").click();
            }
          }
        };
    
        document.addEventListener("keydown", handleKeyPress);
    
        return () => {
          document.removeEventListener("keydown", handleKeyPress); // Cleanup event listener
        };
      }, []); 
}

function Search_Box(){
    let [text, setText] = useState('');
    const ref_chat_list = useRef(null);
    async function handleButtonClick  (){
        if(text){
            const chat_area = document.getElementById('chat-area');
            const userItem = document.createElement('article');
            userItem.textContent = text;
            const submitButton = document.getElementById('submit');
                
            userItem.className="user_text";
            userItem.id="user";
            chat_area.appendChild(userItem);

            try{
                const botItem = document.createElement('article');
                botItem.className="bot_texttyping";
                botItem.textContent = "Thinking...";
                botItem.id="bot";
                chat_area.appendChild(botItem);
                const x = document.getElementById("input_area");
                x.value="";
                text = "";
                window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
                const reply = to_server_api(userItem.textContent,botItem, submitButton);
            }
            catch(error){
                console.log(error);
            }
        }
    };
    enter_to_submit();
    const handleTextChange = (event) => {
        setText(event.target.value);
    };
    return(
        <>
            <div className="chat-area" id="chat-area"></div>
            <div className="Search_Box">
                <textarea className="Text-Area" placeholder="Enter Text" id="input_area" value={text} onChange={handleTextChange}></textarea>
                <button type="submit" className="Submit-Button" onClick={handleButtonClick} id='submit'><b> ↑ </b></button>
            </div>
        </>
    )
}
function File_uploader(){
    const uploadhandler = ()=>{

    }
    const handleupload = ()=>{
        
    }
    return(
        <>
            
        </>
    )
}
function Main(){
    return(
        <>
            <Side_bar/>
            <Search_Box/>
            {/* <File_uploader/> */}
        </>
    )
}
root.render(
    <Main/>
)




