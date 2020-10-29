import * as React from 'react';
import { Login } from './Login';
import { Users } from './Users';
import { MessageList } from './MessageList';
import { Form } from './Form';

export function Content() {
  return (
    <div id="container">
      <Login />
      <div id="components">
        <Users />
        <MessageList />
        <Form />
      </div>
    </div>
  );
}
