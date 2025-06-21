const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	cooldown: 5,
	data: new SlashCommandBuilder()
		.setName('bonk')
		.setDescription('Bonk'),
	async execute(interaction) {
		await interaction.reply('Bonk');
	},
};