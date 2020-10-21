import * as React from 'react';
import { Socket } from './Socket';
import { Button } from './Button';
import { Input } from './Input';

function handleSubmit(event) {
    let new_message = document.getElementById("message_input").value;

    Socket.emit('new message input', {
        'message': new_message,
    });
    
    console.log('Sent message :"' + new_message + ' " to server!');
    
    document.getElementById("message_input").value = "";
    
    event.preventDefault();
}

export function Form() {
    return (
        <form onSubmit={handleSubmit}>
            <Input />
            <Button />
        </form>
    );
}
