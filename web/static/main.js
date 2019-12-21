(() => {
    const createMessage = (title, colour, content) => {
        const parent = document.createElement('article');
        parent.classList.add('message');
        parent.classList.add(colour);

        const header = document.createElement('div');
        header.classList.add('message-header');
        
        const headerText = document.createElement('p');
        headerText.innerText = title;
        header.appendChild(headerText);

        const body = document.createElement('div');
        body.classList.add('message-body');
        body.innerText = content;

        parent.appendChild(header);
        parent.appendChild(body);

        return parent;
    };

    document.querySelector('#submit').addEventListener('click', () => {
        const content = document.querySelector('#content').value;

        fetch('/dlatex', {
            method : 'POST',
            body : content,
            credentials: 'same-origin',
            headers : {
                'Content-Type' : 'text/plain'
            },
        }).then(res => {
            return res.json();
        }).then(json => {
            const messages = document.querySelector('#messages');
            messages.innerHTML = '';

            if ('fail' in json) {
                messages.appendChild(createMessage('Server Error', 'is-dark', json['fail']));
            } else {
                if (json['error']) {
                    messages.appendChild(createMessage('Errors', 'is-danger', 'Errors detected, output PDF may have unexpected results.'))
                } else {
                    messages.appendChild(createMessage('No errors', 'is-success', 'No errors, output PDF okay.'))
                }

                for (const message of json['messages']) {
                    let colour = ''; let title = '';
                    switch (message['severity']) {
                        case 'info' : colour = 'is-info'; title = 'Info'; break;
                        case 'warning' : colour = 'is-warning'; title = 'Warning'; break;
                        case 'error' : colour = 'is-danger'; title = 'Error'; break;
                        default : colour = 'is-primary'; title = 'Unknown';
                    }

                    messages.appendChild(createMessage(`${title} on line ${message['num']}`, colour, message['message']));
                }
            }

            const output = document.querySelector('#output');
            output.innerHTML = '';

            const outputPDF = document.createElement('iframe');
            outputPDF.src = `/static/${json['save']}.pdf`;
            output.appendChild(outputPDF);
        }).catch(console.log);
    });
})();