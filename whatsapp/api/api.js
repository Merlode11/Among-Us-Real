// Build a REST API to interact with a python script and the WhatsApp api
const express = require('express');
const app = express();
const port = 3045;
const bodyParser = require('body-parser');
const {WAWebJS, MessageSendOptions, MessageMedia} = require('whatsapp-web.js');

/**
 * Create a REST API to interact with a python script and the WhatsApp api
 * @param client {WAWebJS.Client}
 */
module.exports = (client) => {
    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({extended: true}));

    /**
     * acceptInvite
     * @param {string} inviteCode
     * @returns {Promise<void>}
     */
    app.post("/acceptInvite", (req, res) => {
        const {inviteCode} = req.body;
        client.acceptInvite(inviteCode).then(r =>
            res.sendStatus(200)
        ).catch(err =>
            res.send(err)
        );
    });

    /**
     * archiveChat
     * @param {string} chatId
     */
    app.post("/archiveChat", (req, res) => {
        const {chatId} = req.body;
        client.archiveChat(chatId).then(r =>
            res.sendStatus(200)
        ).catch(err =>
            res.send(err)
        );
        res.sendStatus(200);
    })

    /**
     * createGroup
     * @param {string} groupName
     * @param {string[]} participants
     */
    app.post("/createGroup", (req, res) => {
        const {groupName, participants} = req.body;
        client.createGroup(groupName, participants).then((group) => {
            res.sendStatus(200).send(group);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getBlockedContacts
     * @returns {Promise<WAWebJS.Contact[]>}
     */
    app.post("/getBlockedContacts", (req, res) => {
        client.getBlockedContacts().then((contacts) => {
            res.send(contacts);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getChatById
     * @param {string} chatId
     * @returns {Promise<WAWebJS.Chat>}
     */
    app.post("/getChatById", (req, res) => {
        const {chatId} = req.body;
        client.getChatById(chatId).then((chat) => {
            res.send(chat);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getChats
     * @returns {Promise<WAWebJS.Chat[]>}
     */
    app.post("/getChats", (req, res) => {
        client.getChats().then((chats) => {
            res.send(chats);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getCommonGroups
     * @param {string} contactId
     * @returns {Promise<WAWebJS.GroupChat[]>}
     */
    app.post("/getCommonGroups", (req, res) => {
        const {contactId} = req.body;
        client.getCommonGroups(contactId).then((groups) => {
            res.send(groups);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getContactById
     * @param {string} contactId
     * @returns {Promise<WAWebJS.Contact>}
     */
    app.post("/getContactById", (req, res) => {
        const {contactId} = req.body;
        client.getContactById(contactId).then((contact) => {
            res.send(contact);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getContacts
     * @returns {Promise<WAWebJS.Contact[]>}
     */
    app.post("/getContacts", (req, res) => {
        client.getContacts().then((contacts) => {
            res.send(contacts);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getCountryCode
     * @returns {Promise<string>}
     */
    app.post("/getCountryCode", (req, res) => {
        client.getCountryCode().then((code) => {
            res.send(code);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getFormattedNumber
     * @param {string} number
     */
    app.post("/getFormattedNumber", (req, res) => {
        const {number} = req.body;
        client.getFormattedNumber(number).then((number) => {
            res.send(number);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getInviteInfo
     * @param {string} inviteCode
     * @returns {Promise<Object>}
     */
    app.post("/getInviteInfo", (req, res) => {
        const {inviteCode} = req.body;
        client.getInviteInfo(inviteCode).then((info) => {
            res.send(info);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getNumberId
     * @param {string} number
     * @returns {Promise<string>}
     */
    app.post("/getNumberId", (req, res) => {
        const {number} = req.body;
        client.getNumberId(number).then((id) => {
            res.send(id);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getProfilePicUrl
     * @param {string} contactId
     * @returns {Promise<string>}
     */
    app.post("/getProfilePicUrl", (req, res) => {
        const {contactId} = req.body;
        client.getProfilePicUrl(contactId).then((url) => {
            res.send(url);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getState
     * @returns {Promise<WAWebJS.WAState>}
     */
    app.post("/getState", (req, res) => {
        client.getState().then((state) => {
            res.send(state);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * isRegisteredUser
     * @param {string} number
     * @returns {Promise<boolean>}
     */
    app.post("/isRegisteredUser", (req, res) => {
        const {number} = req.body;
        client.isRegisteredUser(number).then((isRegistered) => {
            res.send(isRegistered);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * markChatRead
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/markChatUnread", (req, res) => {
        const {chatId} = req.body;
        client.markChatUnread(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * muteChat
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/muteChat", (req, res) => {
        const {chatId} = req.body;
        client.muteChat(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * pinChat
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/pinChat", (req, res) => {
        const {chatId} = req.body;
        client.pinChat(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * searchMessages
     * @param {string} query
     * @param {Object} options
     * @param {string} options.chatId
     * @param {number} options.limit
     * @param {string} options.page
     * @returns {Promise<WAWebJS.Message[]>}
     */
    app.post("/searchMessages", (req, res) => {
        const {query, options} = req.body;
        client.searchMessages(query, options).then((messages) => {
            res.send(messages);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * sendMessage
     * @param {string} chatId
     * @param {string} content
     * @param {MessageSendOptions} options
     * @returns {Promise<WAWebJS.Message>}
     */
    app.post("/sendMessage", (req, res) => {
        const {chatId, content, options} = req.body;
        client.sendMessage(chatId, content, options).then((message) => {
            res.send(message);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * sendPresenceAvailable
     * @returns {Promise<boolean>}
     */
    app.post("/sendPresenceAvailable", (req, res) => {
        client.sendPresenceAvailable().then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * sendPresenceUnavailable
     * @returns {Promise<boolean>}
     */
    app.post("/sendPresenceUnavailable", (req, res) => {
        client.sendPresenceUnavailable().then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * sendSeen
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/sendSeen", (req, res) => {
        const {chatId} = req.body;
        client.sendSeen(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * setDisplayName
     * @param {string} displayName
     * @returns {Promise<boolean>}
     */
    app.post("/setDisplayName", (req, res) => {
        const {displayName} = req.body;
        client.setDisplayName(displayName).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * setProfilePicture
     * @param {MessageMedia} media
     * @returns {Promise<boolean>}
     */
    app.post("/setProfilePicture", (req, res) => {
        const {media} = req.body;
        client.setProfilePicture(media).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * setStatus
     * @param {string} status
     * @returns {Promise<boolean>}
     */
    app.post("/setStatus", (req, res) => {
        const {status} = req.body;
        client.setStatus(status).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * unarchiveChat
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/unarchiveChat", (req, res) => {
        const {chatId} = req.body;
        client.unarchiveChat(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * unmuteChat
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/unmuteChat", (req, res) => {
        const {chatId} = req.body;
        client.unmuteChat(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * unpinChat
     * @param {string} chatId
     * @returns {Promise<boolean>}
     */
    app.post("/unpinChat", (req, res) => {
        const {chatId} = req.body;
        client.unpinChat(chatId).then(() => {
            res.sendStatus(200);
        }).catch((err) =>
            res.send(err)
        );
    })

    /**
     * getChatByPhoneNumber
     * @param {string} phoneNumber
     * @returns {Promise<WAWebJS.Chat>}
     */
    app.post("/getChatByPhoneNumber", (req, res) => {
       let {phoneNumber} = req.body;
       if (!phoneNumber.includes("@c.us") && phoneNumber.length === 12) {
           phoneNumber = "33" + phoneNumber.replace("+", "") + "@c.us";
       }
       client.getChats().then((chats) => {
           console.log(chats);
       })
       client.getNumberId(phoneNumber).then((contactId) => {
           console.log(contactId);
           client.getContactById(contactId._serialized).then((chat) => {
               chat.getChat().then((chat) => {
                   res.send(chat);
               })
           })
       })
    })

    app.listen(port, () => {
        console.log(`WhatsApp API listening at http://localhost:${port}`)
    })
}