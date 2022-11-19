// master.js 0.04b 20220712
/////////////////////////////////////////////////////////////////////////////////
// Unit exchange ////////////////////////////////////////////////////////////////////////

// Unit exchange init
var initUnitc = function( com ){
	if( com == 'init' ){
		var code = '';
		closeBroseWindows( 0 );
	} else{
		var code = document.getElementById( "food_no" ).value;
	}

	$.post( "gm-unitc.cgi", { command:com, code:code }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Direct unit exchange button
var directUnitc = function( code ){
	$.post( "gm-unitc.cgi", { command:'init', code:code }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};


// Unit exchange init
var initUnit = function( com ){
	if( com == 'init' ){
		var code = '';
	} else{
		var code = document.getElementById( "food_no" ).value;
	}

	$.post( "gm-unit.cgi", { command:com, code:code }, function( data ){ $( "#LF" ).html( data );});

	flashBW();
	dl1 = true;
	dlf = true;
	displayBW();
};

// Direct unit exchange button
var directUnit = function( code ){
	$.post( "gm-unit.cgi", { command:'init', code:code }, function( data ){ $( "#LF" ).html( data );});

	dlf = true;
	displayBW();
};

// Update unit exchange button
var updateUint = function(){
	var code = document.getElementById( "food_no" ).value;

	if( code != '' ){
		var uk0 = document.getElementById( "uk0" ).value;
		var uk1 = document.getElementById( "uk1" ).value;
		var uk2 = document.getElementById( "uk2" ).value;
		var uk3 = document.getElementById( "uk3" ).value;
		var uk4 = document.getElementById( "uk4" ).value;
		var uk5 = document.getElementById( "uk5" ).value;
		var uk6 = document.getElementById( "uk6" ).value;
		var uk7 = document.getElementById( "uk7" ).value;
		var uk8 = document.getElementById( "uk8" ).value;
		var uk9 = document.getElementById( "uk9" ).value;

		var uv0 = document.getElementById( "uv0" ).value;
		var uv1 = document.getElementById( "uv1" ).value;
		var uv2 = document.getElementById( "uv2" ).value;
		var uv3 = document.getElementById( "uv3" ).value;
		var uv4 = document.getElementById( "uv4" ).value;
		var uv5 = document.getElementById( "uv5" ).value;
		var uv6 = document.getElementById( "uv6" ).value;
		var uv7 = document.getElementById( "uv7" ).value;
		var uv8 = document.getElementById( "uv8" ).value;
		var uv9 = document.getElementById( "uv9" ).value;

		var note = document.getElementById( "note" ).value;
		$.post( "gm-unit.cgi", { command:'update', code:code, uk0:uk0, uk1:uk1, uk2:uk2, uk3:uk3, uk4:uk4, uk5:uk5, uk6:uk6, uk7:uk7, uk8:uk8, uk9:uk9,
			uv0:uv0, uv1:uv1, uv2:uv2, uv3:uv3, uv4:uv4, uv5:uv5, uv6:uv6, uv7:uv7, uv8:uv8, uv9:uv9, note:note}, function( data ){ $( "#LF" ).html( data );});
		displayVIDEO( code + ' saved' );
	}
};


// Overall unit exchange
var exUnit = function( code ){
	var bunit = document.getElementById( "bunit" ).value;
	var aunit = document.getElementById( "aunit" ).value;
	$.post( "gm-unit.cgi", { command:'exunit', code:code, bunit:bunit, aunit:aunit }, function( data ){
		displayVIDEO( 'Exchange' );
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Food color ////////////////////////////////////////////////////////////////////////

// Food color init
var initColor = function( com ){
	if( com == 'init' ){
		var code = '';
		closeBroseWindows( 0 );
	} else{
		var code = document.getElementById( "food_no" ).value;
	}

	$.post( "gm-color.cgi", { command:com, code:code }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Direct food color button
var directColor = function( code ){
	$.post( "gm-color.cgi", { command:'init', code:code }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Update food color
var updateColor = function(){
	var code = document.getElementById( "food_no" ).value;
	if( code != '' ){
		var color1 = 0
		var color2 = 0
		var color1h = 0
		var color2h = 0

		if( document.getElementById( "color1_0" ).checked ){ color1 = 0; }
		if( document.getElementById( "color1_1" ).checked ){ color1 = 1; }
		if( document.getElementById( "color1_2" ).checked ){ color1 = 2; }
		if( document.getElementById( "color1_3" ).checked ){ color1 = 3; }
		if( document.getElementById( "color1_4" ).checked ){ color1 = 4; }
		if( document.getElementById( "color1_5" ).checked ){ color1 = 5; }
		if( document.getElementById( "color1_6" ).checked ){ color1 = 6; }
		if( document.getElementById( "color1_7" ).checked ){ color1 = 7; }
		if( document.getElementById( "color1_8" ).checked ){ color1 = 8; }
		if( document.getElementById( "color1_9" ).checked ){ color1 = 9; }
		if( document.getElementById( "color1_10" ).checked ){ color1 = 10; }
		if( document.getElementById( "color1_11" ).checked ){ color1 = 11; }

		if( document.getElementById( "color2_0" ).checked ){ color2 = 0; }
		if( document.getElementById( "color2_1" ).checked ){ color2 = 1; }
		if( document.getElementById( "color2_2" ).checked ){ color2 = 2; }
		if( document.getElementById( "color2_3" ).checked ){ color2 = 3; }
		if( document.getElementById( "color2_4" ).checked ){ color2 = 4; }
		if( document.getElementById( "color2_5" ).checked ){ color2 = 5; }
		if( document.getElementById( "color2_6" ).checked ){ color2 = 6; }
		if( document.getElementById( "color2_7" ).checked ){ color2 = 7; }
		if( document.getElementById( "color2_8" ).checked ){ color2 = 8; }
		if( document.getElementById( "color2_9" ).checked ){ color2 = 9; }
		if( document.getElementById( "color2_10" ).checked ){ color2 = 10; }
		if( document.getElementById( "color2_11" ).checked ){ color2 = 11; }

		if( document.getElementById( "color1h_0" ).checked ){ color1h = 0; }
		if( document.getElementById( "color1h_1" ).checked ){ color1h = 1; }
		if( document.getElementById( "color1h_2" ).checked ){ color1h = 2; }
		if( document.getElementById( "color1h_3" ).checked ){ color1h = 3; }
		if( document.getElementById( "color1h_4" ).checked ){ color1h = 4; }
		if( document.getElementById( "color1h_5" ).checked ){ color1h = 5; }
		if( document.getElementById( "color1h_6" ).checked ){ color1h = 6; }
		if( document.getElementById( "color1h_7" ).checked ){ color1h = 7; }
		if( document.getElementById( "color1h_8" ).checked ){ color1h = 8; }
		if( document.getElementById( "color1h_9" ).checked ){ color1h = 9; }
		if( document.getElementById( "color1h_10" ).checked ){ color1h = 10; }
		if( document.getElementById( "color1h_11" ).checked ){ color1h = 11; }

		if( document.getElementById( "color2h_0" ).checked ){ color2h = 0; }
		if( document.getElementById( "color2h_1" ).checked ){ color2h = 1; }
		if( document.getElementById( "color2h_2" ).checked ){ color2h = 2; }
		if( document.getElementById( "color2h_3" ).checked ){ color2h = 3; }
		if( document.getElementById( "color2h_4" ).checked ){ color2h = 4; }
		if( document.getElementById( "color2h_5" ).checked ){ color2h = 5; }
		if( document.getElementById( "color2h_6" ).checked ){ color2h = 6; }
		if( document.getElementById( "color2h_7" ).checked ){ color2h = 7; }
		if( document.getElementById( "color2h_8" ).checked ){ color2h = 8; }
		if( document.getElementById( "color2h_9" ).checked ){ color2h = 9; }
		if( document.getElementById( "color2h_10" ).checked ){ color2h = 10; }
		if( document.getElementById( "color2h_11" ).checked ){ color2h = 11; }

		$.post( "gm-color.cgi", { command:'update', code:code, color1:color1, color2:color2, color1h:color1h, color2h:color2h }, function( data ){ $( "#LF" ).html( data );});
		displayVIDEO( code + ' saved' );
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Food name dictionary ////////////////////////////////////////////////////////////////////////

// Food name dictionary init
var initDic = function( command, sg, org_name, dfn ){
	$.post( "gm-dic.cgi", { command:'menu' }, function( data ){ $( "#LINE" ).html( data );});
	$.post( "gm-dic.cgi", { command:command, sg:sg, org_name:org_name, dfn:dfn }, function( data ){ $( "#L1" ).html( data );});

	flashBW();
	dl1 = true;
	dline = true;
	displayBW();

};

// Food name dictionary Sub group
var changeDic = function( sg ){
	$.post( "gm-dic.cgi", { command:'change', sg:sg }, function( data ){ $( "#L1" ).html( data );});
};

// Direct food name dictionary button
var saveDic = function( org_name, sg ){
	var aliases = document.getElementById( org_name ).value;
	var dfn = document.getElementById( 'dfn_' + org_name ).value;
	$.post( "gm-dic.cgi", { command:'update', org_name:org_name, aliases:aliases, sg:sg, dfn:dfn }, function( data ){
//		$( "#L1" ).html( data );
		displayVIDEO( org_name + ' modified' );
	});
};

// Add new food into dictionary button
var newDic = function(){
	var org_name = document.getElementById( 'new_org_name' ).value;
	var aliases = document.getElementById( 'new_alias' ).value;
	var sg = document.getElementById( 'new_fg' ).value;
	var dfn = document.getElementById( 'dic_def_fn' ).value;
	$.post( "gm-dic.cgi", { command:'new', org_name:org_name, aliases:aliases, sg:sg, dfn:dfn }, function( data ){
//		$( "#L1" ).html( data );
		displayVIDEO( org_name + ' saved' );
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Allergen ////////////////////////////////////////////////////////////////////////

// Allergen init
var initAllergen = function( com ){
	if( com == 'init' ){ closeBroseWindows( 0 ); }
	$.post( "gm-allergen.cgi", { command:com }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Direct allergen button
var directAllergen = function( code ){
	$.post( "gm-allergen.cgi", { command:'init', code:code }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Allergen ON
var onAllergen = function(){
	var code = document.getElementById( 'code' ).value;
	var allergen = 0
	if(document.getElementById( 'ag_class1' ).checked == true ){ allergen = '1' }
	if(document.getElementById( 'ag_class2' ).checked == true ){ allergen = '2' }
	$.post( "gm-allergen.cgi", { command:'on', code:code, allergen:allergen }, function( data ){ $( "#LF" ).html( data );});
	displayVIDEO( code + ':allergen ON' );
};

// Allergen OFF
var offAllergen = function( code ){
	$.post( "gm-allergen.cgi", { command:'off', code:code }, function( data ){ $( "#LF" ).html( data );});
	displayVIDEO( code + ':allergen OFF' );
};


/////////////////////////////////////////////////////////////////////////////////
// Green yellow color vegetable ////////////////////////////////////////////////////////////////////////

// GYCV init
var initGYCV = function( com ){
	if( com == 'init' ){ closeBroseWindows( 0 ); }
	$.post( "gm-gycv.cgi", { command:com }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// GYCV ON
var onGYCV = function(){
	var food_no = document.getElementById( 'food_no' ).value;
	$.post( "gm-gycv.cgi", { command:'on', food_no:food_no }, function( data ){ $( "#LF" ).html( data );});
	displayVIDEO( food_no + ':GYCV ON' );
};

// GYCV OFF
var offGYCV = function( food_no ){
	$.post( "gm-gycv.cgi", { command:'off', food_no:food_no }, function( data ){ $( "#LF" ).html( data );});
	displayVIDEO( food_no + ':GYCV OFF' );
};

/////////////////////////////////////////////////////////////////////////////////
// Shun ////////////////////////////////////////////////////////////////////////

// Shun init
var initShun = function( com ){
	if( com == 'init' ){ closeBroseWindows( 0 ); }
	$.post( "gm-shun.cgi", { command:com }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Direct shun button
var directShun = function( code ){
	$.post( "gm-shun.cgi", { command:'init', code:code }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

// Shun ON
var onShun = function(){
	var code = document.getElementById( 'code' ).value;
	var shun1s = document.getElementById( 'shun1s' ).value;
	var shun1e = document.getElementById( 'shun1e' ).value;
	var shun2s = document.getElementById( 'shun2s' ).value;
	var shun2e = document.getElementById( 'shun2e' ).value;
	$.post( "gm-shun.cgi", { command:'on', code:code, shun1s:shun1s, shun1e:shun1e, shun2s:shun2s, shun2e:shun2e }, function( data ){ $( "#LF" ).html( data );});
	displayVIDEO( code + ':Shun ON' );
};

// Shun OFF
var offShun = function( code ){
	$.post( "gm-shun.cgi", { command:'off', code:code }, function( data ){ $( "#LF" ).html( data );});
	displayVIDEO( code + ':Shun OFF' );
};


/////////////////////////////////////////////////////////////////////////////////
// Food search log ////////////////////////////////////////////////////////////////////////

// Food search log init
var initSlogf = function( com ){
	closeBroseWindows( 1 );
	$.post( "gm-slogf.cgi", { command:com }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Account ////////////////////////////////////////////////////////////////////////

// Account init
var initAccount = function( com ){
	closeBroseWindows( 1 );
	$.post( "gm-account.cgi", { command:com }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};

// Edit account
var editAccount = function( target_uid ){
	$.post( "gm-account.cgi", { command:'edit', target_uid:target_uid }, function( data ){ $( "#L2" ).html( data );});
	document.getElementById( "L1" ).style.display = 'none';
	document.getElementById( "L2" ).style.display = 'block';
};

// Update account
var saveAccount = function( target_uid ){
	var target_pass = document.getElementById( 'target_pass' ).value;
	var target_mail = document.getElementById( 'target_mail' ).value;
	var target_aliasu = document.getElementById( 'target_aliasu' ).value;
	var target_status = document.getElementById( 'target_status' ).value;
	var target_language = document.getElementById( 'target_language' ).value;
	$.post( "gm-account.cgi", { command:'save', target_uid:target_uid, target_pass:target_pass, target_mail:target_mail, target_aliasu:target_aliasu, target_status:target_status, target_language:target_language }, function( data ){ $( "#L1" ).html( data );});
	displayVIDEO( target_uid + ' saved' );
	document.getElementById( "L2" ).style.display = 'none';
	document.getElementById( "L1" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Memory ////////////////////////////////////////////////////////////////////////

// Memory init
var initMemory = function(){
	$.post( "gm-memory.cgi", { command:'init', post_process:'front' }, function( data ){ $( "#L1" ).html( data );});
	flashBW();
	dl1 = true;
	displayBW();
};

// Save New category
var saveCategory = function(){
	var category = document.getElementById( 'category' ).value;
	if( category != '' ){
		$.post( "gm-memory.cgi", { command:'save_category', category:category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( '(>_<)category name!!' );
	}
};

// Change category name
var changeCategory = function( category ){
	var new_category = document.getElementById( category ).value;
	if( category != '' ){
		$.post( "gm-memory.cgi", { command:'change_category', category:category, new_category:new_category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( '(>_<)category name!!' );
	}
};

// Delete category
var deleteCategory = function( category, delete_check_no ){
	if( document.getElementById( delete_check_no ).checked ){
		$.post( "gm-memory.cgi", { command:'delete_category', category:category }, function( data ){ $( "#L1" ).html( data );});
		flashBW();
		dl1	= true;
		displayBW();
	}else{
		displayVIDEO( 'Check!' );
	}
};

// List each pointer
var listPointer = function( category ){
	$.post( "gm-memory.cgi", { command:'list_pointer', category:category, post_process:'front' }, function( data ){ $( "#L1" ).html( data );});
	flashBW();
	dl1 = true;
	displayBW();
};

// New pointer form
var newPMemory = function( category, pointer, post_process ){
	$.post( "gm-memory.cgi", { command:'new_pointer', category:category, pointer:pointer, post_process:post_process }, function( data ){ $( "#LF" ).html( data );});
	dl1 = false;
	if( post_process == 'front'){ dl2 = false; }
	dlf = true;
	displayBW();
};

// New pointer form from nomatch
var newPMemoryNM = function( pointer, post_process ){
	var category = document.getElementById( 'nonmatch_categoly' ).value;
	$.post( "gm-memory.cgi", { command:'new_pointer', category:category, pointer:pointer, post_process:post_process }, function( data ){ $( "#LF" ).html( data );});
	if( post_process == 'front'){ dl1 = false; }
	dlf = true;
	displayBW();
};

// Save pointer
var savePMemory = function( category, post_process ){
	var pointer = document.getElementById( 'pointer' ).value;
	var memory = document.getElementById( 'memory' ).value;
	var rank = document.getElementById( 'rank' ).value;

	if( pointer != '' ){
		if( post_process == 'front'){
			$.post( "gm-memory.cgi", { command:'save_pointer', memory:memory, category:category, pointer:pointer, rank:rank, post_process:post_process }, function( data ){ $( "#L2" ).html( data );});
			$.post( "gm-memory.cgi", { command:'list_pointer', category:category, post_process:post_process }, function( data ){ $( "#L1" ).html( data );});
			dl1 = true;
			dl2 = false;
		}else{
			$.post( "gm-memory.cgi", { command:'save_pointer', memory:memory, category:category, pointer:pointer, rank:rank, post_process:post_process }, function( data ){});
		}
		dlf = false
		displayBW();
	}else{
		displayVIDEO( '(>_<)key!!' );
	}
	displayVIDEO( 'Saved' );
}

// Move pointer
var movePMemory = function( category, pointer, post_process ){
	var memory = document.getElementById( 'memory' ).value;
	var rank = document.getElementById( 'rank' ).value;
	var mvcategory = document.getElementById( 'mvcategory' ).value;

	if( post_process == 'front'){
		$.post( "gm-memory.cgi", { command:'move_pointer', memory:memory, category:category, pointer:pointer, rank:rank, mvcategory:mvcategory }, function( data ){ $( "#L2" ).html( data );});
		$.post( "gm-memory.cgi", { command:'init' }, function( data ){ $( "#L1" ).html( data );});
		document.getElementById( "L1" ).style.display = 'block';
	}else{
		$.post( "gm-memory.cgi", { command:'move_pointer', memory:memory, category:category, pointer:pointer, rank:rank, mvcategory:mvcategory }, function( data ){});
	}
	document.getElementById( "LF" ).style.display = 'none';

	displayVIDEO( 'Moved' );
}

// Delete pointer
var deletePMemory = function( category, pointer, post_process ){
	if( document.getElementById( 'deletepm_check' ).checked ){
		if( post_process == 'front'){
			$.post( "gm-memory.cgi", { command:'delete_pointer', category:category, pointer:pointer, post_process }, function( data ){ $( "#L2" ).html( data );});
			$.post( "gm-memory.cgi", { command:'init' }, function( data ){ $( "#L1" ).html( data );});
			document.getElementById( "L1" ).style.display = 'block';
		}else{
			$.post( "gm-memory.cgi", { command:'delete_pointer', category:category, pointer:pointer, post_process }, function( data ){});
		}
		document.getElementById( "LF" ).style.display = 'none';
	}else{
		displayVIDEO( '(>_<)check!!' );
	}
};

/////////////////////////////////////////////////////////////////////////////////
// DB table export ////////////////////////////////////////////////////////////////////////

var initExport = function(){
	closeBroseWindows( 1 );
	$.post( "gm-export.cgi", { command:'init' }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};

/////////////////////////////////////////////////////////////////////////////////
// DB table import ////////////////////////////////////////////////////////////////////////

var initImport = function(){
	closeBroseWindows( 1 );
	$.post( "gm-import.cgi", { command:'init' }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};

var confirmImport = function(){
	var mode = 0;
	if( document.getElementById( 'mode' ).checked ){ mode = 1; }

	form_data = new FormData( $( '#import_form' )[0] );
	form_data.append( 'command', 'confirm' );
	form_data.append( 'mode', mode );
	$.ajax( "gm-import.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ $( '#L2' ).html( data ); }
		}
	);
	document.getElementById( "L2" ).style.display = 'block';
};

var updateImport = function( tf_name, mode ){
	$.post( "gm-import.cgi", { command:'update', tf_name:tf_name, mode:mode }, function( data ){ $( "#L2" ).html( data );});
};
