let coll = document.getElementsByClassName('arrow');
let HiddenInfo = document.getElementsByClassName('HiddenInfo');
//Вешаем ивенты на каждую стрелку и выбираем следующий элемент (надпись слева)
for (let i = 0; i< coll.length; i++) {
    coll[i].addEventListener('click',function(){
        this.classList.toggle('active');
        
        let content = this.nextElementSibling;
        // Отображение надписи слева при помощи изменения размера родительского блока
        if (content.style.maxHeight){
            content.style.maxHeight = null;
            HiddenInfo[i].style.maxHeight = null;
            
        } else{
            content.style.maxHeight = content.scrollHeight + 'px';
            HiddenInfo[i].style.maxHeight = HiddenInfo[i].scrollHeight + 'px';
        }
        
        

    })
}


