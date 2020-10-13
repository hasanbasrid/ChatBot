import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let new_message = document.getElementById("message_input");

    Socket.emit('new message input', {
        'message': new_message.value,
    });
    
    console.log('Sent message :"' + new_message.value + ' " to server!');

    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="message_input"></input>
            <button>SEND</button>
        </form>
    );
}
