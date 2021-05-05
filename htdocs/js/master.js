// master.js 0.00b 20210503
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

// Update unit exchange button
var updateUintc = function(){
	var code = document.getElementById( "food_no" ).value;

	if( code != '' ){
		var uc2 = document.getElementById( "unitc2" ).value;
		var uc3 = document.getElementById( "unitc3" ).value;
		var uc4 = document.getElementById( "unitc4" ).value;
		var uc5 = document.getElementById( "unitc5" ).value;
		var uc6 = document.getElementById( "unitc6" ).value;
		var uc7 = document.getElementById( "unitc7" ).value;
		var uc8 = document.getElementById( "unitc8" ).value;
		var uc9 = document.getElementById( "unitc9" ).value;
		var uc10 = document.getElementById( "unitc10" ).value;
		var uc11 = document.getElementById( "unitc11" ).value;
		var uc12 = document.getElementById( "unitc12" ).value;
		var uc13 = document.getElementById( "unitc13" ).value;
		var uc14 = document.getElementById( "unitc14" ).value;
		var uc16 = document.getElementById( "unitc16" ).value;
		var uc17 = document.getElementById( "unitc17" ).value;
		var notice = document.getElementById( "notice" ).value;

		$.post( "gm-unitc.cgi", { command:'update', code:code, unitc2:uc2, unitc3:uc3, unitc4:uc4, unitc5:uc5, unitc6:uc6, unitc7:uc7, unitc8:uc8, unitc9:uc9, unitc10:uc10, unitc11:uc11, unitc12:uc12, unitc13:uc13, unitc14:uc14, unitc16:uc16, unitc17:uc17, notice:notice}, function( data ){ $( "#LF" ).html( data );});
		displayVIDEO( code + ' saved' );
	}
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
var initDic = function( command, sg ){
	closeBroseWindows( 1 );
	$.post( "gm-dic.cgi", { command:'menu' }, function( data ){ $( "#LINE" ).html( data );});
	$.post( "gm-dic.cgi", { command:command, sg:sg }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
	displayLINE( 'on' );
};

// Food name dictionary Sub group
var changeDic = function( sg ){
	$.post( "gm-dic.cgi", { command:'change', sg:sg }, function( data ){ $( "#L1" ).html( data );});
};

// Direct food name dictionary button
var saveDic = function( org_name ){
	var aliases = document.getElementById( org_name ).value;
	$.post( "gm-dic.cgi", { command:'update', org_name:org_name, aliases:aliases }, function( data ){});
	displayVIDEO( org_name + ' modified' );
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
	if(document.getElementById( 'ag_class3' ).checked == true ){ allergen = '3' }
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
		dl1	true;
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
