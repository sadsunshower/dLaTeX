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
        body.appendChild(textWithCode(content));

        parent.appendChild(header);
        parent.appendChild(body);

        return parent;
    };

    const textWithCode = (raw) => {
        const ctr = document.createElement('span');
        const components = raw.split(/`/);

        let code = false;
        let codeTag = null;

        for (const comp of components) {
            if (code) {
                codeTag.appendChild(document.createTextNode(comp));
                ctr.appendChild(codeTag);

                code = false;
                codeTag = null;
            } else {
                ctr.appendChild(document.createTextNode(comp));

                code = true;
                codeTag = document.createElement('code');
            }
        }

        return ctr;
    };

    document.querySelector('#content').value = localStorage.getItem('saved');

    const save = () => {
        localStorage.setItem('saved', document.querySelector('#content').value);
    }

    setInterval(save, 3000);

    const about = document.querySelector('#about-modal');
    document.querySelectorAll('.about-toggle').forEach(e => {
        e.addEventListener('click', () => {
            about.classList.toggle('is-active');
        })
    });

    document.querySelector('#submit').addEventListener('click', () => {
        const content = document.querySelector('#content').value;
        save();

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

                if (!json['pdf']) {
                    messages.appendChild(createMessage('No PDF', 'is-danger', 'LaTeX produced no output PDF, the log file is shown instead.'))
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

            outputPDF.src = `/static/${json['save']}.${json['pdf'] ? 'pdf' : 'txt'}`;
            outputPDF.classList.add('has-ratio');
            outputPDF.style.width = '100%';
            outputPDF.style.height = '100%';
            output.appendChild(outputPDF);
        }).catch(console.log);
    });
})();