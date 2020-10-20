import * as React from 'react';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login'

function handleSuccessfulLogin(response) {
    // TODO replace with name from oauth
    Socket.emit('new google user', {
        'email':response.profileObj.email,
        'name':response.profileObj.name,
        'profile_pic': response.profileObj.imageURL
    });
}

export function GoogleButton() {
    return (
    <GoogleLogin
    clientId="272516160783-40amej6085rmt99ag682j59fq3io3ue2.apps.googleusercontent.com"
    buttonText="Login"
    onSuccess={handleSuccessfulLogin}
    cookiePolicy={'single_host_origin'}
    />
    );
}
