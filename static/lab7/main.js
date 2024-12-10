function fillfilmlist() {
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        return response.json();
    })
    .then(function (films){
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td'); 
            let tdTitle = document.createElement('td'); 
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;

            if (films[i].title && films[i].title !== films[i].title_ru) {
                tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
            } else {
                tdTitle.innerHTML = `<i>(${films[i].title_ru})</i>`; 
            }

            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() { 
                editfilm(i); 
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';

            delButton.onclick = function() { 
                deletefilm(i, films[i].title_ru); 
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus); 
            tr.append(tdTitle); 
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    });
}

function deletefilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function (){
            fillfilmlist();
        })
        .catch(function(error) {
            console.error('Ошибка при удалении фильма:', error);
        });
}

function showmodal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hidemodal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hidemodal();
}

function addfilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showmodal();
}

function sendfilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value,
    }

    if (film.description.trim() === '') {
        document.getElementById('description-error').innerText = 'Описание не может быть пустым';
        return;
    } else {
        document.getElementById('description-error').innerText = ''; 
    }
    
    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if (resp.ok){
            fillfilmlist();
            hidemodal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.description)
            document.getElementById('description-error').innerText = errors.description;
    })
    .catch(function(error) {
        console.error('Ошибка при отправке данных:', error);
    });
}

function editfilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        return response.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showmodal();
    })
}