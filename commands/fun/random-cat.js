const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { theCatApiKey } = require('../../settings/secrets.json');
const { primaryEmbedColor } = require('../../settings/config.json');
const { request } = require('undici');

async function getApiBodyResponse(path) {
	const apiResponse = await request(`https://api.thecatapi.com/v1/${path}`, {
		headers: { 'x-api-key': theCatApiKey },
	});
	const body = await apiResponse.body.json();
	return body;
}

module.exports = {
	cooldown: 5,

	data: new SlashCommandBuilder()
		.setName('random-cat')
		.setDescription('Meow! Get a random cat pic.')
		.addStringOption(option =>
			option.setName('breed')
				.setDescription('Choose a cat breed')
				.setRequired(false)
				.setAutocomplete(true),
		),

	async autocomplete(interaction) {
		const focusedValue = interaction.options.getFocused();
		const breeds = await getApiBodyResponse('breeds');
		const filtered = breeds
			.filter(breed => breed.name.toLowerCase().includes(focusedValue.toLowerCase()))
			.slice(0, 25)
			.map(breed => ({ name: breed.name, value: breed.id }));

		await interaction.respond(filtered);
	},

	async execute(interaction) {
	    await interaction.deferReply();

	    const selectedBreed = interaction.options.getString('breed');
	    let breedName = null;

	    if (selectedBreed) {
			const breeds = await getApiBodyResponse('breeds');
	    	const match = breeds.find(breed => breed.id === selectedBreed);
	    	if (match) breedName = match.name;
	    }

	    const breedParam = selectedBreed ? `?breed_ids=${selectedBreed}` : '';
		const json = await getApiBodyResponse(`images/search${breedParam}`);
	    const response = json[0];

	    const embed = new EmbedBuilder()
	    	.setColor(primaryEmbedColor)
	    	.setDescription(breedName ? `A \`${breedName}\` cat` : 'A random cat')
	    	.setImage(response.url);

	    await interaction.editReply({ embeds: [embed] });
	},
};
