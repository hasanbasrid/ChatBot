import * as React from 'react';
import { GoogleButton } from './GoogleButton';

export function Login() {
  return (
    <div id="login">
      <span id="login_text"> Login to participate in chat : </span>
      <GoogleButton />
    </div>
  );
}
