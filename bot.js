const Discord = require('discord.js');
const client = new Discord.Client();
var logger = require('winston');
var auth = require('./auth.json');
var fileManager = require('./fileManager.js');
//var commands = require('./commands.js');
const fs = require('fs')
const fetch = require('node-fetch');
const { json } = require('express');
const masterColor = 7871916
var lastUserID = "735550470675759106"
// Require the module in your project

// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot

client.once('ready', () => {
  let rawdata = fs.readFileSync('status.json');
  let status = JSON.parse(rawdata);
  client.user.setPresence(status);
  client.user.setPresence(status)

  console.log('Lore Master is Ready!');
});

client.login(auth.token);


client.on('message', message => {
  let rawdata = fs.readFileSync('status.json');
  let status = JSON.parse(rawdata);
  client.user.setPresence(status);
  if (message.author.id == "779431244222955520"){
    if (message.content.includes(" » ") == true) {
      message.content = message.content.substring(message.content.indexOf("»") + 2);
      console.log(`Updated message: ${message.content}`);
    }
  }
  //member = members.checkMember(message.author.username, message.author.id)
  var channel = message.channel;
  var guild = message.guild;
  var simplify = false;
  console.log(`${message.author.username} sent: ${message} on Channel: ${channel}`)

  if (channel == "779436910841954354") {
    simplify = true;
  }
  
  //if (message.content.substring(0, 1) == '!') {
    //score = commands.command(Discord, client, message, channel, score, IP, simplify)
  //}

  if (message.author.id == lastUserID) {
    score = 0;
  } else {
    lastUserID = message.author.id
  }
  //member = members.addScore(message.author.username, message.author.id, score, member)
    
});