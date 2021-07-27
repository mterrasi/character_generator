const getAbilities = () => {
	let access_token = 'API_TOKEN'
	let config = {
		'X-Api-Key': `${access_token}`
	};
	const req = axios.get('API_ENDPOINT', {headers: config});
	console.log(req);
	req.then(resp => {
		console.log(`Status code: ${resp.status}`)
		console.log(resp.data);
		let abilities = resp.data;
		document.getElementById("str-table").innerHTML = abilities.Strength
		document.getElementById("int-table").innerHTML = abilities.Intelligence
		document.getElementById("wis-table").innerHTML = abilities.Wisdom
		document.getElementById("dex-table").innerHTML = abilities.Dexterity
		document.getElementById("con-table").innerHTML = abilities.Constitution
		document.getElementById("cha-table").innerHTML = abilities.Charisma
		/* Set Displays */
		document.getElementById("ability_display").style.display = "block"
		document.getElementById("user_input").style.display = "block"
		document.getElementById("directions").style.display = "none"
	})
	.catch(err => {
		console.log(err.toString())
	});
}

const getAttributes = () => {
	let access_token = 'API_TOKEN'
	let config = {
		'X-Api-Key': `${access_token}`
	};
	let payload = {
		"Strength": Number(document.getElementById("str-table").innerHTML),
  		"Intelligence": Number(document.getElementById("int-table").innerHTML),
  		"Wisdom": Number(document.getElementById("wis-table").innerHTML),
  		"Dexterity": Number(document.getElementById("dex-table").innerHTML),
  		"Constitution": Number(document.getElementById("con-table").innerHTML),
  		"Charisma": Number(document.getElementById("cha-table").innerHTML),
  		"char_type": document.getElementById("char_class").value,
  		"char_level": Number(document.getElementById("char_level").value),
  		"sex_choice": document.getElementById("sex_choice").value,
  		"weight_choice": document.getElementById("weight_choice").value,
  		"older": document.getElementById("older").value,
  		"id_quality": document.getElementById("id_quality").value,
  		"name_deity": false,
  		"char_name": document.getElementById("char_name").value
	}
	console.log(payload)
	const req = axios.post('API_ENDPOINT', payload, {headers: config});
	console.log(req)
	req.then(resp => {
		console.log(`Status code: ${resp.status}`)
		console.log(resp.data)
		let new_character = resp.data;
		/* Name/class/level */
		document.getElementById("name").innerHTML = new_character.character.name
		document.getElementById("class").innerHTML = new_character.character.experience[0].class
		document.getElementById("level").innerHTML = document.getElementById("char_level").value
		/* Hit dice/hit points */
		document.getElementById("hit_dice").innerHTML = "Hit Dice"
		document.getElementById("hit_points").innerHTML = new_character.character.current_hp
		document.getElementById("to-hit").innerHTML = "Hit Points"
		/* Abilities */
		document.getElementById("str").innerHTML = new_character.character.abilities.strength
		document.getElementById("int").innerHTML = new_character.character.abilities.intelligence
		document.getElementById("wis").innerHTML = new_character.character.abilities.wisdom
		document.getElementById("dex").innerHTML = new_character.character.abilities.dexterity
		document.getElementById("con").innerHTML = new_character.character.abilities.constitution
		document.getElementById("cha").innerHTML = new_character.character.abilities.charisma
		/* Experience Boost */
		document.getElementById("xp_boost").innerHTML = `%`
		/* Saves */
		document.getElementById("system_shock").innerHTML = new_character.character.saving_throws.system_shock
		document.getElementById("death_ray").innerHTML = new_character.character.saving_throws.poison
		document.getElementById("wand").innerHTML = new_character.character.saving_throws.paralysis
		document.getElementById("petrification").innerHTML = new_character.character.saving_throws.petrification
		document.getElementById("dragon_breath").innerHTML = new_character.character.saving_throws.dragon_breath
		document.getElementById("spell_save").innerHTML = new_character.character.saving_throws.spell
		/* Attributes */
		document.getElementById("sex").innerHTML = new_character.character.sex
		document.getElementById("age").innerHTML = new_character.character.age
		document.getElementById("height").innerHTML = new_character.character.height_foot
		document.getElementById("weight").innerHTML = new_character.character.weight
		document.getElementById("eyes").innerHTML = new_character.character.eye_color
		document.getElementById("hair_color").innerHTML = new_character.character.hair_color
		document.getElementById("hair_type").innerHTML = new_character.character.hair_style
		document.getElementById("hair_length").innerHTML = new_character.character.hair_length
		document.getElementById("skin").innerHTML = new_character.character.skin_color
		document.getElementById("hand").innerHTML = new_character.character.appearance[1]
		document.getElementById("dental").innerHTML = new_character.character.appearance[0]
		document.getElementById("profession").innerHTML = new_character.character.profession
		document.getElementById("m_load").innerHTML = `cn`
		document.getElementById("alignment").innerHTML = new_character.character.alignment
		document.getElementById("gold").innerHTML = `${new_character.character.purse.gold} gp`
		/* Display Result */
		document.getElementById("ability_display").style.display = "none"
		document.getElementById("user_input").style.display = "none"
		document.getElementById("new_character").style.display = "block"
	})
	.catch(err => {
		console.log(err.toString())
	});
}

const resetGenerator = () => {
	/* Clear abilities */
	document.getElementById("str-table").innerHTML = ""
	document.getElementById("int-table").innerHTML = ""
	document.getElementById("wis-table").innerHTML = ""
	document.getElementById("dex-table").innerHTML = ""
	document.getElementById("con-table").innerHTML = ""
	document.getElementById("cha-table").innerHTML = ""
	/* Reset display */
	document.getElementById("directions").style.display = "block"
	document.getElementById("ability_display").style.display = "none"
	document.getElementById("user_input").style.display = "none"
	document.getElementById("new_character").style.display = "none"
	/* Reset form */
	document.getElementById("char_form").reset()
}