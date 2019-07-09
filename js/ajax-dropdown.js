(function() {
    let xhr = new XMLHttpRequest();

    var fileNames;
    xhr.open('GET', '/?listfiles=1', true);

    xhr.onload = () => {
        if(xhr.status == 200) {
            fileNames = xhr.responseText;
            fileNames = fileNames.split(',');
            for(let i in fileNames){
                let option = document.createElement('option');
                option.appendChild(document.createTextNode(fileNames[i]));
                option.value = fileNames[i];
                document.getElementById('dropdown-menu').append(option);
            }
        }

        document.getElementById('dropdown-menu').addEventListener('change', () => {
            if(document.getElementById('dropdown-menu').value){
                let xhr_inner = new XMLHttpRequest();
                xhr_inner.open('GET', 'files/' + document.getElementById('dropdown-menu').value, true);
                xhr_inner.onload = () =>  {
                    if (xhr_inner.status == 200) {
                        if(document.getElementById('dropdown-menu').value.split('.')[1] == 'json') {
                            document.getElementById('disp-dropdown').innerText = ""
                            document.getElementById('disp-json').innerHTML = JSON.stringify(xhr_inner.response, undefined, 2)
                        } else {
                            document.getElementById('disp-json').innerHTML = ""
                            document.getElementById('disp-dropdown').innerText = xhr_inner.responseText;
                        }
                        
                    }
                }
                if(document.getElementById('dropdown-menu').value.split('.')[1] == 'json'){
                    xhr_inner.responseType = 'json'
                }
                xhr_inner.send()
            } else {
                document.getElementById('disp-dropdown').innerText = ""
            }
        })
    }

    xhr.send();
})();
