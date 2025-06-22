const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { primaryEmbedColor } = require('../../settings/config.json')
const { request } = require('undici');
const { trim } = require('../../tools/string');

module.exports = {
	cooldown: 5,
	data: new SlashCommandBuilder()
		.setName('urban-dictionary')
		.setDescription('Search a term in Urban Dictionary.')
		.addStringOption(option => 
			option.setName('term')
				.setDescription('What term are you looking for?')
				.setMaxLength(50)
				.setRequired(true)
		)
		.addStringOption(option =>
			option.setName('mode')
				.setDescription('How would you like to sort posts?')
				.addChoices(
					{ name: 'Most Likes (default)', value: 'l' },
					{ name: 'Most Dislikes', value: 'd' },
					{ name: 'Random', value: 'r' },
				)
				.setRequired(false)
		),

	async execute(interaction) {
		await interaction.deferReply();

		const mode = interaction.options.getString('mode') ?? 'l';
		const term = interaction.options.getString('term');
		const query = new URLSearchParams({ term });

		const dictResult = await request(`https://api.urbandictionary.com/v0/define?${query}`);
		const { list } = await dictResult.body.json();
		
		if (!list.length) {
			return interaction.editReply(`No results found for **${term}**.`);
		}

		let selectedPost;

		if (mode === 'l') {
			selectedPost = list.sort((a, b) => b.thumbs_up - a.thumbs_up)[0];
		} else if (mode === 'd') {
			selectedPost = list.sort((a, b) => b.thumbs_down - a.thumbs_down)[0];
		} else if (mode === 'r') {
			selectedPost = list[Math.floor(Math.random() * list.length)];
		}

		const modeMapping = {
			'l': 'Most Likes',
			'd': 'Most Dislikes',
			'r': 'Random'
		};

		const embed = new EmbedBuilder()
			.setColor(primaryEmbedColor)
			.setAuthor({ name: `"${term}"`, url: selectedPost.permalink })
			.setDescription(`-# Content is not filtered. Use at your own risk.`)
			.addFields(
				{ name: 'Definition', value: trim(selectedPost.definition, 512) },
				{ name: 'Example', value: trim(selectedPost.example, 512) },
				{ name: 'Rating', value: `<:thumbs_up:1386095747509784586> \`${selectedPost.thumbs_up}\` • <:thumbs_down:1386095758473957557> \`${selectedPost.thumbs_down}\`` },
				{ name: 'Search Method', value: modeMapping[mode] })
			.setFooter({ text: 'Urban Dictionary' });

		interaction.editReply({ embeds : [embed] });
	},
};
