var questions = [
    {question:"¿Cual es tu nombre?"},
    {question:"¿Cual es tu email?", pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/},
    {question:"Create una contraseña", type: "password", pattern: /^.{6,}$/}
  ]
  
  ;(function(){
  
    var tTime = 100  
    var wTime = 200  
    var eTime = 1000 
  
    var position = 0
  
    putQuestion()
  
    progressButton.addEventListener('click', validate)
    inputField.addEventListener('keyup', function(e){
      transform(0, 0) 
      if(e.keyCode == 13) validate()
    })
  
    function putQuestion() {
      inputLabel.innerHTML = questions[position].question
      inputField.value = ''
      inputField.type = questions[position].type || 'text'  
      inputField.focus()
      showCurrent()
    }
    
    async function done() {
      
      register.className = 'close'
      
      await fetch("/register?nm=" + questions[0].value + "&psw=" + questions[2].value + "&mail=" + questions[1].value, {
        method: 'POST'
      }).then(response => response.json()).then(function(data) {
          console.log(data)
          if (JSON.stringify(data) == "{}") {
            if (window.confirm("Ese email ya existe ¿quieres entrar en tu cuenta?")) {
              window.location.href = "/login";
              return ;
            } else {
              window.location.replace("/register");
              return ;
          }
        }
      });
      setTimeout(function() {   
        setTimeout(function() {
            window.location.replace("/account")
        }, 50)
      }, eTime)
      
    }
  
    function validate() {
  
      questions[position].value = inputField.value
      
  
      if (!inputField.value.match(questions[position].pattern || /.+/)) wrong()
      else ok(function() {
        
        progress.style.width = ++position * 100 / questions.length + 'vw'
  
        if (questions[position]) hideCurrent(putQuestion)
        else hideCurrent(done)
               
      })
  
    }
  
    function hideCurrent(callback) {
      inputContainer.style.opacity = 0
      inputProgress.style.transition = 'none'
      inputProgress.style.width = 0
      setTimeout(callback, wTime)
    }
  
    function showCurrent(callback) {
      inputContainer.style.opacity = 1
      inputProgress.style.transition = ''
      inputProgress.style.width = '100%'
      setTimeout(callback, wTime)
    }
  
    function transform(x, y) {
      register.style.transform = 'translate(' + x + 'px ,  ' + y + 'px)'
    }
  
    function ok(callback) {
      register.className = ''
      setTimeout(transform, tTime * 0, 0, 10)
      setTimeout(transform, tTime * 1, 0, 0)
      setTimeout(callback,  tTime * 2)
    }
  
    function wrong(callback) {
      register.className = 'wrong'
      for(var i = 0; i < 6; i++) 
        setTimeout(transform, tTime * i, (i%2*2-1)*20, 0)
      setTimeout(transform, tTime * 6, 0, 0)
      setTimeout(callback,  tTime * 7)
    }
  
  }())