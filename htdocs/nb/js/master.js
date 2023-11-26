// master.js 0.07b (2023/11/26)

const mp = 'master/';


/////////////////////////////////////////////////////////////////////////////////
// Unit exchange ////////////////////////////////////////////////////////////////////////

// Unit exchange init
const initUnit = function( com ){
	let code = '';
	if( com != 'init' ){ code = document.getElementById( "food_no" ).value; }

	$.post(  mp + "gm-unit.cgi", { command:com, code:code }, function( data ){ $( "#LF" ).html( data );});

	flashBW();
	dlf = true;
	displayBW();
};

// Direct unit exchange button
const directUnit = function( code ){
	$.post( mp + "gm-unit.cgi", { command:'init', code:code }, function( data ){ $( "#LF" ).html( data );});

	dlf = true;
	displayBW();
};

// Update unit exchange button
const updateUint = function(){
	const code = document.getElementById( "food_no" ).value;

	if( code != '' ){
		const uk0 = document.getElementById( "uk0" ).value;
		const uk1 = document.getElementById( "uk1" ).value;
		const uk2 = document.getElementById( "uk2" ).value;
		const uk3 = document.getElementById( "uk3" ).value;
		const uk4 = document.getElementById( "uk4" ).value;
		const uk5 = document.getElementById( "uk5" ).value;
		const uk6 = document.getElementById( "uk6" ).value;
		const uk7 = document.getElementById( "uk7" ).value;
		const uk8 = document.getElementById( "uk8" ).value;
		const uk9 = document.getElementById( "uk9" ).value;

		const uv0 = document.getElementById( "uv0" ).value;
		const uv1 = document.getElementById( "uv1" ).value;
		const uv2 = document.getElementById( "uv2" ).value;
		const uv3 = document.getElementById( "uv3" ).value;
		const uv4 = document.getElementById( "uv4" ).value;
		const uv5 = document.getElementById( "uv5" ).value;
		const uv6 = document.getElementById( "uv6" ).value;
		const uv7 = document.getElementById( "uv7" ).value;
		const uv8 = document.getElementById( "uv8" ).value;
		const uv9 = document.getElementById( "uv9" ).value;

		const note = document.getElementById( "note" ).value;
		$.post(  mp + "gm-unit.cgi", { command:'update', code:code, uk0:uk0, uk1:uk1, uk2:uk2, uk3:uk3, uk4:uk4, uk5:uk5, uk6:uk6, uk7:uk7, uk8:uk8, uk9:uk9,
			uv0:uv0, uv1:uv1, uv2:uv2, uv3:uv3, uv4:uv4, uv5:uv5, uv6:uv6, uv7:uv7, uv8:uv8, uv9:uv9, note:note}, function( data ){
			$( "#LF" ).html( data );
			displayVIDEO( code + ' saved' );
		});			
	}
};


// Overall unit exchange
const exUnit = function( code ){
	const bunit = document.getElementById( "bunit" ).value;
	const aunit = document.getElementById( "aunit" ).value;
	$.post(  mp + "gm-unit.cgi", { command:'exunit', code:code, bunit:bunit, aunit:aunit }, function( data ){
		displayVIDEO( 'Exchange' );
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Food color ////////////////////////////////////////////////////////////////////////

// Food color init
const initColor = function( com ){
	let  code = document.getElementById( "food_no" ).value;
	if( com == 'init' ){ code = ''; }

	$.post( mp + "gm-color.cgi", { command:com, code:code }, function( data ){
		$( "#LF" ).html( data );

		flashBW();
		dlf = true;
		displayBW();
	});
};

// Direct food color button
const directColor = function( code ){
	$.post( mp + "gm-color.cgi", { command:'init', code:code }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// Update food color
const updateColor = function(){
	const code = document.getElementById( "food_no" ).value;
	if( code != '' ){
		let color1 = 0
		let color2 = 0
		let color1h = 0
		let color2h = 0

		for ( let i = 0; i <= 11; i++ ) {
			if( document.getElementById( "color1_" + i ).checked ){ color1 = i; }
			if( document.getElementById( "color2_" + i).checked ){ color2 = i; }
			if( document.getElementById( "color1h_" + i ).checked ){ color1h = i; }
			if( document.getElementById( "color2h_" + i ).checked ){ color2h = i; }
		}

		$.post( mp + "gm-color.cgi", { command:'update', code:code, color1:color1, color2:color2, color1h:color1h, color2h:color2h }, function( data ){
			$( "#LF" ).html( data );

			displayVIDEO( code + ' saved' );
		});
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Food name dictionary ////////////////////////////////////////////////////////////////////////

// Food name dictionary init
const initDic = function( command, sg, org_name, dfn ){
	$.post( mp + "gm-dic.cgi", { command:'menu' }, function( data ){ $( "#LINE" ).html( data );});
	$.post( mp + "gm-dic.cgi", { command:command, sg:sg, org_name:org_name, dfn:dfn }, function( data ){ $( "#L1" ).html( data );});

	flashBW();
	dl1 = true;
	dline = true;
	displayBW();
};

// Food name dictionary Sub group
const changeDic = function( sg ){
	$.post( mp + "gm-dic.cgi", { command:'change', sg:sg }, function( data ){ $( "#L1" ).html( data );});
};

// Direct food name dictionary button
const saveDic = function( org_name, sg ){
	const aliases = document.getElementById( org_name ).value;
	const dfn = document.getElementById( 'dfn_' + org_name ).value;
	$.post( mp + "gm-dic.cgi", { command:'update', org_name:org_name, aliases:aliases, sg:sg, dfn:dfn }, function( data ){
//		$( "#L1" ).html( data );
		displayVIDEO( org_name + ' modified' );
	});
};

// Add new food into dictionary button
const newDic = function(){
	const org_name = document.getElementById( 'new_org_name' ).value;
	const aliases = document.getElementById( 'new_alias' ).value;
	const sg = document.getElementById( 'new_fg' ).value;
	const dfn = document.getElementById( 'dic_def_fn' ).value;
	$.post( mp + "gm-dic.cgi", { command:'new', org_name:org_name, aliases:aliases, sg:sg, dfn:dfn }, function( data ){
//		$( "#L1" ).html( data );
		displayVIDEO( org_name + ' saved' );
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Allergen ////////////////////////////////////////////////////////////////////////

// Allergen init
const initAllergen = function(){
	$.post( mp + "gm-allergen.cgi", { command:'init' }, function( data ){
		$( "#LF" ).html( data );

		flashBW();
		dlf = true;
		displayBW();
	});
};

// Allergen change class
const changeAllergen = function(){
	const allergen = document.getElementById( 'allergen' ).value;
	$.post( mp + "gm-allergen.cgi", { command:'change', allergen:allergen }, function( data ){ $( "#LF" ).html( data );});
};

// Direct allergen button
const directAllergen = function( code ){
	$.post( mp + "gm-allergen.cgi", { command:'init', code:code, allergen:1 }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// Allergen ON
const onAllergen = function(){
	const allergen = document.getElementById( 'allergen' ).value;
	const code = document.getElementById( 'code' ).value;
	$.post( mp + "gm-allergen.cgi", { command:'on', code:code, allergen:allergen }, function( data ){
		$( "#LF" ).html( data );
		displayVIDEO( code + ':allergen ON' );
	});
};

// Allergen OFF
const offAllergen = function( code ){
	const allergen = document.getElementById( 'allergen' ).value;
	$.post( mp + "gm-allergen.cgi", { command:'off', code:code, allergen:allergen }, function( data ){
		$( "#LF" ).html( data );
		displayVIDEO( code + ':allergen OFF' );
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Green yellow color vegetable ////////////////////////////////////////////////////////////////////////

// GYCV init
const initGYCV = function( com ){
	if( com == 'init' ){ flashBW(); }
	$.post( mp + "gm-gycv.cgi", { command:com }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// GYCV ON
const onGYCV = function(){
	const food_no = document.getElementById( 'food_no' ).value;
	$.post( mp + "gm-gycv.cgi", { command:'on', food_no:food_no }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// GYCV OFF
const offGYCV = function( food_no ){
	$.post( mp + "gm-gycv.cgi", { command:'off', food_no:food_no }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Shun ////////////////////////////////////////////////////////////////////////

// Shun init
const initShun = function( com ){
	if( com == 'init' ){ flashBW(); }
	$.post( mp + "gm-shun.cgi", { command:com }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// Direct shun button
const directShun = function( code ){
	$.post( mp + "gm-shun.cgi", { command:'init', code:code }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// Shun ON
const onShun = function(){
	const code = document.getElementById( 'code' ).value;
	const shun1s = document.getElementById( 'shun1s' ).value;
	const shun1e = document.getElementById( 'shun1e' ).value;
	const shun2s = document.getElementById( 'shun2s' ).value;
	const shun2e = document.getElementById( 'shun2e' ).value;
	$.post( mp + "gm-shun.cgi", { command:'on', code:code, shun1s:shun1s, shun1e:shun1e, shun2s:shun2s, shun2e:shun2e }, function( data ){
		$( "#LF" ).html( data );
		displayVIDEO( code + ':Shun ON' );
	});
};

// Shun OFF
const offShun = function( code ){
	$.post( mp + "gm-shun.cgi", { command:'off', code:code }, function( data ){
		$( "#LF" ).html( data );
		displayVIDEO( code + ':Shun OFF' );
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Food search log ////////////////////////////////////////////////////////////////////////

// Food search log init
const initSlogf = function( com ){
	$.post( mp + "gm-slogf.cgi", { command:com }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Account ////////////////////////////////////////////////////////////////////////

// Account init
const initAccount = function( com ){
	$.post( mp + "gm-account.cgi", { command:com }, function( data ){
		$( "#L1" ).html( data );
		
		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Edit account
const editAccount = function( target_uid ){
	$.post( mp + "gm-account.cgi", { command:'edit', target_uid:target_uid }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		displayBW();
	});
};

// Update account
const saveAccount = function( target_uid ){
	const target_pass = document.getElementById( 'target_pass' ).value;
	const target_mail = document.getElementById( 'target_mail' ).value;
	const target_aliasu = document.getElementById( 'target_aliasu' ).value;
	const target_status = document.getElementById( 'target_status' ).value;
	const target_language = document.getElementById( 'target_language' ).value;

	$.post( mp + "gm-account.cgi", { command:'save', target_uid:target_uid, target_pass:target_pass, target_mail:target_mail, target_aliasu:target_aliasu, target_status:target_status, target_language:target_language }, function( data ){
		$( "#L1" ).html( data );

		dl2 = true;
		dl2 = false;
		displayBW();
		displayVIDEO( target_uid + ' saved' );
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Memory ////////////////////////////////////////////////////////////////////////

// Memory init
const initMemory = function(){
	$.post( mp + "gm-memory.cgi", { command:'init', post_process:'front' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Save New category
const saveCategory = function(){
	let category = document.getElementById( 'category' ).value;
	if( category != '' ){
		$.post( mp + "gm-memory.cgi", { command:'save_category', category:category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( '(>_<)category name!!' );
	}
};

// Change category name
const changeCategory = function( category ){
	let new_category = document.getElementById( category ).value;
	if( category != '' ){
		$.post( mp + "gm-memory.cgi", { command:'change_category', category:category, new_category:new_category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( '(>_<)category name!!' );
	}
};

// Delete category
const deleteCategory = function( category, delete_check_no ){
	if( document.getElementById( delete_check_no ).checked ){
		$.post( mp + "gm-memory.cgi", { command:'delete_category', category:category }, function( data ){
			$( "#L1" ).html( data );

			flashBW();
			dl1	= true;
			displayBW();
		});
	}else{
		displayVIDEO( 'Check!' );
	}
};

// List each pointer
const listPointerGM = function( category ){
	$.post( mp + "gm-memory.cgi", { command:'list_pointer', category:category, post_process:'front' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// New pointer form
const newPMemoryGM = function( code, category, pointer, post_process ){
	$.post( mp + "gm-memory.cgi", { command:'new_pointer', code:code, category:category, pointer:pointer, post_process:post_process }, function( data ){
		$( "#LF" ).html( data );

		dl1 = false;
		if( post_process == 'front'){ dl2 = false; }
		dlf = true;
		displayBW();
	});

	$.post( "photo.cgi", { command:'view_series', code:code, base:'memory' }, function( data ){
		$( "#LM" ).html( data );

		dlm = true;
		displayBW();
	});
};

// Save pointer
const savePMemory = function( category, post_process ){
	const pointer = document.getElementById( 'pointer' ).value;
	const memory = document.getElementById( 'memory' ).value;
	const rank = document.getElementById( 'rank' ).value;

	if( pointer != '' ){
		if( post_process == 'front'){
			$.post( mp + "gm-memory.cgi", { command:'save_pointer', memory:memory, category:category, pointer:pointer, rank:rank, post_process:post_process }, function( data ){});
			$.post( mp + "gm-memory.cgi", { command:'list_pointer', category:category, post_process:post_process }, function( data ){ $( "#L1" ).html( data );});
			dl1 = true;
			dl2 = false;
			dlm = false;
		}else{
			$.post( mp + "gm-memory.cgi", { command:'save_pointer', memory:memory, category:category, pointer:pointer, rank:rank, post_process:post_process }, function( data ){});
		}
		pullHW();
		dlf = false;
		dlm = false;
		displayBW();

		displayVIDEO( 'Saved' );
	}else{
		displayVIDEO( '(>_<)Pointer!!' );
	}
}

// Move pointer
const movePMemory = function( category, pointer, post_process ){
	const memory = document.getElementById( 'memory' ).value;
	const rank = document.getElementById( 'rank' ).value;
	const mvcategory = document.getElementById( 'mvcategory' ).value;

	if( post_process == 'front'){
		$.post( mp + "gm-memory.cgi", { command:'move_pointer', memory:memory, category:category, pointer:pointer, rank:rank, mvcategory:mvcategory }, function( data ){ $( "#L2" ).html( data );});
		$.post( mp + "gm-memory.cgi", { command:'init' }, function( data ){ $( "#L1" ).html( data );});

		dl1 = true;
	}else{
		$.post( mp + "gm-memory.cgi", { command:'move_pointer', memory:memory, category:category, pointer:pointer, rank:rank, mvcategory:mvcategory }, function( data ){});
	}

	dlf = false;
	displayBW();
	displayVIDEO( 'Moved' );
}

// Delete pointer
const deletePMemory = function( category, pointer, post_process ){
	if( document.getElementById( 'deletepm_check' ).checked ){
		if( post_process == 'front'){
			$.post( mp + "gm-memory.cgi", { command:'delete_pointer', category:category, pointer:pointer, post_process }, function( data ){ $( "#L2" ).html( data );});
			$.post( mp + "gm-memory.cgi", { command:'init' }, function( data ){ $( "#L1" ).html( data );});
			dl1 = true;
		}else{
			$.post( mp + "gm-memory.cgi", { command:'delete_pointer', category:category, pointer:pointer, post_process }, function( data ){});
		}
		dlf = false;
	}else{
		displayVIDEO( '(>_<)check!!' );
	}

	displayBW();
};

/////////////////////////////////////////////////////////////////////////////////
// Bomd James bond ////////////////////////////////////////////////////////////////////////

const initBond = function(){
	$.post( mp + "gm-bond.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

const crossBond = function(){
	const urls = document.getElementById( 'urls' ).value;
	if( document.getElementById( 'open_nb' ).checked ){ var open_nb = 1; }else{var open_nb = 0; }

	$.post( mp + "gm-bond.cgi", { command:'cross', urls:urls, open_nb:open_nb }, function( data ){
		$( "#L2" ).html( data );
		dl2 = true;
		displayBW();
	});
};

