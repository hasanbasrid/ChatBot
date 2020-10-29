import * as React from 'react';
import { Socket } from './Socket';
import { Button } from './Button';
import { Input } from './Input';

export function Form() {
  function handleSubmit(event) {
    const newMessage = document.getElementById('message_input').value;

    Socket.emit('new message input', {
      message: newMessage,
    });

    console.log(`Sent message :"${newMessage} " to server!`);

    document.getElementById('message_input').value = '';

    event.preventDefault();
  }

  return (
    <form onSubmit={handleSubmit}>
      <Input />
      <Button />
    </form>
  );
}
