const express = require('express');
const app = express();
const PORT = 5000;
const cors = require('cors');
const path = require('path');
const {gemini_api_call,sentiment_api_call,Link_Analyzer_api_call,PDF_Analyzer_api_call} = require('./api_call.js');
const {console} = require('inspector');

app.use(cors());
app.use(express.json()); 
async function call_user_choice(choice, prompt) {
  try {
    if (choice === 'Sentiment') {
      return await sentiment_api_call(prompt);
    } else if (choice === 'Gemini') {
      return await gemini_api_call(prompt);
    } else if (choice === 'Link_Analyzer') {
      return await Link_Analyzer_api_call(prompt);
    }else{
      return await PDF_Analyzer_api_call(prompt);
    }
  }catch (error) {
    console.error(`Error in call_user_choice with choice ${choice}:`, error);
    throw new Error('Error processing the request');
  }
}

let choice = 'Sentiment';

app.get('/',async(req,res)=>{
  choice = 'Sentiment';
  res.status(200).json({reply:"Refresed..."});
})
app.post('/api/chat',async(req, res) => {
  const userMessage = req.body.message;
  if (userMessage) {
    try{
      let reply = await call_user_choice(choice,userMessage);
      res.status(200).json({reply: reply});  
    }
    catch(error){
      res.status(500).json({reply:"Something went wrong!!!"});
    }
  } else {
    res.status(400).json({ error: 'No message provided' });
  }
});
app.post('/api/type',async(req, res) => {
  const userchoice = req.body.button_type;
  if (userchoice) {
    try{
      choice = userchoice;
      res.status(200).json({reply:userchoice+" has been selected"});  
    }
    catch(error){
      res.status(400).json({reply:"Something went wrong!!!"});
    }
  } else {
    res.status(400).json({ error: 'No message provided' });
  }
});

app.listen(PORT,()=>{
  console.log(`Hellow Server from port ${PORT}...`)
})

