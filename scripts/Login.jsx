import * as React from 'react';
import { GoogleButton } from './GoogleButton';

export function Login(props){
    return  <div id="login">
                <span id ="login_text"> Log in to participate in chat </span>
                <GoogleButton />
            </div>;
}