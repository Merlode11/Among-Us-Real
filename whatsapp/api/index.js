// Build a REST API to interact with a python script and the WhatsApp api
const { Client, Location, List, Buttons, LocalAuth } = require('whatsapp-web.js');
const api = require('./api');
const axios = require('axios');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: false
    }
});

client.initialize().then();

api(client);

client.on('qr', (qr) => {
    // NOTE: This event will not be fired if a session is specified.
    console.log('QR RECEIVED', qr);
    sendEvent('qr', qr);

});

client.on('authenticated', () => {
    console.log('AUTHENTICATED');
    sendEvent('authenticated', true);
});

client.on('auth_failure', msg => {
    // Fired if session restore was unsuccessful
    console.error('AUTHENTICATION FAILURE', msg);
    sendEvent('auth_failure', msg);
});

client.on('ready', () => {
    console.log('READY');
    sendEvent('ready', true);
});

client.on('message', async msg => {
    sendEvent('message', msg);
});


client.on('message_revoke_everyone', async (after, before) => {
    // Fired whenever a message is deleted by anyone (including you)
    console.log(after); // message after it was deleted.
    if (before) {
        console.log(before); // message before it was deleted.
    }
    sendEvent('message_revoke_everyone', { after, before });
});

client.on('disconnected', (reason) => {
    console.log('Client was logged out', reason);
    sendEvent('disconnected', reason);
});

client.on("media_uploaded", (media) => {
    console.log("media uploaded, here is the id", media.id)
    sendEvent('media_uploaded', media);
})


function sendEvent(event, data) {
    axios.post(`http://localhost:3046/${event}`, { data: data })
        .then(res => console.log("success"))
        .catch(err => {
            // Pass error if ECONNREFUSED
            if (err.code === 'ECONNREFUSED') {
                return console.error('ERROR: The server is not running!');
            } else console.error(err)
        });
}