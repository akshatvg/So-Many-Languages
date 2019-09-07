

const mic = document.querySelector('.mic')
const recordingStatus = document.querySelector('.recording-status')
const samantha = window.speechSynthesis.getVoices().filter( voice => voice.name === 'Samantha')[0]

if (typeof(String.prototype.localeCompare) === 'undefined') {
  String.prototype.localeCompare = function(str, locale, options) {
      return ((this == str) ? 0 : ((this > str) ? 1 : -1));
  };
}
var flag=1
let isRecording = false; 
mic.addEventListener('click', listenForSpeech)
function clearChatInput () {
   chatInput.value = ''
}

function sendTextChatMessage ( ){
  let newChat = chatInput.value
  postChatMessage(newChat)
}

function postChatMessage (response) {
  
  console.log("post chat function");
  res_list = document.getElementById("chat-responses"); //chat-responses should be the class of the mic button in the html.
  var check=response.toString().localeCompare("open C plus plus")
  if(check==0){
    response="open c++"
  }
  element_val = `
  User: ${response}
  `
  res_list.innerHTML = element_val;
 var respon_json = {"text": response}
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    url: "http://127.0.0.1:5000/print/name", //localhostURL
    //url: " https://f0061e2e.ngrok.io/print/name", //servo.net 
    traditional: "true",
    data: JSON.stringify(respon_json),
    dataType: "json",
    success:function(response){
      //speakResponse(response.response);
      var p=response.response.toString().localeCompare("python running!")
      var c=response.response.toString().localeCompare("running c++")
      var ph=response.response.toString().localeCompare("running php")
      var sw=response.response.toString().localeCompare("running swift")
      if(p==0){
        flag=1
        console.log(flag)
      }
      else if(p==-1 || p==1){
        flag=flag
        console.log(flag)
      }
      if(c==0){
        flag=0
        console.log(flag)
      }
      else if(c==-1 || c==1) {
        flag=flag
        console.log(flag)
      }
      if(ph==0){
        flag=2
        console.log(flag)
      }
      else if(ph==-1 || ph==1) {
        flag=flag
        console.log(flag)
      }
      if(sw==0){
        flag=3
        console.log(flag)
      }
      else if(sw==-1 || sw==1){
        flag=flag
        console.log(flag)
      }
      if(flag==1){
      displayResponse(response.response);
      }
      else if(flag==0){
      displayResponseC(response.response);
      }
      else if(flag==2){
        displayResponsePhp(response.response);
        }
        else if(flag==3){
          displayResponseSwift(response.response);
          }
    }
    });
}

function displayResponse (response) {
    let newChat = document.createElement('p')
    newChat.innerHTML = `${response}`
      chatMessages = document.getElementById("chat-input");
      chatMessages.append(newChat)
      EnlighterJS.Util.Init('p', null, {
        indent: 4,
        language: 'python',
        theme: 'Beyond'
    });
}

function displayResponsePhp (response) {
  let newChat = document.createElement('p')
  newChat.innerHTML = `${response}`
    chatMessages = document.getElementById("chat-input");
    chatMessages.append(newChat)
    EnlighterJS.Util.Init('p', null, {
      indent: 4,
      language: 'php',
      theme: 'Beyond'
  });
}

function displayResponseC (response) {
  let newChat = document.createElement('p')
  newChat.innerHTML = `${response}`
    chatMessages = document.getElementById("chat-input");
    chatMessages.append(newChat)
    EnlighterJS.Util.Init('p', null, {
      indent: 4,
      language: 'cpp',
      theme: 'MooTwo'
  });
}

function displayResponseSwift (response) {
  let newChat = document.createElement('p')
  newChat.innerHTML = `${response}`
    chatMessages = document.getElementById("chat-input");
    chatMessages.append(newChat)
    EnlighterJS.Util.Init('p', null, {
      indent: 4,
      language: 'swift',
      theme: 'MooTwo'
  });
}

function speakResponse (response) {
  let utterance = new SpeechSynthesisUtterance(response);
  utterance.voice = samantha
  window.speechSynthesis.speak(utterance)
  displayResponse(response)
}

function listenForSpeech () {
        console.log(isRecording)
        if (isRecording){
          isRecording = false
          recordingStatus.innerText = 'Speak your querry :)'
          return 0;
        }
        isRecording = true
        recordingStatus.innerText = 'Listening....'
        var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
        var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent
        var recognition = new SpeechRecognition()

        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.start()

        recognition.onspeechstart = function() {
            console.log('Speech has been detected');
        }

        recognition.onresult = function(event) {
            let last = event.results.length - 1;
            let speech = event.results[last][0].transcript;
     
            postChatMessage(speech)
          
            console.log('Result received: ' + speech + '.');
            console.log('Confidence: ' + event.results[0][0].confidence);
        }

        recognition.onspeechend = function() {
            recordingStatus.innerText = 'speak your querry :)'
            console.log('Speech has stopped being detected');
        }

        recognition.onerror = function(event) {
            console.log('Error occurred in recognition: ' + event.error);
        }
}

document.querySelector('.chat-bot-button').addEventListener('click', function (){
  console.log('clicked')
  document.querySelector('.chat-bot-modal').classList.toggle('open')
})
console.log(flag)
