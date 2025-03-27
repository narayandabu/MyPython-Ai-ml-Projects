import React,{useState} from "react";
import "./side_bar.css";
import axios from "axios";

function to_server(button){
    axios.post('http://localhost:5000/api/type',{ button_type: button })
    .then((response) => {
        // const botItem = typewritter_effect(response.data.reply);
        // console.log(response.data.reply);
        // chat_area.appendChild(botItem);
        return response;
    })
    .catch(error => {
        console.error('There was an error!', error);
        return "";
});
}
const reset_chats = ()=>{
    const chats = document.getElementById('chat-area');
    if(chats){
        // console.log('Chats Cleared...');
        while(chats.firstChild){
            chats.removeChild(chats.firstChild);
        }
        return true;
    }
    else return false;
}
const Side_bar = ()=>{
    const [isOpen, setIsOpen] = useState(true);
    const [selected, setSelected] = useState(0); // Track selected button

    const button_names = ["Sentiment", "Gemini", "PDF_Analyzer", "Link_Analyzer"];

    const button_funcs = [
        /*1.Sentiment*/()=>{
            to_server('Sentiment');
        },
        /*2.Gemini*/()=>{
            to_server('Gemini');
        },
        /*3.PDF_Analyzer*/()=>{
            to_server('PDF_Analyzer');
        },
        /*4.Link_Analyzer*/()=>{
            
            to_server('Link_Analyzer');
        },
    ]
    return(
        <>
            <div className="side-bar">
                <button  onClick={() => setIsOpen(!isOpen)} className="menu_button"> {isOpen ? "☰": "✖"}</button>
                <div className="navb">AllInDOCS</div> 
            </div>
            <div className="side-menu">
                <div className={`side-menu-bar-ele${isOpen ? "open" : ""}`}>
                    <div className={`side-menu-bar${isOpen ? "open" : ""}`}>
                        <h2 className="side-bar-title">Choose Mode</h2>
                        <ul className="side-menu-list">
                            {button_names.map((label, index) => (
                            <button 
                                key={index} 
                                className={selected === index ? "selected" : ""} 
                                onClick={() => {setSelected(index),button_funcs[index](),reset_chats()}}
                            >
                                {label}
                            </button>
                            ))}
                        </ul>
                        <div className={`Link-Request${selected == 3? "open" : ""}`}>
                            <h3>Hi,Hellow</h3>
                        </div>
                    </div>
                </div>
            </div>
        
        </>
    )


}

export default Side_bar;