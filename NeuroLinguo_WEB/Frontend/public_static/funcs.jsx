import axios from "axios";


function fromatt_text(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    text = text.replace(/`(.*?)`/g, "<br><code class='code_area'>$1</code><br>");
    text = text.replace(/\n/g, "<br>");
    return text;
}
function typewritter_effect(data,botItem){
    let bot_text = fromatt_text(data);
    let i = 0,temptext="";
    botItem.textContent = "";
    let x = setInterval(()=>{
        if(i < bot_text.length){
            temptext+=bot_text[i];
            botItem.innerHTML = temptext;
            i+=1;
        }
        else{
            clearInterval(x);
        }
        if(i%200){
            window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
        }
    },22);
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    return botItem;
}
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function to_server_api(text,botItem,submitButton){
    axios.post('http://localhost:5000/api/chat',{ message: text })
    .then(async(response) => {
        await delay(1000); 
        botItem.className="bot_text";
        typewritter_effect(response.data.reply,botItem);
        return response.data.reply;
    })
    .catch(error => {
        submitButton.disabled = false;
        console.error('There was an error!', error);
        return "";
});
}
export{
    typewritter_effect,
    to_server_api
};

