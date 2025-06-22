const { SlashCommandBuilder, EmbedBuilder, ApplicationCommandOptionType } = require('discord.js');
const { theCatApiKey } = require('../../settings/secrets.json');
const { primaryEmbedColor } = require('../../settings/config.json')
const { request } = require('undici');

module.exports = {
	cooldown: 5,

	data: new SlashCommandBuilder()
		.setName('random-cat')
		.setDescription('Meow! Get a random cat pic.')
		.addStringOption(option =>
			option.setName('breed')
				.setDescription('Choose a cat breed')
				.setRequired(false)
				.setAutocomplete(true)
		),

	async autocomplete(interaction) {
		const focusedValue = interaction.options.getFocused();
		const apiResponse = await request(`https://api.thecatapi.com/v1/breeds`, {
			headers: { 'x-api-key': theCatApiKey }
		});
		const breeds = await apiResponse.body.json();
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
	    	const breedListResponse = await request(`https://api.thecatapi.com/v1/breeds`, {
	    		headers: { 'x-api-key': theCatApiKey }
	    	});
	    	const breeds = await breedListResponse.body.json();
	    	const match = breeds.find(breed => breed.id === selectedBreed);
	    	if (match) breedName = match.name;
	    }

	    const breedParam = selectedBreed ? `?breed_ids=${selectedBreed}` : '';
	    const apiRequest = await request(`https://api.thecatapi.com/v1/images/search${breedParam}`, {
	    	headers: { 'x-api-key': theCatApiKey }
	    });
	    const json = await apiRequest.body.json();
	    const response = json[0];

	    const embed = new EmbedBuilder()
	    	.setColor(primaryEmbedColor)
	    	.setDescription(breedName ? `A \`${breedName}\` cat` : 'A random cat')
	    	.setImage(response.url);

	    await interaction.editReply({ embeds: [embed] });
    },
};
