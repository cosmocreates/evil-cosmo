const { SlashCommandBuilder, EmbedBuilder, AttachmentBuilder, MessageFlags } = require('discord.js');
const { primaryEmbedColor } = require('../../settings/config.json');
const path = require('path');
const package = require('../../package.json');

module.exports = {
	cooldown: 5,

	data: new SlashCommandBuilder()
		.setName('bot-info')
		.setDescription('Who, now?'),

	async execute(interaction) {
		const imagePath = path.resolve(__dirname, '../../assets/images/gnu-logo-banner.png');
		const imageAttachment = new AttachmentBuilder(imagePath, { name: 'gnu-logo-banner.png' });

		const dependenciesFormatted = Object.entries(package.dependencies)
			.map(([key, value]) => `\`${key}\` (${value})`)
			.join('\n');
			
		const embed = new EmbedBuilder()
			.setColor(primaryEmbedColor)
			.setDescription(`<:info:1386217256354054149> \`${package.description}\`
		<:github:1386217246485119037> [View on GitHub](${package.github})`)
			.addFields(
				{ name: 'Dependencies', value: dependenciesFormatted, inline: true },
				{ name: 'Version', value: `\`v${package.version}\``, inline: true },
			)
			.setImage('attachment://gnu-logo-banner.png');

		await interaction.reply({ embeds: [embed], files: [imageAttachment], flags: MessageFlags.Ephemeral });
	},
};