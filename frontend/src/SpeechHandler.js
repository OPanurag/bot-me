const SpeechHandler = {
    speak: (text) => {
      const audio = new Audio(`https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=${encodeURIComponent(text)}`);
      audio.play();
    },
  
    listen: () => {
      const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      recognition.lang = 'en-US';
      recognition.start();
      recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        document.querySelector('input').value = spokenText;
      };
    }
  };
  export default SpeechHandler;
  