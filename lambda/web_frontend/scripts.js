const getAbilities = () => {
	let access_token = 'HDqv6PvHy53S43uGQHbSirxEGOqRVOO9i4O4P1a3'
	let config = {
		'X-Api-Key': `${access_token}`
	};
	const req = axios.get('https://qhs15o4rab.execute-api.us-east-2.amazonaws.com/test/', {headers: config});
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
	let access_token = 'HDqv6PvHy53S43uGQHbSirxEGOqRVOO9i4O4P1a3'
	let config = {
		'X-Api-Key': `${access_token}`
	};
	let char_level_input = document.getElementById("char_level").value
	if (char_level_input == '') {
		char_level_req = 1
	} else if (char_level_input < 0) {
		char_level_req = 0
	} else {
		char_level_req = document.getElementById("char_level").value
	}
	let char_name_input = document.getElementById("char_name").value
	if (char_name_input == '') {
		var char_name_req = "random"
	} else {
		var char_name_req = document.getElementById("char_name").value
	}
	if (document.getElementById("char_class").value != "cleric") {
		var name_deity_option = "no"
	} else {
		var name_deity_option = document.getElementById("name_deity").value
	}
	let payload = {
		"Strength": Number(document.getElementById("str-table").innerHTML),
  		"Intelligence": Number(document.getElementById("int-table").innerHTML),
  		"Wisdom": Number(document.getElementById("wis-table").innerHTML),
  		"Dexterity": Number(document.getElementById("dex-table").innerHTML),
  		"Constitution": Number(document.getElementById("con-table").innerHTML),
  		"Charisma": Number(document.getElementById("cha-table").innerHTML),
  		"char_type": document.getElementById("char_class").value,
  		"char_level": Number(char_level_req),
  		"sex_choice": document.getElementById("sex_choice").value,
  		"weight_choice": document.getElementById("weight_choice").value,
  		"older": document.getElementById("older").value,
  		"id_quality": document.getElementById("id_quality").value,
  		"name_deity": name_deity_option,
  		"char_name": char_name_req
	}
	console.log(payload)
	const req = axios.post('https://qhs15o4rab.execute-api.us-east-2.amazonaws.com/test/', payload, {headers: config});
	console.log(req)
	req.then(resp => {
		console.log(`Status code: ${resp.status}`)
		console.log(resp.data)
		let new_character = resp.data;
		/* Name/class/level */
		document.getElementById("name").innerHTML = new_character.ics.character.name
		document.getElementById("class").innerHTML = new_character.ics.character.experience[0].class
		document.getElementById("level").innerHTML = char_level_req
		/* Hit dice/hit points */
		document.getElementById("hit_dice").innerHTML = new_character.display.hit_dice
		document.getElementById("hit_points").innerHTML = new_character.ics.character.current_hp
		document.getElementById("to-hit").innerHTML =new_character.display.to_hit
		/* Get Prime boost */
		let prime_ability = new_character.ics.character.experience[0].prime
		/* Abilities */
		if (prime_ability  == "strength") {
			document.getElementById("str").innerHTML = `${new_character.ics.character.abilities.strength} + ${char_level_req}`
		} else {
			document.getElementById("str").innerHTML = new_character.ics.character.abilities.strength
		}
		if (prime_ability == "intelligence") {
			document.getElementById("int").innerHTML = `${new_character.ics.character.abilities.intelligence} + ${char_level_req}`
		} else {
			document.getElementById("int").innerHTML = new_character.ics.character.abilities.intelligence
		}
		if (prime_ability == "wisdom") {
			document.getElementById("wis").innerHTML = `${new_character.ics.character.abilities.wisdom} + ${char_level_req}`
		} else {
			document.getElementById("wis").innerHTML = new_character.ics.character.abilities.wisdom
		}
		document.getElementById("dex").innerHTML = new_character.ics.character.abilities.dexterity
		document.getElementById("con").innerHTML = new_character.ics.character.abilities.constitution
		document.getElementById("cha").innerHTML = new_character.ics.character.abilities.charisma
		/* Experience Boost */
		document.getElementById("adjustments").innerHTML = new_character.display.adjustments
		document.getElementById("xp_boost").innerHTML = new_character.ics.character.experience[0].bonus_xp
		/* Saves */
		document.getElementById("system_shock").innerHTML = new_character.ics.character.saving_throws.system_shock
		document.getElementById("death_ray").innerHTML = new_character.ics.character.saving_throws.poison
		document.getElementById("wand").innerHTML = new_character.ics.character.saving_throws.paralysis
		document.getElementById("petrification").innerHTML = new_character.ics.character.saving_throws.petrification
		document.getElementById("dragon_breath").innerHTML = new_character.ics.character.saving_throws.dragon_breath
		document.getElementById("spell_save").innerHTML = new_character.ics.character.saving_throws.spell
		/* Attributes */
		document.getElementById("sex").innerHTML = new_character.ics.character.sex
		document.getElementById("age").innerHTML = new_character.ics.character.age
		document.getElementById("height").innerHTML = new_character.display.height
		document.getElementById("weight").innerHTML = `${new_character.ics.character.weight}lbs`
		document.getElementById("eyes").innerHTML = new_character.ics.character.eye_color
		document.getElementById("hair_color").innerHTML = new_character.ics.character.hair_color
		document.getElementById("hair_type").innerHTML = new_character.ics.character.hair_style
		document.getElementById("hair_length").innerHTML = new_character.ics.character.hair_length
		document.getElementById("skin").innerHTML = new_character.ics.character.skin_color
		document.getElementById("hand").innerHTML = new_character.display.handedness
		document.getElementById("dental").innerHTML = new_character.display.dental_status
		document.getElementById("identifying_quality").innerHTML = new_character.display.id_quality
		document.getElementById("profession").innerHTML = new_character.display.profession
		document.getElementById("prof_def").innerHTML = new_character.display.profession_definition
		if (prime_ability == "strength") {
			var m_load = Number(new_character.ics.character.abilities.strength + char_level_req) * 150
		} else {
			var m_load = Number(new_character.ics.character.abilities.strength) * 150
		}
		document.getElementById("m_load").innerHTML = `${m_load}cn`
		document.getElementById("alignment").innerHTML = new_character.ics.character.alignment
		document.getElementById("gold").innerHTML = `${new_character.ics.character.purse.gold}gp`
		/* Display Result */
		document.getElementById("ability_display").style.display = "none"
		document.getElementById("user_input").style.display = "none"
		document.getElementById("new_character").style.display = "block"
		if (new_character.ics.character.experience[0].class == "Cleric") {
			document.getElementById("deity_name").innerHTML = new_character.display.deity_name
			document.getElementById("domain").innerHTML = new_character.display.domain
			document.getElementById("edict").innerHTML = new_character.display.edict
			document.getElementById("anathema").innerHTML = new_character.display.anathema
			document.getElementById("turning_events").innerHTML = new_character.display.turning_event_stats
			document.getElementById("spell_slots_cleric").innerHTML = new_character.display.spell_slots
			document.getElementById("cleric_info").style.display = "block"
		} else if (new_character.ics.character.experience[0].class == "Magic User") {
			document.getElementById("starting_spell").innerHTML = new_character.ics.character.experience.spellbook.spells
			document.getElementById("magic_info").style.display = "block"
		}
		sessionStorage.setItem('name', new_character.ics.character.name)
		sessionStorage.setItem('ics_data', JSON.stringify(new_character.ics));
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
	document.getElementById("cleric_info").style.display = "none"
	document.getElementById("magic_info").style.display = "none"
	/* Reset form */
	document.getElementById("char_form").reset()
	document.getElementById("deity_name_input").style.display = "none"
}

const displayDeityName = () => {
	let selected = document.getElementById("char_class").value
	if (selected == "cleric") {
		document.getElementById("deity_name_input").style.display = "block"
	} else {
		document.getElementById("deity_name_input").style.display = "none"
	}
}

const download = (content, fileName, contentType) => {
	const a = document.createElement("a");
	const file = new Blob([content], { type: contentType });
	a.href = URL.createObjectURL(file);
	a.download = fileName;
	a.click();
}

const downloadCharacterSheet = () => {
	var d = new Date();
	var n = d.toISOString();
	var name = sessionStorage.getItem('name');
	var fileName = n.slice(0, 10) + "_" + name + ".json";
	jsonData = sessionStorage.getItem('ics_data');
	download(jsonData, fileName, "text/plain");
}